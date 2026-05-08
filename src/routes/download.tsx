import { createFileRoute, Link } from "@tanstack/react-router";
import { Layout } from "@/components/peralta/Layout";
import { Button } from "@/components/ui/button";
import { DOWNLOAD_CONFIG } from "@/lib/download-config";
import { useOS, OS } from "@/hooks/useOS";
import { useAuth } from "@/hooks/useAuth";
import { Monitor, Apple, Terminal, ChevronRight, CheckCircle2, Download as DownloadIcon, Info, Lock, Copy, Star, MessageSquare, UserPlus } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "sonner";

export const Route = createFileRoute("/download")({
  head: () => ({
    meta: [
      { title: "Descargar — Peralta Antivirus" },
      { name: "description", content: "Descarga Peralta Antivirus para Windows, macOS y Linux. Protección neuronal gratuita y de código abierto." },
    ],
  }),
  component: DownloadPage,
});

function DownloadPage() {
  const detectedOS = useOS();
  const { user, loading: authLoading } = useAuth();
  const [hasReviewed, setHasReviewed] = useState<boolean | null>(null);
  const [checkingReview, setCheckingReview] = useState(false);

  useEffect(() => {
    async function checkReview() {
      if (!user) return;
      setCheckingReview(true);
      try {
        const { count, error } = await supabase
          .from("comments")
          .select("*", { count: "exact", head: true })
          .eq("user_id", user.id);
        
        if (!error) {
          setHasReviewed((count ?? 0) > 0);
        } else {
          // If error (e.g. table doesn't exist yet), we assume no review
          setHasReviewed(false);
        }
      } catch (e) {
        setHasReviewed(false);
      } finally {
        setCheckingReview(false);
      }
    }
    checkReview();
  }, [user]);

  return (
    <Layout>
      <section className="container mx-auto px-6 py-16 md:py-24 max-w-5xl">
        <div className="text-center mb-16 animate-slide-up">
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6 mt-16 font-display">Obtén tu protección hoy</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Peralta V{DOWNLOAD_CONFIG.version} está optimizado para brindarte la máxima seguridad con el mínimo impacto en el rendimiento.
          </p>
        </div>

        {/* Gate: User must be registered */}
        {!loading && !user ? (
          <div className="max-w-2xl mx-auto animate-fade-in">
            <div className="relative p-1 rounded-[2.5rem] bg-gradient-to-r from-primary via-accent to-primary bg-[length:200%_100%] animate-gradient-x">
              <div className="bg-background rounded-[2.4rem] p-10 md:p-16 text-center">
                <div className="mx-auto w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mb-8 border border-primary/20">
                  <Lock className="h-10 w-10 text-primary" />
                </div>
                <h2 className="text-3xl md:text-4xl font-bold mb-4 font-display">Regístrate para descargar</h2>
                <p className="text-muted-foreground text-lg mb-3 max-w-md mx-auto leading-relaxed">
                  Peralta Antivirus es <span className="text-foreground font-semibold">100% gratis</span>. Solo te pedimos una cosa a cambio:
                </p>
                <p className="text-primary font-bold text-xl mb-8">
                  Tu opinión honesta ⭐
                </p>

                <div className="space-y-4 text-left max-w-sm mx-auto mb-10">
                  {[
                    { icon: UserPlus, text: "Crea tu cuenta gratuita (10 segundos)" },
                    { icon: DownloadIcon, text: "Descarga Peralta para tu sistema operativo" },
                    { icon: Star, text: "Deja tu reseña — es el único \"costo\"" },
                  ].map((step, i) => (
                    <div key={i} className="flex items-center gap-4 p-3 rounded-xl bg-muted/30 border border-border/50">
                      <div className="h-9 w-9 rounded-lg bg-primary/10 flex items-center justify-center text-primary shrink-0">
                        <step.icon className="h-4 w-4" />
                      </div>
                      <span className="text-sm font-medium">{step.text}</span>
                    </div>
                  ))}
                </div>

                <Link to="/auth" search={{ redirect: "/download" }}>
                  <Button size="lg" className="h-16 px-12 text-lg bg-gradient-to-r from-primary to-accent text-primary-foreground shadow-[0_0_40px_-5px_oklch(0.78_0.18_175/0.4)] hover:scale-105 transition-premium">
                    <UserPlus className="h-6 w-6 mr-3" /> Crear Cuenta Gratis
                  </Button>
                </Link>
                <p className="mt-4 text-xs text-muted-foreground">
                  ¿Ya tienes cuenta? <Link to="/auth" search={{ redirect: "/download" }} className="text-primary hover:underline font-semibold">Inicia sesión</Link>
                </p>
              </div>
            </div>
          </div>
        ) : authLoading || checkingReview ? (
          <div className="flex justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
          </div>
        ) : !hasReviewed ? (
          /* Locked Content: Must Review First */
          <div className="max-w-2xl mx-auto animate-fade-in">
            <div className="bg-card/40 border border-yellow-500/30 rounded-[2.5rem] p-10 md:p-16 text-center backdrop-blur-md">
              <div className="mx-auto w-20 h-20 rounded-full bg-yellow-500/10 flex items-center justify-center mb-8 border border-yellow-500/20">
                <Star className="h-10 w-10 text-yellow-500" />
              </div>
              <h2 className="text-3xl font-bold mb-4 font-display text-white">Último paso requerido</h2>
              <p className="text-muted-foreground text-lg mb-8 leading-relaxed">
                Has iniciado sesión correctamente. Ahora, para desbloquear la descarga de grado militar, necesitamos tu **Reseña de Inteligencia**.
              </p>
              
              <div className="p-6 rounded-2xl bg-yellow-500/5 border border-yellow-500/10 mb-10 text-sm text-yellow-200/70 italic">
                "Peralta es gratuito gracias a la comunidad. Tu reporte ayuda a mejorar el motor neuronal para todos."
              </div>

              <Link to="/community">
                <Button size="lg" className="h-16 px-12 text-lg bg-yellow-600 hover:bg-yellow-500 text-white shadow-xl hover:scale-105 transition-premium w-full sm:w-auto">
                  <MessageSquare className="h-6 w-6 mr-3" /> Dejar Reseña y Desbloquear
                </Button>
              </Link>
            </div>
          </div>
        ) : (
          <>
            {/* Download Section (authenticated) */}
            <Tabs defaultValue={detectedOS !== "unknown" ? detectedOS : "windows"} className="w-full">
              <TabsList className="grid grid-cols-3 w-full max-w-2xl mx-auto h-20 bg-muted/50 p-2 rounded-2xl mb-12 border border-border/50">
                <TabsTrigger value="windows" className="rounded-xl data-[state=active]:bg-background data-[state=active]:shadow-lg gap-2">
                  <Monitor className="h-5 w-5" /> <span className="hidden sm:inline">Windows</span>
                </TabsTrigger>
                <TabsTrigger value="macos" className="rounded-xl data-[state=active]:bg-background data-[state=active]:shadow-lg gap-2">
                  <Apple className="h-5 w-5" /> <span className="hidden sm:inline">macOS</span>
                </TabsTrigger>
                <TabsTrigger value="linux" className="rounded-xl data-[state=active]:bg-background data-[state=active]:shadow-lg gap-2">
                  <Terminal className="h-5 w-5" /> <span className="hidden sm:inline">Linux</span>
                </TabsTrigger>
              </TabsList>

              {(Object.entries(DOWNLOAD_CONFIG.platforms) as [OS, any][]).map(([key, platform]) => (
                <TabsContent key={key} value={key} className="animate-fade-in focus-visible:outline-none">
                  <div className="grid md:grid-cols-5 gap-8 items-start">
                    {/* Main Download Card */}
                    <div className="md:col-span-3 p-8 md:p-12 rounded-3xl border border-primary/30 bg-gradient-to-br from-primary/5 via-background to-accent/5 shadow-2xl relative overflow-hidden group">
                      <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
                        {key === "windows" && <Monitor size={160} />}
                        {key === "macos" && <Apple size={160} />}
                        {key === "linux" && <Terminal size={160} />}
                      </div>
                      
                      <div className="relative z-10">
                        <div className="flex items-center gap-2 text-primary font-bold uppercase tracking-widest text-xs mb-6">
                          <DownloadIcon className="h-4 w-4" /> Recomendado para tu sistema
                        </div>
                        <h2 className="text-4xl font-bold mb-4">Peralta para {platform.name}</h2>
                        <p className="text-muted-foreground mb-8 text-lg">{platform.version} · {platform.size}</p>
                        
                        <div className="space-y-6">
                          <a href={platform.url} download>
                            <Button size="lg" className="h-16 px-10 text-lg bg-gradient-to-r from-primary to-accent text-primary-foreground shadow-[0_0_40px_-5px_oklch(0.78_0.18_175/0.4)] hover:scale-105 transition-premium group w-full sm:w-auto">
                              <DownloadIcon className="h-6 w-6 mr-3 group-hover:animate-bounce" /> Descargar Ahora
                            </Button>
                          </a>
                        </div>
                        
                        <div className="mt-8 flex items-center gap-6 text-xs text-muted-foreground/60 font-mono">
                          <span>Ver: v{DOWNLOAD_CONFIG.version}</span>
                          <span className="hidden sm:inline">SHA-256: {platform.checksum.slice(0, 12)}...</span>
                        </div>
                      </div>
                    </div>

                    {/* Instructions Column */}
                    <div className="md:col-span-2 space-y-6">
                      <div className="p-6 rounded-2xl border border-border bg-card/40">
                        <h3 className="font-bold flex items-center gap-2 mb-4">
                          <ChevronRight className="h-5 w-5 text-primary" /> Instrucciones de Instalación
                        </h3>
                        <ul className="space-y-4">
                          {platform.steps.map((step: string, i: number) => (
                            <li key={i} className="flex gap-3 text-sm text-muted-foreground leading-relaxed">
                              <CheckCircle2 className="h-5 w-5 text-primary shrink-0 mt-0.5" />
                              <span>{step}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div className="p-4 rounded-xl border border-border/50 bg-muted/20 flex gap-3 text-xs text-muted-foreground italic">
                        <Info className="h-4 w-4 shrink-0 text-primary" />
                        <p>Al descargar Peralta Antivirus, aceptas nuestros términos de servicio y políticas de privacidad garantizadas de código abierto.</p>
                      </div>

                      {platform.terminalCommand && (
                        <div className="p-6 rounded-2xl border border-primary/20 bg-black/40 backdrop-blur-sm animate-fade-in">
                          <h3 className="text-sm font-bold flex items-center gap-2 mb-4 text-primary">
                            <Terminal className="h-4 w-4" /> Instalación vía Terminal
                          </h3>
                          <div className="relative group">
                            <code className="block bg-black p-4 rounded-lg text-xs leading-relaxed font-mono text-emerald-400 overflow-x-auto border border-white/5 break-all">
                              {platform.terminalCommand}
                            </code>
                            <Button 
                              size="sm" 
                              variant="ghost" 
                              className="absolute top-2 right-2 h-8 w-8 p-0 hover:bg-white/10"
                              onClick={() => {
                                navigator.clipboard.writeText(platform.terminalCommand);
                                toast.success("Comando copiado al portapapeles");
                              }}
                            >
                              <Copy className="h-4 w-4" />
                            </Button>
                          </div>
                          <p className="mt-3 text-[10px] text-muted-foreground">
                            Copia y pega este comando en tu terminal para descargar e instalar Peralta en un solo paso.
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </TabsContent>
              ))}
            </Tabs>

            {/* Review CTA — the "cost" of the antivirus */}
            <div className="mt-16 relative p-1 rounded-[2.5rem] bg-gradient-to-r from-yellow-500 via-primary to-accent">
              <div className="bg-background rounded-[2.4rem] p-10 md:p-14 text-center">
                <div className="mx-auto w-16 h-16 rounded-full bg-yellow-500/10 flex items-center justify-center mb-6 border border-yellow-500/20">
                  <Star className="h-8 w-8 text-yellow-500 fill-yellow-500" />
                </div>
                <h3 className="text-2xl md:text-3xl font-bold mb-3 font-display">¡Gracias por descargar Peralta!</h3>
                <p className="text-muted-foreground text-lg mb-8 max-w-lg mx-auto">
                  Este antivirus es <span className="text-foreground font-semibold">gratuito</span>. El único "pago" que te pedimos es una reseña honesta para ayudar a otros usuarios.
                </p>
                <Link to="/community">
                  <Button size="lg" className="h-14 px-10 text-lg bg-gradient-to-r from-yellow-500 to-primary text-white shadow-lg hover:scale-105 transition-premium">
                    <MessageSquare className="h-5 w-5 mr-3" /> Dejar Mi Reseña ⭐
                  </Button>
                </Link>
              </div>
            </div>

            {/* System Requirements Footer */}
            <div className="mt-24 border-t border-border pt-16">
              <h3 className="text-2xl font-bold mb-8 text-center">Requisitos Mínimos</h3>
              <div className="grid sm:grid-cols-3 gap-8">
                <div className="text-center p-6 bg-card/20 rounded-2xl border border-border/50">
                  <p className="text-primary font-bold mb-2">Procesador</p>
                  <p className="text-sm text-muted-foreground text-foreground">Dual Core 1.6GHz o superior</p>
                </div>
                <div className="text-center p-6 bg-card/20 rounded-2xl border border-border/50">
                  <p className="text-primary font-bold mb-2">Memoria RAM</p>
                  <p className="text-sm text-muted-foreground text-foreground">2 GB mínimo (4 GB recomendado)</p>
                </div>
                <div className="text-center p-6 bg-card/20 rounded-2xl border border-border/50">
                  <p className="text-primary font-bold mb-2">Disco Duro</p>
                  <p className="text-sm text-muted-foreground text-foreground">500 MB de espacio libre</p>
                </div>
              </div>
            </div>
          </>
        )}
      </section>
    </Layout>
  );
}
