import { createFileRoute } from "@tanstack/react-router";
import { Layout } from "@/components/peralta/Layout";
import { ShieldCheck, Code, Heart, Layers, Cpu, Database, Cloud } from "lucide-react";
import { CTA } from "@/components/peralta/CTA";

export const Route = createFileRoute("/about")({
  head: () => ({
    meta: [
      { title: "Sobre nosotros — Peralta Antivirus" },
      { name: "description", content: "Conoce a Juan Manuel Peralta y la misión detrás del antivirus más personal y transparente." },
    ],
  }),
  component: AboutPage,
});

function AboutPage() {
  return (
    <Layout>
      <section className="container mx-auto px-6 pt-32 pb-24 max-w-5xl animate-slide-up">
        <h1 className="text-6xl md:text-8xl font-bold tracking-tighter mb-8 font-display">La Misión Peralta.</h1>
        <p className="text-2xl text-muted-foreground leading-relaxed max-w-3xl">
          Nacimos para demostrar que la ciberseguridad puede ser potente, transparente y estar al alcance de todos. Sin cajas negras, sin telemetría invasiva.
        </p>
        
        <div className="grid md:grid-cols-3 gap-6 mt-20">
          {[
            { icon: ShieldCheck, t: "Misión", d: "Democratizar la seguridad de grado militar para el usuario común.", color: "bg-blue-500/10 text-blue-400" },
            { icon: Code, t: "Transparencia", d: "Código abierto para que sepas exactamente qué corre en tu máquina.", color: "bg-purple-500/10 text-purple-400" },
            { icon: Heart, t: "Privacidad", d: "Tus datos son sagrados. No recolectamos lo que no necesitamos.", color: "bg-emerald-500/10 text-emerald-400" },
          ].map((c) => (
            <div key={c.t} className="p-8 rounded-[2.5rem] border border-border bg-card/20 shadow-sm hover:shadow-xl transition-premium group">
              <div className={`h-12 w-12 rounded-xl ${c.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                <c.icon className="h-6 w-6" />
              </div>
              <h3 className="font-bold text-xl mb-3">{c.t}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{c.d}</p>
            </div>
          ))}
        </div>

        {/* Story Section */}
        <div className="mt-32 grid lg:grid-cols-2 gap-20 items-center">
          <div className="space-y-8">
            <h2 className="text-4xl font-bold font-display">Nuestra Historia</h2>
            <div className="space-y-10 relative">
              <div className="absolute left-2.5 top-2 bottom-2 w-px bg-gradient-to-b from-primary to-transparent" />
              {[
                { year: "2023", t: "El Concepto", d: "Juan Manuel Peralta comienza a experimentar con motores YARA locales." },
                { year: "2024", t: "Fase Beta", d: "Lanzamiento privado para entornos Linux críticos." },
                { year: "2025", t: "Expansión", d: "Peralta se vuelve multiplataforma con el motor neuronal V3." },
              ].map((step, i) => (
                <div key={i} className="relative pl-10 group">
                  <div className="absolute left-0 top-1 h-5 w-5 rounded-full border-2 border-primary bg-background group-hover:bg-primary transition-colors" />
                  <span className="text-xs font-bold text-primary tracking-widest">{step.year}</span>
                  <h4 className="text-xl font-bold mt-1">{step.t}</h4>
                  <p className="text-muted-foreground text-sm mt-2">{step.d}</p>
                </div>
              ))}
            </div>
          </div>
          
          <div className="p-10 md:p-14 rounded-[3rem] border border-primary/20 bg-gradient-to-br from-primary/5 to-accent/5 relative">
            <div className="flex items-center gap-6 mb-8">
              <div className="h-20 w-20 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-3xl font-bold text-primary-foreground shadow-2xl">
                JMP
              </div>
              <div>
                <h2 className="text-3xl font-bold">Juan Manuel Peralta</h2>
                <p className="text-primary font-bold text-sm tracking-widest uppercase">Fundador & CTO — Estudiante de Ingeniería</p>
              </div>
            </div>
            <p className="text-muted-foreground leading-relaxed text-lg italic">
              "Peralta no es solo software; es una declaración de principios sobre la soberanía tecnológica. Queremos que el usuario recupere el control de su propia seguridad."
            </p>
          </div>
        </div>

        {/* Tech Stack */}
        <div className="mt-32 border-t border-border pt-20">
          <h3 className="text-2xl font-bold mb-12 text-center font-display">Potenciado por Tecnología Moderna</h3>
          <div className="flex flex-wrap justify-center gap-10 opacity-40 hover:opacity-100 transition-opacity">
            <div className="flex items-center gap-3"><Layers className="h-6 w-6" /> <span className="font-bold">React 19</span></div>
            <div className="flex items-center gap-3"><Cpu className="h-6 w-6" /> <span className="font-bold">AI Neuronal</span></div>
            <div className="flex items-center gap-3"><Database className="h-6 w-6" /> <span className="font-bold">Supabase</span></div>
            <div className="flex items-center gap-3"><Cloud className="h-6 w-6" /> <span className="font-bold">Edge Runtime</span></div>
          </div>
        </div>
      </section>
      <CTA />
    </Layout>
  );
}
