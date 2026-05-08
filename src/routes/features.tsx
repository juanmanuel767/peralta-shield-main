import { createFileRoute } from "@tanstack/react-router";
import { Layout } from "@/components/peralta/Layout";
import { FeatureGrid } from "@/components/peralta/FeatureGrid";
import { CTA } from "@/components/peralta/CTA";
import { Check, X, Shield, Zap, Lock, Globe } from "lucide-react";

export const Route = createFileRoute("/features")({
  head: () => ({
    meta: [
      { title: "Funciones — Peralta Antivirus" },
      { name: "description", content: "Descubre los 8 módulos de seguridad de Peralta: IA conductual, firewall neuronal, YARA, análisis de binarios y más." },
    ],
  }),
  component: FeaturesPage,
});

function FeaturesPage() {
  return (
    <Layout>
      <div className="container mx-auto px-6 pt-32 pb-16 text-center animate-slide-up">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-primary/20 bg-primary/5 text-primary text-xs font-bold uppercase mb-6">
          Tecnología de Vanguardia
        </div>
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight font-display mb-6">Funciones que protegen de verdad</h1>
        <p className="text-muted-foreground max-w-2xl mx-auto text-xl leading-relaxed">
          Cada módulo de Peralta ha sido diseñado para neutralizar las amenazas más sofisticadas antes de que toquen tu sistema.
        </p>
      </div>

      <FeatureGrid />

      {/* Comparison Section */}
      <section className="container mx-auto px-6 py-24 border-y border-border/40">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4 font-display">Simplemente Mejor</h2>
          <p className="text-muted-foreground">Compara Peralta con las soluciones tradicionales.</p>
        </div>

        <div className="max-w-4xl mx-auto overflow-hidden rounded-3xl border border-border bg-card/20 backdrop-blur-sm shadow-xl">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-muted/50 border-b border-border">
                <th className="p-6 font-bold">Capacidad</th>
                <th className="p-6 font-bold text-primary">Peralta</th>
                <th className="p-6 font-bold text-muted-foreground">Tradicionales</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/50 text-sm">
              {[
                { f: "IA Conductual (Sin firmas)", p: true, t: false },
                { f: "Firewall Neuronal", p: true, t: false },
                { f: "Código Abierto & Verificable", p: true, t: false },
                { f: "Instalación en 1-Click", p: true, t: true },
                { f: "Impacto en CPU < 1%", p: true, t: false },
                { f: "Privacidad Total (Sin Telemetría)", p: true, t: false },
              ].map((row, i) => (
                <tr key={i} className="hover:bg-muted/20 transition-colors">
                  <td className="p-6 font-medium">{row.f}</td>
                  <td className="p-6"><Check className="text-primary h-5 w-5" /></td>
                  <td className="p-6">{row.t ? <Check className="text-muted-foreground h-5 w-5" /> : <X className="text-destructive/50 h-5 w-5" />}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Workflow Section */}
      <section className="container mx-auto px-6 py-24">
        <div className="grid md:grid-cols-2 gap-16 items-center">
          <div className="space-y-8">
            <h2 className="text-4xl font-bold font-display leading-tight">Privacidad por diseño,<br />Vigilancia por IA.</h2>
            <div className="space-y-6">
              {[
                { icon: Shield, t: "Protección Offline", d: "No necesitas estar conectado para que nuestra IA detecte amenazas." },
                { icon: Zap, t: "Rápido como la luz", d: "Escaneo ultrarrápido que no ralentiza tu flujo de trabajo." },
                { icon: Lock, t: "Cero Logs", d: "Tus datos nunca salen de tu máquina. El análisis es 100% local." },
                { icon: Globe, t: "Multiplataforma", d: "Misma experiencia pro en Windows, macOS y Linux." },
              ].map((item, i) => (
                <div key={i} className="flex gap-4">
                  <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
                    <item.icon className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h4 className="font-bold mb-1">{item.t}</h4>
                    <p className="text-sm text-muted-foreground">{item.d}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="relative">
             <div className="absolute inset-0 blur-[100px] bg-primary/20 rounded-full" />
             <div className="relative rounded-3xl border border-border p-1 bg-gradient-to-br from-border/50 to-transparent">
               <div className="bg-background rounded-[1.4rem] p-8 aspect-square flex items-center justify-center">
                 <Shield className="h-48 w-48 text-primary/20 animate-pulse" />
                 <div className="absolute inset-0 flex items-center justify-center">
                   <div className="h-24 w-24 rounded-full border-2 border-primary/50 animate-ping" />
                 </div>
               </div>
             </div>
          </div>
        </div>
      </section>

      <CTA />
    </Layout>
  );
}