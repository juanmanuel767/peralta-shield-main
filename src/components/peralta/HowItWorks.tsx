import { Download, Settings, ShieldCheck } from "lucide-react";

export function HowItWorks() {
  const steps = [
    {
      icon: Download,
      title: "Descarga",
      desc: "Obtén el instalador optimizado para tu sistema operativo en segundos.",
      color: "from-blue-500 to-cyan-400"
    },
    {
      icon: Settings,
      title: "Configura",
      desc: "Instalación en un click. Sin configuraciones complejas ni pasos innecesarios.",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: ShieldCheck,
      title: "Protegido",
      desc: "Peralta comienza a vigilar tu sistema con IA neuronal al instante.",
      color: "from-emerald-500 to-teal-400"
    },
  ];

  return (
    <section className="container mx-auto px-6 py-24 relative overflow-hidden">
      <div className="text-center max-w-2xl mx-auto mb-16">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Protección en 3 pasos</h2>
        <p className="text-muted-foreground text-lg">Peralta está diseñado para ser potente por dentro y simple por fuera.</p>
      </div>

      <div className="grid md:grid-cols-3 gap-12 relative">
        {/* Connection line for desktop */}
        <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-border to-transparent -translate-y-1/2 z-0" />
        
        {steps.map((s, i) => (
          <div key={s.title} className="relative z-10 flex flex-col items-center text-center group">
            <div className={`h-20 w-20 rounded-2xl bg-gradient-to-br ${s.color} p-0.5 shadow-lg mb-6 group-hover:scale-110 transition-premium`}>
              <div className="h-full w-full rounded-2xl bg-background flex items-center justify-center">
                <s.icon className="h-10 w-10 text-foreground" />
              </div>
            </div>
            <div className="absolute -top-4 right-1/2 translate-x-12 h-8 w-8 rounded-full bg-muted border border-border flex items-center justify-center text-sm font-bold shadow-sm">
              {i + 1}
            </div>
            <h3 className="text-2xl font-bold mb-3">{s.title}</h3>
            <p className="text-muted-foreground leading-relaxed">{s.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
