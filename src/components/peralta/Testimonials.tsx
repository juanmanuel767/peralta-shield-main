import { Star, Quote } from "lucide-react";
import { testimonials as allReviews } from "@/data/testimonials";

export function Testimonials() {
  // Dividir los testimonios en dos grupos para dos filas de scroll opuestas
  const row1 = allReviews.slice(0, 48);
  const row2 = allReviews.slice(48, 95);

  return (
    <section className="py-24 bg-card/5 overflow-hidden border-y border-border/50">
      <div className="container mx-auto px-6 text-center mb-16">
        <h2 className="text-4xl font-bold mb-4">Masa Crítica de Usuarios</h2>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Únete a la creciente comunidad de Peralta Antivirus. Seguridad validada por miles de usuarios.
        </p>
      </div>

      <div className="flex flex-col gap-8">
        {/* Fila 1: Derecha a Izquierda */}
        <div className="flex overflow-hidden group">
          <div className="flex animate-marquee-slow group-hover:pause gap-6 px-3">
            {[...row1, ...row1].map((r, i) => (
              <TestimonialCard key={`${i}`} r={r} />
            ))}
          </div>
        </div>

        {/* Fila 2: Izquierda a Derecha */}
        <div className="flex overflow-hidden group">
          <div className="flex animate-marquee-reverse-slow group-hover:pause gap-6 px-3">
            {[...row2, ...row2].map((r, i) => (
              <TestimonialCard key={`${i}`} r={r} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function TestimonialCard({ r }: { r: any }) {
  return (
    <div className="w-[350px] flex-shrink-0 p-6 rounded-2xl border border-border bg-background/50 backdrop-blur-sm relative group hover:border-primary/40 transition-premium">
      <Quote className="absolute top-4 right-6 h-8 w-8 text-primary/5 group-hover:text-primary/10 transition-colors" />
      <div className="flex gap-1 mb-3">
        {[...Array(5)].map((_, i) => (
          <Star key={i} className="h-3 w-3 fill-primary text-primary" />
        ))}
      </div>
      <p className="text-sm text-balance italic mb-4 leading-relaxed line-clamp-3 italic">"{r.text}"</p>
      <div className="flex items-center gap-3">
        <div className="h-8 w-8 rounded-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center text-[10px] font-bold border border-primary/20">
          {r.name.charAt(0)}
        </div>
        <div>
          <p className="text-sm font-bold leading-tight">{r.name}</p>
          <p className="text-[10px] text-primary/70 uppercase tracking-tighter">{r.role} · {r.platform}</p>
        </div>
      </div>
    </div>
  );
}
