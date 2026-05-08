import { createFileRoute, Link } from '@tanstack/react-router';
import { Shield, Activity, Lock, Zap, Cpu, Database, AlertTriangle, Play, RefreshCw, StopCircle, Terminal as TerminalIcon, Bot } from 'lucide-react';
import { useState, useEffect } from 'react';

export const Route = createFileRoute('/security')({
  component: SecurityDashboard,
});

function SecurityDashboard() {
  const [stats, setStats] = useState({
    status: 'PROTEGIDO',
    threats_blocked: 0,
    cpu_usage: '0%',
    neural_model: 'Cargando...',
    uptime: '99.9%',
    memory_usage: '0 GB'
  });
  const [logs, setLogs] = useState<any[]>([]);
  const [isScanning, setIsScanning] = useState(false);

  useEffect(() => {
    // Real-time Integration with Neural Daemon
    const fetchData = async () => {
      try {
        const statsRes = await fetch('http://localhost:5005/api/stats');
        if (statsRes.ok) {
          const data = await statsRes.json();
          setStats({
            status: data.estado || 'PROTEGIDO',
            threats_blocked: data.amenazas_bloqueadas || 0,
            cpu_usage: data.carga_motor || '0%',
            neural_model: data.motor_neural || 'Peralta v3.2',
            uptime: data.uptime || '99.9%',
            memory_usage: data.memoria_uso || '0 GB'
          });
        }

        const logsRes = await fetch('http://localhost:5005/api/logs');
        if (logsRes.ok) {
          const logsData = await logsRes.json();
          setLogs(logsData);
        }
      } catch (error) {
        // Fallback for Web Demo session
        setStats(prev => ({ ...prev, status: 'DEMO' }));
      }
    };
    
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleAction = async (action: string) => {
    try {
      if (action === 'scan') {
        setIsScanning(true);
        await fetch('http://localhost:5005/api/scan', { method: 'POST' });
        // Progress is handled by chat polling or logs
        setTimeout(() => setIsScanning(false), 5000);
      } else if (action === 'update') {
        await fetch('http://localhost:5005/api/update', { method: 'POST' });
      } else if (action === 'stop') {
        await fetch('http://localhost:5005/api/stop', { method: 'POST' });
      }
    } catch (error) {
      alert(`Acción '${action}' falló: El motor no responde.`);
    }
  };

  return (
    <div className="min-h-screen bg-[#020408] text-white pt-24 pb-12 px-4 md:px-8 font-['Space_Grotesk'] overflow-hidden">
      <div className="max-w-7xl mx-auto">
        {/* Header con Control de Estado */}
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-12 gap-8 bg-white/5 p-8 rounded-[2.5rem] border border-white/5 backdrop-blur-3xl shadow-2xl">
          <div className="flex items-center gap-6">
            <div className={`p-5 rounded-[1.5rem] ${stats.status === 'PROTEGIDO' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'} border border-current/30 shadow-lg`}>
              <Shield className="w-10 h-10" />
            </div>
            <div>
              <h1 className="text-4xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-white to-purple-400">
                Centro de Comando Neural
              </h1>
              <p className="text-gray-500 flex items-center gap-2 mt-1">
                <Database className="w-4 h-4" /> Sistema de Defensa Peralta v1.0 • <span className={stats.status === 'PROTEGIDO' ? 'text-green-500' : 'text-red-500'}>{stats.status}</span>
              </p>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-4 w-full lg:w-auto">
            <Link to="/chat" className="flex items-center gap-3 px-6 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl font-black transition-all hover:scale-[1.05] shadow-lg shadow-blue-500/20">
              <Bot className="w-5 h-5" />
              <span>Preguntar a IA</span>
            </Link>
            <ControlButton onClick={() => handleAction('scan')} active={isScanning} icon={<Play />} label={isScanning ? "Escaneando..." : "Iniciar Escaneo"} color="blue" />
            <ControlButton onClick={() => handleAction('update')} icon={<RefreshCw />} label="Actualizar" color="purple" />
            <ControlButton onClick={() => handleAction('stop')} icon={<StopCircle />} label="Detener" color="red" />
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <StatCard title="Amenazas Bloqueadas" value={stats.threats_blocked} icon={<Lock className="w-6 h-6 text-blue-400" />} color="blue" />
          <StatCard title="Carga del Cerebro IA" value={stats.cpu_usage} icon={<Cpu className="w-6 h-6 text-purple-400" />} color="purple" />
          <StatCard title="Modelo Neuronal" value={stats.neural_model} icon={<Zap className="w-6 h-6 text-yellow-400" />} color="yellow" />
          <StatCard title="Servicio Activo" value={stats.uptime} icon={<Activity className="w-6 h-6 text-green-400" />} color="green" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Live Engine Console */}
          <div className="lg:col-span-2 bg-[#05070a] border border-blue-900/20 rounded-[2rem] p-8 shadow-inner overflow-hidden flex flex-col h-[500px]">
            <h2 className="text-xl font-bold mb-6 flex items-center gap-3 text-blue-400">
              <TerminalIcon className="w-5 h-5" /> Consola del Motor Neural
            </h2>
            <div className="flex-1 bg-black/60 rounded-2xl p-6 font-mono text-sm overflow-y-auto space-y-2 border border-white/5 custom-scrollbar">
              {logs.length > 0 ? logs.map((log, i) => (
                <div key={i} className={`flex gap-4 ${log.type === 'warning' ? 'text-yellow-500' : log.type === 'error' ? 'text-red-500' : 'text-blue-300'}`}>
                  <span className="opacity-30">[{log.time}]</span>
                  <span className="flex-1">{log.msg}</span>
                </div>
              )) : (
                <div className="text-gray-600 animate-pulse">Esperando señales del núcleo...</div>
              )}
            </div>
          </div>

          {/* Quick Info & Security Health */}
          <div className="flex flex-col gap-6">
            <div className="bg-gradient-to-br from-blue-600 to-purple-800 rounded-[2rem] p-8 shadow-xl relative overflow-hidden group">
              <div className="absolute -right-8 -bottom-8 w-48 h-48 bg-white/10 rounded-full blur-3xl group-hover:scale-150 transition-transform duration-1000"></div>
              <h3 className="text-2xl font-bold mb-4">Salud del Sistema</h3>
              <div className="space-y-4 relative z-10">
                <HealthBar label="Escaneo de Apps" active />
                <HealthBar label="Protección Web" active />
                <HealthBar label="Monitor de Red" active />
                <HealthBar label="Detección de Intrusos" active />
              </div>
            </div>

            <div className="bg-white/5 border border-white/10 rounded-[2rem] p-8">
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <AlertTriangle className="text-yellow-500 w-5 h-5" /> Acción Requerida
              </h3>
              <p className="text-gray-400 text-sm mb-6 leading-relaxed">
                El sistema está operando normalmente. No se requieren acciones manuales en este momento.
              </p>
              <button className="w-full py-4 bg-white/10 hover:bg-white/20 rounded-xl font-bold transition-all border border-white/10">
                Optimizar Base de Datos
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ControlButton({ onClick, icon, label, color, active }: any) {
  const colors: any = {
    blue: 'bg-blue-600 hover:bg-blue-500 shadow-blue-500/20',
    purple: 'bg-purple-600 hover:bg-purple-500 shadow-purple-500/20',
    red: 'bg-red-600 hover:bg-red-500 shadow-red-500/20'
  };
  return (
    <button 
      onClick={onClick}
      className={`flex items-center gap-3 px-6 py-4 ${colors[color]} rounded-2xl font-black transition-all hover:scale-[1.05] active:scale-95 shadow-lg ${active ? 'animate-pulse ring-2 ring-white/50' : ''}`}
    >
      <span className={active ? 'animate-spin' : ''}>{icon}</span>
      <span className="hidden sm:inline">{label}</span>
    </button>
  );
}

function StatCard({ title, value, icon, color }: any) {
  const colors: any = {
    blue: 'border-blue-500/20 bg-blue-500/5',
    purple: 'border-purple-500/20 bg-purple-500/5',
    yellow: 'border-yellow-500/20 bg-yellow-500/5',
    green: 'border-green-500/20 bg-green-500/5',
  };

  return (
    <div className={`p-8 rounded-[2rem] border ${colors[color]} backdrop-blur-md group hover:border-white/20 transition-all shadow-inner`}>
      <div className="flex justify-between items-start mb-6">
        <div className="p-4 rounded-2xl bg-black/40 border border-white/10 shadow-lg">{icon}</div>
        <div className="text-[10px] font-black text-white/30 tracking-[0.2em] uppercase">Neural Stat</div>
      </div>
      <div className="text-4xl font-black mb-1">{value}</div>
      <div className="text-gray-500 text-sm font-bold uppercase tracking-tight">{title}</div>
    </div>
  );
}

function HealthBar({ label, active }: any) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm font-medium text-white/80">{label}</span>
      <div className={`w-12 h-6 rounded-full p-1 transition-colors ${active ? 'bg-green-400' : 'bg-white/20'}`}>
        <div className={`w-4 h-4 bg-white rounded-full transition-transform ${active ? 'translate-x-6' : 'translate-x-0'}`}></div>
      </div>
    </div>
  );
}
