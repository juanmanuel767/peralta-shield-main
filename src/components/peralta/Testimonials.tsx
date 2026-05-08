import { Star, Quote } from "lucide-react";

export function Testimonials() {
  const reviews = [
    {
      name: "Andrés Silva",
      role: "Security Researcher",
      text: "La mejor interfaz que he visto en un antivirus para Linux. Potente y minimalista.",
      rating: 5,
      platform: "Linux"
    },
    {
      name: "Carla Méndez",
      role: "Freelance Designer",
      text: "Me encanta que no me molesta con popups innecesarios. Se siente muy premium.",
      rating: 5,
      platform: "macOS"
    },
    {
      name: "Roberto Gómez",
      role: "DevOps Engineer",
      text: "Detección YARA impecable. Es mi capa de seguridad principal ahora mismo.",
      rating: 5,
      platform: "Windows"
    }
  ];

  return (
    <section className="container mx-auto px-6 py-24 bg-card/10 border-y border-border/50">
      <div className="text-center mb-16">
        <h2 className="text-4xl font-bold mb-4">Confianza real de usuarios reales</h2>
        <div className="flex justify-center gap-1">
          {[1, 2, 3, 4, 5].map((n) => (
            <Star key={n} className="h-5 w-5 fill-primary text-primary" />
          ))}
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {reviews.map((r, i) => (
          <div key={i} className="p-8 rounded-3xl border border-border bg-background relative group hover:border-primary/40 transition-premium">
            <Quote className="absolute top-6 right-8 h-10 w-10 text-primary/10 group-hover:text-primary/20 transition-colors" />
            <div className="flex gap-1 mb-4">
              {[...Array(r.rating)].map((_, i) => (
                <Star key={i} className="h-4 w-4 fill-primary text-primary" />
              ))}
            </div>
            <p className="text-muted-foreground italic mb-6 leading-relaxed">"{r.text}"</p>
            <div>
              <p className="font-bold">{r.name}</p>
              <p className="text-xs text-primary/80 uppercase tracking-widest mt-1">{r.role} · {r.platform}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
