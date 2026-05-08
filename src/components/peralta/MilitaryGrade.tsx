import { Shield, Lock, Fingerprint, Radar, Eye, Zap, ShieldCheck, ServerCrash } from "lucide-react";
import { useEffect, useState, useRef } from "react";

const certifications = [
  { icon: Shield, label: "Cifrado AES-256", desc: "Estándar utilizado por la NSA para proteger información clasificada TOP SECRET." },
  { icon: Lock, label: "Sandbox Neuronal", desc: "Aislamiento de procesos en capas virtualizadas con análisis de comportamiento en tiempo real." },
  { icon: Fingerprint, label: "Firmas YARA Militares", desc: "Motor de detección basado en patrones de amenazas usados por agencias de inteligencia globales." },
  { icon: Radar, label: "IDS/IPS Integrado", desc: "Sistema de detección y prevención de intrusiones con análisis de tráfico en capa 7." },
  { icon: Eye, label: "Análisis Heurístico", desc: "IA conductual que detecta malware de día cero sin depender de firmas conocidas." },
  { icon: ServerCrash, label: "Anti-Exfiltración", desc: "Bloqueo automático de conexiones salientes sospechosas y túneles encubiertos." },
];

const threatStats = [
  { value: "AES-256", label: "CIFRADO MILITAR" },
  { value: "0-Day", label: "DETECCIÓN PROACTIVA" },
  { value: "Layer 7", label: "INSPECCIÓN PROFUNDA" },
  { value: "24/7", label: "VIGILANCIA ACTIVA" },
];

export function MilitaryGrade() {
  const [visible, setVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) setVisible(true);
    }, { threshold: 0.1 });
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <section ref={ref} className="relative py-24 md:py-32 overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-red-950/5 to-background" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-red-500/5 rounded-full blur-[150px]" />
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-red-500/30 to-transparent" />
      <div className="absolute bottom-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-red-500/30 to-transparent" />

      <div className="container mx-auto px-6 relative z-10">
        {/* Header */}
        <div className={`text-center mb-20 transition-all duration-1000 ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}>
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-bold uppercase tracking-[0.2em] mb-6">
            <ShieldCheck className="h-4 w-4" />
            Clasificación de Seguridad
          </div>
          <h2 className="text-4xl md:text-6xl font-bold font-display tracking-tight mb-6">
            Protección de{" "}
            <span className="bg-gradient-to-r from-red-500 via-orange-400 to-red-600 bg-clip-text text-transparent">
              Grado Militar
            </span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Peralta Antivirus implementa los mismos estándares de cifrado y detección que utilizan 
            las agencias de defensa más avanzadas del mundo. Tu equipo merece protección de élite.
          </p>
        </div>

        {/* Stats bar */}
        <div className={`grid grid-cols-2 lg:grid-cols-4 gap-4 mb-16 transition-all duration-1000 delay-200 ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}>
          {threatStats.map((stat, i) => (
            <div key={stat.label} className="relative group">
              <div className="absolute inset-0 bg-gradient-to-r from-red-500/10 to-orange-500/10 rounded-2xl blur-xl group-hover:blur-2xl opacity-0 group-hover:opacity-100 transition-all duration-500" />
              <div className="relative p-6 rounded-2xl border border-red-500/10 bg-card/30 backdrop-blur-sm text-center hover:border-red-500/30 transition-all duration-300">
                <div className="text-2xl md:text-3xl font-bold text-red-400 font-display">{stat.value}</div>
                <div className="text-[10px] font-bold uppercase tracking-[0.2em] text-muted-foreground mt-2">{stat.label}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Certification Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {certifications.map((cert, i) => (
            <div
              key={cert.label}
              className={`group relative transition-all duration-700 ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}
              style={{ transitionDelay: `${300 + i * 100}ms` }}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-red-500/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative p-8 rounded-2xl border border-border/50 bg-card/20 backdrop-blur-sm hover:border-red-500/20 transition-all duration-300 h-full">
                <div className="flex items-start gap-5">
                  <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-red-500/20 to-orange-500/10 flex items-center justify-center shrink-0 border border-red-500/10 group-hover:shadow-[0_0_20px_-3px_rgba(239,68,68,0.3)] transition-all duration-300">
                    <cert.icon className="h-6 w-6 text-red-400" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg mb-2 group-hover:text-red-400 transition-colors duration-300">{cert.label}</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">{cert.desc}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom classified banner */}
        <div className={`mt-16 text-center transition-all duration-1000 delay-700 ${visible ? "opacity-100" : "opacity-0"}`}>
          <div className="inline-flex items-center gap-3 px-8 py-4 rounded-2xl bg-red-500/5 border border-red-500/10">
            <div className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
            <span className="text-sm font-mono text-red-400/80 tracking-wider">
              NIVEL DE PROTECCIÓN: <span className="font-bold text-red-400">MÁXIMO</span> — MOTOR NEURONAL v3.2 ACTIVO
            </span>
            <div className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
          </div>
        </div>
      </div>
    </section>
  );
}
