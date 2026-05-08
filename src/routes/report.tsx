import { createFileRoute } from '@tanstack/react-router';
import { Shield, AlertCircle, Terminal, Info, ChevronRight, Download, Share2, Printer, XCircle } from 'lucide-react';
import { useState, useEffect } from 'react';

export const Route = createFileRoute('/report')({
  component: ThreatReport,
});

function ThreatReport() {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Mock data para demo web
  useEffect(() => {
    setReport({
      nombre: 'real_threat_test.py',
      estado: 'AMENAZA CRÍTICA',
      nivel: 'ALTO',
      tipo: 'Reverse Shell / Backdoor',
      ia_analisis: {
        veredicto: 'MALICIOSO',
        confianza: 98,
        descripcion: 'Este archivo intentó establecer una conexión remota no autorizada a una IP externa y otorgar control total de la terminal (bash). Detectado y bloqueado por Peralta Neural Sandbox.',
        acciones: ['Conexión a /dev/tcp bloqueada', 'Intento de pty.spawn interceptado', 'Redirección de descriptores de archivo denegada'],
        recomendacion: 'Mantenga este archivo en cuarentena virtual. Esta demostración refleja cómo el Antivirus instalado localmente intercepta ejecuciones de scripts letales en memoria.'
      },
      timestamp: new Date().toLocaleString(),
      ruta: '/home/user/descargas/script_sospechoso.py'
    });
    setLoading(false);
  }, []);

  if (loading) return <div className="min-h-screen bg-[#05070a] flex items-center justify-center"><div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div></div>;

  return (
    <div className="min-h-screen bg-[#05070a] text-white pt-28 pb-20 px-4 md:px-8 font-['Space_Grotesk'] overflow-x-hidden">
      <div className="max-w-4xl mx-auto">
        
        {/* Banner de Peligro */}
        <div className="relative p-1 rounded-[2.5rem] bg-gradient-to-r from-red-600 via-purple-600 to-red-600 animate-gradient-x mb-12 shadow-2xl shadow-red-900/20">
          <div className="bg-[#0b0d12] rounded-[2.4rem] p-8 md:p-12">
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="w-24 h-24 md:w-32 md:h-32 bg-red-500/10 rounded-full flex items-center justify-center border border-red-500/20 shadow-[0_0_50px_rgba(239,68,68,0.2)]">
                <AlertCircle className="w-12 h-12 md:w-16 md:h-16 text-red-500 animate-pulse" />
              </div>
              <div className="text-center md:text-left flex-1">
                <div className="inline-block px-4 py-1 bg-red-500/20 border border-red-500/30 rounded-full text-red-400 text-xs font-bold tracking-widest uppercase mb-4">
                   Amenaza Neutralizada por Peralta Neural
                </div>
                <h1 className="text-3xl md:text-5xl font-black mb-2 tracking-tight">
                  {report.nombre}
                </h1>
                <p className="text-gray-500 font-mono text-sm break-all">{report.ruta}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Columna Izquierda: Análisis IA */}
          <div className="md:col-span-2 space-y-8">
            <section className="bg-white/5 border border-white/10 rounded-[2rem] p-8 backdrop-blur-xl relative overflow-hidden">
              <div className="absolute top-0 right-0 p-6 opacity-10">
                <Shield className="w-24 h-24 text-blue-500" />
              </div>
              <h2 className="text-xl font-bold mb-6 flex items-center gap-3 text-blue-400">
                <Terminal className="w-5 h-5" /> Análisis del Cerebro IA (Llama 3.2)
              </h2>
              <div className="bg-black/40 rounded-2xl p-6 border border-white/5 mb-6 leading-relaxed text-gray-300">
                "{report.ia_analisis.descripcion}"
              </div>
              <div className="space-y-3">
                <p className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-4">Indicadores de Compromiso (IoC):</p>
                {report.ia_analisis.acciones.map((accion: string, i: number) => (
                  <div key={i} className="flex items-center gap-3 text-sm text-gray-400 group">
                    <ChevronRight className="w-4 h-4 text-purple-500 group-hover:translate-x-1 transition-transform" />
                    <span className="font-mono bg-white/5 px-2 py-0.5 rounded border border-white/5">{accion}</span>
                  </div>
                ))}
              </div>
            </section>

            <section className="bg-gradient-to-br from-blue-600/20 to-purple-600/20 border border-blue-500/30 rounded-[2rem] p-8 backdrop-blur-xl shadow-xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-3 text-white">
                <Info className="w-5 h-5" /> Recomendación de Seguridad
              </h2>
              <p className="text-blue-100 leading-relaxed mb-6">
                {report.ia_analisis.recomendacion}
              </p>
              <div className="grid grid-cols-2 gap-4">
                <button className="flex items-center justify-center gap-2 py-3 bg-red-600 hover:bg-red-700 rounded-xl font-bold transition-all">
                  <XCircle className="w-4 h-4" /> Eliminar Seguro
                </button>
                <button className="flex items-center justify-center gap-2 py-3 bg-white/10 hover:bg-white/20 rounded-xl font-bold transition-all border border-white/10">
                  <Download className="w-4 h-4" /> Investigar Más
                </button>
              </div>
            </section>
          </div>

          {/* Columna Derecha: Stats */}
          <div className="space-y-8">
            <div className="bg-white/5 border border-white/10 rounded-[2rem] p-6 text-center">
              <div className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Confianza de IA</div>
              <div className="relative inline-block mb-4">
                <svg className="w-32 h-32">
                  <circle className="text-white/5" strokeWidth="8" stroke="currentColor" fill="transparent" r="58" cx="64" cy="64" />
                  <circle className="text-blue-500" strokeWidth="8" strokeDasharray={364} strokeDashoffset={364 - (364 * report.ia_analisis.confianza) / 100} strokeLinecap="round" stroke="currentColor" fill="transparent" r="58" cx="64" cy="64" />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center text-3xl font-black">{report.ia_analisis.confianza}%</div>
              </div>
              <div className="text-blue-400 font-bold">Veredicto {report.ia_analisis.veredicto}</div>
            </div>

            <div className="bg-white/5 border border-white/10 rounded-[2rem] p-6 space-y-4">
              <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2">
                <span className="text-gray-500">Fecha</span>
                <span className="text-gray-300">{report.timestamp.split(',')[0]}</span>
              </div>
              <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2">
                <span className="text-gray-500">Hora</span>
                <span className="text-gray-300">{report.timestamp.split(',')[1]}</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-500">Nivel Mortal</span>
                <span className="text-red-500 font-bold">{report.nivel}</span>
              </div>
            </div>

            <div className="flex flex-col gap-3">
              <button className="flex items-center justify-center gap-3 p-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl transition-all">
                <Share2 className="w-4 h-4 text-gray-400" /> Exportar Reporte
              </button>
              <button className="flex items-center justify-center gap-3 p-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl transition-all">
                <Printer className="w-4 h-4 text-gray-400" /> Imprimir Análisis
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
