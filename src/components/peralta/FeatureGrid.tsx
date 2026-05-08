import { Brain, Network, Wifi, Usb, Eye, FileSearch, MessageSquareCode, ShieldAlert } from "lucide-react";

const features = [
  { icon: Brain, title: "IA Conductual", desc: "Vigilante puntúa cada proceso por su comportamiento real, no solo por firmas.", color: "text-blue-400" },
  { icon: Network, title: "Firewall Neuronal", desc: "Detecta C2 beaconing y túneles DNS antes de que se exfiltre tu información.", color: "text-purple-400" },
  { icon: ShieldAlert, title: "YARA Engine", desc: "7 reglas profesionales: Ransomware, RATs, Cryptominers, Webshells y Rootkits.", color: "text-red-400" },
  { icon: FileSearch, title: "Análisis de Binarios", desc: "Inspecciona ejecutables PE/ELF y detecta empaquetadores como UPX.", color: "text-emerald-400" },
  { icon: Wifi, title: "Protector WiFi", desc: "Alerta de ARP Spoofing y nuevos dispositivos conectados a tu red.", color: "text-orange-400" },
  { icon: Usb, title: "Monitor USB", desc: "Escaneo automático de cualquier dispositivo USB conectado.", color: "text-cyan-400" },
  { icon: Eye, title: "Privacidad Total", desc: "Te avisa cuando una app accede a tu cámara o micrófono.", color: "text-pink-400" },
  { icon: MessageSquareCode, title: "Asistente IA", desc: "Pregúntale a Peralta y obtén un análisis al instante.", color: "text-indigo-400" },
];

export function FeatureGrid() {
  return (
    <section className="container mx-auto px-6 py-24">
      <div className="text-center max-w-3xl mx-auto mb-20 animate-slide-up">
        <h2 className="text-4xl md:text-6xl font-bold tracking-tight font-display mb-6">Diseñado para amenazas modernas</h2>
        <p className="text-muted-foreground text-xl leading-relaxed">
          8 módulos de seguridad de grado empresarial trabajando en armonía perfecta.
        </p>
      </div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((f, i) => (
          <div 
            key={f.title} 
            className={`p-8 rounded-[2rem] border border-border bg-card/40 hover:bg-card hover:border-primary/50 transition-premium hover:-translate-y-2 hover:shadow-2xl group animate-slide-up stagger-${(i % 4) + 1} opacity-0 fill-mode-forwards`}
          >
            <div className={`h-14 w-14 rounded-2xl bg-muted/50 flex items-center justify-center mb-6 group-hover:bg-primary/20 transition-colors`}>
              <f.icon className={`h-8 w-8 ${f.color} transition-transform group-hover:scale-110`} />
            </div>
            <h3 className="font-bold text-xl mb-3 tracking-tight">{f.title}</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
