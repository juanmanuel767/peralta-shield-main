import { Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import { ShieldCheck, Monitor, Apple, Terminal } from "lucide-react";

export function CTA() {
  return (
    <section className="container mx-auto px-6 py-24 mb-12">
      <div className="relative rounded-[3rem] border border-primary/30 p-12 md:p-24 text-center overflow-hidden group" style={{ background: "var(--gradient-card)" }}>
        <div className="absolute inset-0 opacity-10 group-hover:opacity-20 transition-premium" style={{ background: "var(--gradient-hero)" }} />
        
        <div className="relative z-10">
          <h2 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6 font-display">Protege tu mundo digital hoy</h2>
          <p className="text-xl text-muted-foreground mt-4 max-w-2xl mx-auto leading-relaxed">
            Únete a miles de usuarios que ya confían en la seguridad neuronal de Peralta. Gratis, ligero y de código abierto.
          </p>
          
          <Link to="/download" className="inline-block mt-12">
            <Button size="lg" className="h-16 px-12 text-lg bg-gradient-to-r from-primary to-accent text-primary-foreground shadow-[var(--shadow-glow)] hover:scale-105 transition-premium group">
              <ShieldCheck className="h-6 w-6 mr-3 group-hover:rotate-12 transition-transform" /> 
              Descargar Peralta Antivirus
            </Button>
          </Link>

          <div className="mt-16 flex justify-center items-center gap-10 md:gap-16 opacity-40 hover:opacity-80 transition-opacity">
            <div className="flex flex-col items-center gap-2">
              <Monitor className="h-6 w-6" />
              <span className="text-[10px] font-bold uppercase tracking-widest">Windows</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <Apple className="h-6 w-6" />
              <span className="text-[10px] font-bold uppercase tracking-widest">macOS</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <Terminal className="h-6 w-6" />
              <span className="text-[10px] font-bold uppercase tracking-widest">Linux</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
