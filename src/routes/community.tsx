import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState, useRef } from "react";
import { z } from "zod";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/hooks/useAuth";
import { Layout } from "@/components/peralta/Layout";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Star, MessageSquare, ShieldCheck, Activity, Terminal, ShieldAlert, Zap, Lock, Filter } from "lucide-react";
import { toast } from "sonner";

export const Route = createFileRoute("/community")({
  head: () => ({
    meta: [
      { title: "Centro de Inteligencia — Peralta Antivirus" },
      { name: "description", content: "Reportes reales de la comunidad Peralta. Inteligencia colectiva contra amenazas." },
    ],
  }),
  component: Community,
});

type Comment = { id: string; user_id: string; content: string; rating: number; created_at: string; display_name?: string };

const schema = z.object({
  content: z.string().trim().min(3, "Mínimo 3 caracteres").max(1000, "Máximo 1000"),
  rating: z.number().int().min(1).max(5),
});

function Community() {
  const { user } = useAuth();
  const [comments, setComments] = useState<Comment[]>([]);
  const [content, setContent] = useState("");
  const [rating, setRating] = useState(5);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);

  async function load() {
    try {
      const { data: cs } = await supabase.from("comments").select("*").order("created_at", { ascending: false }).limit(100);
      if (!cs) {
        setComments([]);
        return;
      }
      const ids = Array.from(new Set(cs.map((c) => c.user_id)));
      const { data: profs } = ids.length
        ? await supabase.from("profiles").select("id, display_name").in("id", ids)
        : { data: [] as { id: string; display_name: string }[] };
      const map = new Map((profs ?? []).map((p) => [p.id, p.display_name]));
      setComments(cs.map((c) => ({ ...c, display_name: map.get(c.user_id) ?? "Usuario Anónimo" })));
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!user) return toast.error("Inicia sesión para reportar");
    const parsed = schema.safeParse({ content, rating });
    if (!parsed.success) return toast.error(parsed.error.issues[0].message);
    setBusy(true);
    const { error } = await supabase.from("comments").insert({ user_id: user.id, content: parsed.data.content, rating: parsed.data.rating });
    setBusy(false);
    if (error) return toast.error(error.message);
    setContent("");
    setRating(5);
    toast.success("¡Reporte de inteligencia enviado!");
    load();
  }

  return (
    <Layout>
      <section className="container mx-auto px-6 py-16 md:py-24 max-w-5xl">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-16 animate-slide-up">
          <div className="space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-[10px] font-bold uppercase tracking-widest">
              <Activity className="h-3 w-3 animate-pulse" />
              Feed de Inteligencia en Tiempo Real
            </div>
            <h1 className="text-5xl md:text-6xl font-bold tracking-tight font-display">Comunidad</h1>
            <p className="text-xl text-muted-foreground max-w-xl">
              Nuestra red de usuarios reporta actividad y efectividad del motor neuronal Peralta en entornos reales de combate.
            </p>
          </div>
          <div className="flex gap-4">
            <div className="p-4 rounded-2xl bg-card/30 border border-border/50 text-center min-w-[120px]">
              <div className="text-2xl font-bold font-display">{comments.length}</div>
              <div className="text-[10px] text-muted-foreground uppercase font-bold tracking-tighter">REPORTES ACTIVOS</div>
            </div>
            <div className="p-4 rounded-2xl bg-card/30 border border-border/50 text-center min-w-[120px]">
              <div className="text-2xl font-bold font-display text-primary">100%</div>
              <div className="text-[10px] text-muted-foreground uppercase font-bold tracking-tighter">EFICACIA COMUNAL</div>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-12">
          {/* Post Comment Section */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 space-y-6">
              <div className="p-8 rounded-[2rem] border border-primary/30 bg-gradient-to-br from-primary/5 via-background to-accent/5 shadow-2xl relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
                  <ShieldCheck size={80} />
                </div>
                
                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Terminal className="h-5 w-5 text-primary" /> Enviar Reporte
                </h2>
                
                {user ? (
                  <form onSubmit={submit} className="space-y-6">
                    <div className="space-y-3">
                      <label className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Nivel de Satisfacción</label>
                      <div className="flex items-center justify-between p-3 rounded-xl bg-background/50 border border-border">
                        {[1, 2, 3, 4, 5].map((n) => (
                          <button 
                            type="button" 
                            key={n} 
                            onClick={() => setRating(n)} 
                            className="transition-all hover:scale-125"
                          >
                            <Star className={`h-6 w-6 ${n <= rating ? "fill-primary text-primary" : "text-muted-foreground/30"}`} />
                          </button>
                        ))}
                      </div>
                    </div>
                    
                    <div className="space-y-3">
                      <label className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Contenido del Reporte</label>
                      <Textarea 
                        value={content} 
                        onChange={(e) => setContent(e.target.value)} 
                        placeholder="Escribe sobre la eficiencia del antivirus, detección de amenazas o rendimiento..." 
                        className="bg-background/50 border-border h-40 resize-none focus:ring-primary/20"
                        maxLength={1000} 
                      />
                    </div>
                    
                    <Button 
                      type="submit" 
                      disabled={busy} 
                      className="w-full h-14 bg-gradient-to-r from-primary to-accent text-primary-foreground text-md font-bold shadow-lg shadow-primary/20 hover:scale-[1.02] transition-premium"
                    >
                      {busy ? (
                        <div className="flex items-center gap-2">
                          <Activity className="h-4 w-4 animate-spin" /> PROCESANDO...
                        </div>
                      ) : (
                        <div className="flex items-center gap-2">
                          <Zap className="h-4 w-4" /> ENVIAR INTELIGENCIA
                        </div>
                      )}
                    </Button>
                  </form>
                ) : (
                  <div className="text-center py-6 space-y-6">
                    <div className="mx-auto w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center border border-primary/20">
                      <Lock className="h-8 w-8 text-primary" />
                    </div>
                    <p className="text-muted-foreground text-sm">Debes estar autenticado para enviar reportes a la red neuronal.</p>
                    <Link to="/auth" search={{ redirect: "/community" }}>
                      <Button className="w-full h-12">Entrar / Registrarse</Button>
                    </Link>
                  </div>
                )}
              </div>
              
              <div className="p-6 rounded-2xl border border-border bg-card/20 flex gap-4">
                <ShieldAlert className="h-6 w-6 text-yellow-500 shrink-0" />
                <p className="text-xs text-muted-foreground leading-relaxed italic">
                  Todos los reportes son analizados por el equipo de **Juan Manuel Peralta** para garantizar la integridad y veracidad de la información. No compartas datos sensibles.
                </p>
              </div>
            </div>
          </div>

          {/* Comments List */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center justify-between mb-4 px-2">
              <h2 className="text-sm font-bold uppercase tracking-[0.2em] text-muted-foreground inline-flex items-center gap-2">
                <Filter className="h-4 w-4" /> Últimos Reportes Verificados
              </h2>
            </div>

            {loading ? (
              <div className="space-y-4">
                {[1, 2, 3].map(i => (
                  <div key={i} className="h-40 w-full rounded-2xl bg-card/40 animate-pulse border border-border/50" />
                ))}
              </div>
            ) : comments.length === 0 ? (
              <div className="text-center py-20 border-2 border-dashed border-border rounded-[2rem]">
                <MessageSquare className="h-12 w-12 text-muted-foreground mx-auto mb-4 opacity-20" />
                <p className="text-muted-foreground italic">No se han registrado reportes de inteligencia aún. Sé el primero.</p>
              </div>
            ) : (
              <div className="grid gap-6">
                {comments.map((c) => (
                  <article 
                    key={c.id} 
                    className="group relative p-8 rounded-[2rem] border border-border/50 bg-card/30 hover:bg-card/50 hover:border-primary/20 transition-all duration-300 backdrop-blur-sm shadow-sm overflow-hidden animate-fade-in"
                  >
                    {/* Visual accents */}
                    <div className="absolute top-0 right-0 p-6 opacity-0 group-hover:opacity-10 transition-opacity">
                      <ShieldCheck size={100} className="text-primary" />
                    </div>
                    
                    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
                      <div className="flex items-center gap-4">
                        <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-primary to-accent flex items-center justify-center text-lg font-bold text-primary-foreground shadow-lg group-hover:scale-110 transition-transform">
                          {(c.display_name ?? "?").slice(0, 1).toUpperCase()}
                        </div>
                        <div>
                          <p className="font-bold text-foreground leading-none mb-1">{c.display_name}</p>
                          <p className="text-[10px] text-muted-foreground uppercase font-bold tracking-widest flex items-center gap-2">
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                            Reporte Verificado · {new Date(c.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex bg-background/50 backdrop-blur px-3 py-1.5 rounded-full border border-border">
                        {[1, 2, 3, 4, 5].map((n) => (
                          <Star 
                            key={n} 
                            className={`h-3.5 w-3.5 ${n <= c.rating ? "fill-yellow-500 text-yellow-500" : "text-muted-foreground/20"}`} 
                          />
                        ))}
                      </div>
                    </div>
                    <div className="relative">
                      <div className="absolute -left-4 top-0 bottom-0 w-1 bg-gradient-to-b from-primary/50 to-transparent rounded-full opacity-0 group-hover:opacity-100 transition-opacity" />
                      <p className="text-foreground/80 leading-relaxed text-md whitespace-pre-wrap pl-2">
                        {c.content}
                      </p>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>
    </Layout>
  );
}
