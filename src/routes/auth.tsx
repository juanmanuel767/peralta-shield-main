import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { z } from "zod";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/hooks/useAuth";
import { Layout } from "@/components/peralta/Layout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Shield } from "lucide-react";
import { toast } from "sonner";

export const Route = createFileRoute("/auth")({
  validateSearch: z.object({
    redirect: z.string().optional(),
  }),
  head: () => ({
    meta: [
      { title: "Acceder — Peralta Antivirus" },
      { name: "description", content: "Crea tu cuenta o inicia sesión en Peralta." },
    ],
  }),
  component: AuthPage,
});

const signUpSchema = z.object({
  email: z.string().trim().email("Email inválido").max(255),
  password: z.string().min(8, "Mínimo 8 caracteres").max(72),
  displayName: z.string().trim().min(2, "Mínimo 2 caracteres").max(50),
});
const signInSchema = z.object({
  email: z.string().trim().email("Email inválido").max(255),
  password: z.string().min(1).max(72),
});

function AuthPage() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const { redirect } = Route.useSearch();
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!loading && user) {
      navigate({ to: redirect || "/community" });
    }
  }, [user, loading, navigate, redirect]);

  async function handleSignUp(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const parsed = signUpSchema.safeParse({
      email: fd.get("email"),
      password: fd.get("password"),
      displayName: fd.get("displayName"),
    });
    if (!parsed.success) return toast.error(parsed.error.issues[0].message);
    setBusy(true);
    const { error } = await supabase.auth.signUp({
      email: parsed.data.email,
      password: parsed.data.password,
      options: {
        emailRedirectTo: `${window.location.origin}/community`,
        data: { display_name: parsed.data.displayName },
      },
    });
    setBusy(false);
    if (error) return toast.error(error.message);
    toast.success("¡Cuenta creada! Revisa tu email para confirmar.");
  }

  async function handleSignIn(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const parsed = signInSchema.safeParse({ email: fd.get("email"), password: fd.get("password") });
    if (!parsed.success) return toast.error(parsed.error.issues[0].message);
    setBusy(true);
    const { error } = await supabase.auth.signInWithPassword(parsed.data);
    setBusy(false);
    if (error) return toast.error(error.message);
    toast.success("Bienvenido de vuelta");
    navigate({ to: "/community" });
  }

  return (
    <Layout>
      <section className="container mx-auto px-6 py-20 flex justify-center">
        <div className="w-full max-w-md p-8 rounded-3xl border border-border" style={{ background: "var(--gradient-card)" }}>
          <div className="flex items-center gap-2 justify-center mb-6">
            <Shield className="h-7 w-7 text-primary" />
            <span className="font-bold text-xl">Peralta</span>
          </div>
          <Tabs defaultValue="signin">
            <TabsList className="grid grid-cols-2 w-full">
              <TabsTrigger value="signin">Entrar</TabsTrigger>
              <TabsTrigger value="signup">Registrarse</TabsTrigger>
            </TabsList>
            <TabsContent value="signin">
              <form onSubmit={handleSignIn} className="space-y-4 mt-6">
                <div><Label>Email</Label><Input name="email" type="email" required /></div>
                <div><Label>Contraseña</Label><Input name="password" type="password" required /></div>
                <Button type="submit" disabled={busy} className="w-full bg-gradient-to-r from-primary to-accent text-primary-foreground">{busy ? "..." : "Entrar"}</Button>
              </form>
            </TabsContent>
            <TabsContent value="signup">
              <form onSubmit={handleSignUp} className="space-y-4 mt-6">
                <div><Label>Nombre</Label><Input name="displayName" required maxLength={50} /></div>
                <div><Label>Email</Label><Input name="email" type="email" required /></div>
                <div><Label>Contraseña</Label><Input name="password" type="password" required minLength={8} /></div>
                <Button type="submit" disabled={busy} className="w-full bg-gradient-to-r from-primary to-accent text-primary-foreground">{busy ? "..." : "Crear cuenta"}</Button>
              </form>
            </TabsContent>
          </Tabs>
        </div>
      </section>
    </Layout>
  );
}
