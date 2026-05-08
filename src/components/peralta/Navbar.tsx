import { Link } from "@tanstack/react-router";
import { LogOut, Menu, X, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/useAuth";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";
import { useState, useEffect } from "react";

export function Navbar() {
  const { user } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header className={`sticky top-0 z-50 transition-premium ${scrolled ? "bg-background/80 backdrop-blur-xl border-b border-border shadow-sm" : "bg-transparent"}`}>
      <div className="container mx-auto flex items-center justify-between px-6 py-4">
        <Link to="/" className="flex items-center gap-2 group" onClick={() => setIsOpen(false)}>
          <div className="relative h-10 w-10">
            <img src="/logo-official.png" alt="Peralta Shield Logo" className="h-full w-full object-contain transition-transform group-hover:scale-110" />
            <div className="absolute inset-0 blur-lg bg-primary/40 opacity-0 group-hover:opacity-100 transition-opacity" />
          </div>
          <span className="font-bold text-xl tracking-tight font-display">Peralta</span>
        </Link>
        
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium">
          <Link to="/" activeOptions={{ exact: true }} className="text-muted-foreground hover:text-foreground transition-colors" activeProps={{ className: "text-foreground" }}>Inicio</Link>
          <Link to="/features" className="text-muted-foreground hover:text-foreground transition-colors" activeProps={{ className: "text-foreground" }}>Funciones</Link>
          <Link to="/about" className="text-muted-foreground hover:text-foreground transition-colors" activeProps={{ className: "text-foreground" }}>Sobre</Link>
          <Link to="/community" className="text-muted-foreground hover:text-foreground transition-colors" activeProps={{ className: "text-foreground" }}>Comunidad</Link>
        </nav>

        <div className="flex items-center gap-3">
          <Link to="/download" className="hidden sm:block">
            <Button variant="ghost" size="sm" className="gap-2">
              <Download className="h-4 w-4" /> Descargar
            </Button>
          </Link>
          
          {user ? (
            <Button variant="outline" size="sm" className="hidden md:flex gap-2" onClick={async () => { await supabase.auth.signOut(); toast.success("Sesión cerrada"); }}>
              <LogOut className="h-4 w-4" /> Salir
            </Button>
          ) : (
            <Link to="/auth" className="hidden md:block">
              <Button size="sm" className="bg-gradient-to-r from-primary to-accent text-primary-foreground hover:opacity-90 shadow-[var(--shadow-glow)]">Entrar</Button>
            </Link>
          )}

          <button className="md:hidden p-2 text-foreground" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <div className={`md:hidden absolute top-full left-0 w-full bg-background/95 backdrop-blur-xl border-b border-border transition-premium overflow-hidden ${isOpen ? "max-h-[400px] opacity-100 py-6" : "max-h-0 opacity-0 py-0"}`}>
        <nav className="flex flex-col items-center gap-6 text-lg font-medium">
          <Link to="/" activeOptions={{ exact: true }} onClick={() => setIsOpen(false)} className="text-muted-foreground hover:text-foreground" activeProps={{ className: "text-foreground" }}>Inicio</Link>
          <Link to="/features" onClick={() => setIsOpen(false)} className="text-muted-foreground hover:text-foreground" activeProps={{ className: "text-foreground" }}>Funciones</Link>
          <Link to="/about" onClick={() => setIsOpen(false)} className="text-muted-foreground hover:text-foreground" activeProps={{ className: "text-foreground" }}>Sobre</Link>
          <Link to="/community" onClick={() => setIsOpen(false)} className="text-muted-foreground hover:text-foreground" activeProps={{ className: "text-foreground" }}>Comunidad</Link>
          <Link to="/download" onClick={() => setIsOpen(false)} className="text-primary font-bold flex items-center gap-2">
            <Download className="h-5 w-5" /> Descargar Antivirus
          </Link>
          {!user && (
            <Link to="/auth" onClick={() => setIsOpen(false)}>
              <Button className="w-48 bg-gradient-to-r from-primary to-accent">Entrar / Registro</Button>
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
}