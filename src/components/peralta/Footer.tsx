import { Github, Twitter, MessageCircle } from "lucide-react";
import { Link } from "@tanstack/react-router";
import { DOWNLOAD_CONFIG } from "@/lib/download-config";

export function Footer() {
  return (
    <footer className="border-t border-border bg-card/20 pt-24 pb-12 overflow-hidden relative">
      {/* Decorative gradient blur */}
      <div className="absolute -bottom-24 left-1/2 -translate-x-1/2 w-full max-w-4xl h-48 bg-primary/10 blur-[100px] rounded-full" />
      
      <div className="container mx-auto px-6 relative z-10">
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-12 mb-16">
          <div className="col-span-2 lg:col-span-2">
            <Link to="/" className="flex items-center gap-2 mb-6">
              <img src="/logo-official.png" alt="Logo" className="h-8 w-8 object-contain" />
              <span className="font-bold text-xl tracking-tighter">Peralta Antivirus</span>
            </Link>
            <p className="text-muted-foreground text-sm max-w-xs leading-relaxed mb-8">
              Protección neuronal de código abierto para la era moderna. Construido con pasión para asegurar tu libertad digital en Linux, Windows y macOS.
            </p>
            <div className="flex items-center gap-4">
              <a href="#" className="h-9 w-9 rounded-full bg-muted flex items-center justify-center hover:bg-primary hover:text-primary-foreground transition-premium">
                <Twitter className="h-4 w-4" />
              </a>
              <a href="#" className="h-9 w-9 rounded-full bg-muted flex items-center justify-center hover:bg-primary hover:text-primary-foreground transition-premium">
                <Github className="h-4 w-4" />
              </a>
              <a href="#" className="h-9 w-9 rounded-full bg-muted flex items-center justify-center hover:bg-primary hover:text-primary-foreground transition-premium">
                <MessageCircle className="h-4 w-4" />
              </a>
            </div>
          </div>

          <div>
            <h4 className="font-bold text-sm uppercase tracking-widest mb-6">Producto</h4>
            <ul className="space-y-4 text-sm text-muted-foreground">
              <li><Link to="/download" className="hover:text-primary transition-colors">Descarga</Link></li>
              <li><Link to="/features" className="hover:text-primary transition-colors">Funciones</Link></li>
              <li><Link to="/community" className="hover:text-primary transition-colors">Comunidad</Link></li>
              <li><a href="#" className="hover:text-primary transition-colors">Changelog</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-sm uppercase tracking-widest mb-6">Recursos</h4>
            <ul className="space-y-4 text-sm text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">Documentación</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Soporte</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">GitHub Releases</a></li>
              <li><Link to="/about" className="hover:text-primary transition-colors">Sobre Peralta</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-sm uppercase tracking-widest mb-6">Legal</h4>
            <ul className="space-y-4 text-sm text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">Privacidad</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Términos</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Licencia MIT</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Cookies</a></li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-border flex flex-col md:flex-row items-center justify-between gap-6 text-xs text-muted-foreground">
          <div className="flex items-center gap-2">
            <span>Peralta Antivirus © {new Date().getFullYear()}</span>
            <span className="h-1 w-1 rounded-full bg-border" />
            <span>Versión {DOWNLOAD_CONFIG.version}</span>
          </div>
          <p>Hecho por <span className="text-foreground font-semibold">Juan Manuel Peralta</span> — Estudiante de Ingeniería — con ❤️ para el mundo.</p>
        </div>
      </div>
    </footer>
  );
}