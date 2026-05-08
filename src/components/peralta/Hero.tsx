import { Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import { ShieldCheck, Sparkles, Apple, Monitor, Download } from "lucide-react";
import heroShield from "/logo-official.png";
import { useOS } from "@/hooks/useOS";

export function Hero() {
  const os = useOS();
  
  const getOSName = () => {
    if (os === "windows") return "Windows";
    if (os === "macos") return "macOS";
    if (os === "linux") return "Linux";
    return "";
  };

  return (
    <section className="relative overflow-hidden min-h-[85vh] flex items-center" style={{ background: "var(--gradient-hero)" }}>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,oklch(0.78_0.18_175/0.1),transparent_50%)]" />
      
      <div className="container mx-auto px-6 py-20 grid lg:grid-cols-2 gap-16 items-center relative">
        <div className="space-y-8 animate-slide-up">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-primary/30 bg-primary/10 text-primary text-xs font-semibold tracking-wide uppercase animate-fade-in translate-y-0 opacity-100">
            <Sparkles className="h-3.5 w-3.5" /> Seguridad de Próxima Generación
          </div>
          
          <h1 className="text-6xl md:text-7xl font-bold tracking-tighter leading-[0.95] font-display">
            Tu fortaleza digital.<br />
            <span className="bg-gradient-to-r from-primary via-primary-glow to-accent bg-clip-text text-transparent italic">
              Sin compromisos.
            </span>
          </h1>
          
          <p className="text-xl text-muted-foreground max-w-xl leading-relaxed stagger-1 animate-slide-up opacity-0 fill-mode-forwards">
            Peralta Antivirus combina IA conductual conductual, firewall neuronal y análisis YARA de grado militar para proteger tus equipos en tiempo real.
          </p>
          
          <div className="flex flex-wrap gap-4 pt-4 stagger-2 animate-slide-up opacity-0 fill-mode-forwards">
            <Link to="/download">
              <Button size="lg" className="h-14 px-8 bg-gradient-to-r from-primary to-accent text-primary-foreground shadow-[var(--shadow-glow)] hover:scale-105 transition-premium group">
                <Download className="h-5 w-5 mr-2 group-hover:animate-bounce" /> 
                Descargar para {getOSName() || "tu sistema"}
              </Button>
            </Link>
            <Link to="/features">
              <Button size="lg" variant="outline" className="h-14 px-8 hover:bg-primary/5 transition-premium">
                Ver funciones
              </Button>
            </Link>
          </div>
          
          <div className="flex items-center gap-8 pt-6 text-muted-foreground/60 text-xs font-medium uppercase tracking-widest stagger-3 animate-fade-in opacity-0 fill-mode-forwards">
            <span className={`flex items-center gap-2 transition-colors ${os === "windows" ? "text-primary opacity-100" : ""}`}>
              <Monitor className="h-4 w-4" /> Windows
            </span>
            <span className={`flex items-center gap-2 transition-colors ${os === "macos" ? "text-primary opacity-100" : ""}`}>
              <Apple className="h-4 w-4" /> macOS
            </span>
            <span className={`flex items-center gap-2 transition-colors ${os === "linux" ? "text-primary opacity-100" : ""}`}>
              <span className="text-base">🐧</span> Linux
            </span>
          </div>
        </div>
        
        <div className="relative lg:block stagger-2 animate-fade-in opacity-0 fill-mode-forwards hidden">
          <div className="absolute inset-0 blur-[120px] bg-primary/30 rounded-full animate-glow-pulse" />
          <div className="relative animate-float">
            <div className="absolute -inset-1 bg-gradient-to-br from-primary/50 to-accent/50 rounded-3xl blur opacity-30" />
            <img 
              src={heroShield} 
              alt="Peralta Shield Logo Official" 
              className="relative rounded-3xl object-contain h-[500px] w-auto drop-shadow-[0_0_50px_rgba(34,197,94,0.3)] hover:scale-105 transition-premium" 
            />
            {/* Trust Badges */}
            <div className="absolute -bottom-6 -left-6 bg-background/80 backdrop-blur-md border border-border p-4 rounded-2xl shadow-xl flex items-center gap-3 animate-slide-up stagger-4">
              <ShieldCheck className="h-8 w-8 text-primary" />
              <div>
                <p className="text-xs font-bold uppercase tracking-tighter">Certificación</p>
                <p className="text-sm font-medium text-muted-foreground">Neural Guard V3</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}