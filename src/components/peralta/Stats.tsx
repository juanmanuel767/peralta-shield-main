import { useEffect, useState, useRef } from "react";

export function Stats() {
  const [visible, setVisible] = useState(false);
  const [downloads, setDownloads] = useState(95);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) setVisible(true);
    }, { threshold: 0.1 });
    if (ref.current) observer.observe(ref.current);

    // Simular incremento de descargas cada 30-60 segundos
    const interval = setInterval(() => {
      setDownloads(prev => prev + 1);
    }, 45000);

    return () => {
      observer.disconnect();
      clearInterval(interval);
    };
  }, []);

  const stats = [
    { v: 99.7, l: "Tasa de detección", suffix: "%" },
    { v: downloads, l: "Descargas Activas", prefix: "+" },
    { v: 8, l: "Módulos de seguridad" },
    { v: 100, l: "Privacidad", suffix: "%" },
  ];

  return (
    <section ref={ref} className="border-y border-border/40 bg-gradient-to-b from-card/30 to-background py-16">
      <div className="container mx-auto px-6 grid grid-cols-2 lg:grid-cols-4 gap-12">
        {stats.map((s, i) => (
          <div key={s.l} className={`text-center transition-all duration-700 delay-[${i * 100}ms] ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}>
            <div className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-primary via-primary-glow to-accent bg-clip-text text-transparent font-display tracking-tighter">
              {s.prefix}{visible ? s.v : 0}{s.suffix}
            </div>
            <div className="text-sm font-semibold uppercase tracking-widest text-muted-foreground mt-3 opacity-60">{s.l}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
