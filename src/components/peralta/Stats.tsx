import { useEffect, useState, useRef } from "react";

export function Stats() {
  const [visible, setVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const stats = [
    { v: 99.7, l: "Tasa de detección", suffix: "%" },
    { v: 0.1, l: "Falsos positivos", prefix: "<", suffix: "%" },
    { v: 8, l: "Módulos de seguridad" },
    { v: 3, l: "Sistemas operativos" },
  ];

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) setVisible(true);
    }, { threshold: 0.1 });
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <section ref={ref} className="border-y border-border/40 bg-gradient-to-b from-card/30 to-background py-16">
      <div className="container mx-auto px-6 grid grid-cols-2 lg:grid-cols-4 gap-12">
        {stats.map((s, i) => (
          <div key={s.l} className={`text-center transition-premium delay-[${i * 100}ms] ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}>
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
