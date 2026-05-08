import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Shield, 
  ShieldCheck, 
  Activity, 
  Globe, 
  Zap, 
  Bell, 
  AlertTriangle, 
  Terminal, 
  Settings,
  Cpu,
  Lock,
  Search,
  CheckCircle,
  XCircle
} from 'lucide-react';
import { LineChart, Line, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';

const API_BASE = 'http://localhost:5005/api';

const StatCard = ({ icon: Icon, title, value, color }) => (
  <div className="glass-panel p-6 shadow-xl flex items-center space-x-4 border-l-4" style={{ borderColor: color }}>
    <div className="p-3 rounded-xl bg-opacity-10" style={{ backgroundColor: color }}>
      <Icon size={24} style={{ color }} />
    </div>
    <div>
      <p className="text-secondary text-sm font-medium">{title}</p>
      <h3 className="text-2xl font-bold">{value}</h3>
    </div>
  </div>
);

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState({
    estado: 'CONECTANDO...',
    amenazas_bloqueadas: 0,
    carga_motor: '0%',
    memoria_uso: '0 GB/s',
    uptime: '0%'
  });
  const [logs, setLogs] = useState([]);
  const [isScanning, setIsScanning] = useState(false);
  const [notification, setNotification] = useState(null);
  const [activityData, setActivityData] = useState([]);

  // Polling de datos
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, logsRes] = await Promise.all([
          fetch(`${API_BASE}/stats`),
          fetch(`${API_BASE}/logs`)
        ]);
        const statsData = await statsRes.json();
        const logsData = await logsRes.json();
        
        setStats(statsData);
        setLogs(logsData);
        
        // Simular datos de gráfica basados en carga real
        const loadVal = parseInt(statsData.carga_motor) || 10;
        setActivityData(prev => [...prev.slice(-10), { time: new Date().toLocaleTimeString(), load: loadVal }]);
      } catch (err) {
        console.error("Error conectando con Peralta API:", err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleAction = async (endpoint, label) => {
    if (endpoint === 'scan') setIsScanning(true);
    
    try {
      const res = await fetch(`${API_BASE}/${endpoint}`, { method: 'POST' });
      if (res.ok) {
        showNotification(`${label} iniciado correctamente`, 'success');
      }
    } catch (err) {
      showNotification(`Error al ejecutar ${label}`, 'error');
    }
    
    if (endpoint === 'scan') {
        setTimeout(() => setIsScanning(false), 5000); // Simulamos fin de escaneo para el UI
    }
  };

  const showNotification = (msg, type) => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 4000);
  };

  return (
    <div className="min-vh-100 p-8 flex flex-col items-center bg-[#050505] text-white">
      {/* Notifications */}
      <AnimatePresence>
        {notification && (
          <motion.div 
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
            className={`fixed top-8 z-50 glass-panel px-6 py-3 flex items-center space-x-3 border-b-2 ${notification.type === 'success' ? 'border-success' : 'border-danger'}`}
          >
            {notification.type === 'success' ? <CheckCircle className="text-success" size={20} /> : <XCircle className="text-danger" size={20} />}
            <span className="font-bold text-sm">{notification.msg}</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <header className="w-full max-w-6xl flex justify-between items-center mb-12">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 glass-panel flex items-center justify-center neon-border">
            <Shield className="text-accent-cyan" size={28} />
          </div>
          <div>
            <h1 className="text-2xl m-0 font-bold tracking-tight">
              PERALTA <span className="text-gradient">ANTIVIRUS</span>
            </h1>
            <p className="text-xs text-secondary font-mono">NEURAL ENGINE V1.0</p>
          </div>
        </div>
        
        <nav className="glass-panel px-4 py-2 flex space-x-1">
          {['dashboard', 'threats', 'network', 'settings'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === tab ? 'bg-white bg-opacity-10 text-white' : 'text-secondary hover:text-white'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 glass-panel px-4 py-2">
            <div className={`w-2 h-2 rounded-full ${stats.estado === 'PROTEGIDO' ? 'bg-success' : 'bg-warning'} neural-glow`} />
            <span className="text-sm font-semibold">{stats.estado || 'DESCONECTADO'}</span>
          </div>
          <button className="glass-panel p-2 hover:bg-white hover:bg-opacity-5">
            <Bell size={20} className="text-secondary" />
          </button>
        </div>
      </header>

      {/* Main Grid */}
      <main className="w-full max-w-6xl grid grid-cols-12 gap-6">
        
        {/* Left Column: Stats & Monitoring */}
        <div className="col-span-12 lg:col-span-8 space-y-6">
          
          <div className="grid grid-cols-3 gap-4">
            <StatCard icon={Activity} title="Actividad Global" value={stats.memoria_uso} color="var(--accent-cyan)" />
            <StatCard icon={ShieldCheck} title="Amenazas Bloqueadas" value={stats.amenazas_bloqueadas} color="var(--success)" />
            <StatCard icon={Cpu} title="Carga del Motor" value={stats.carga_motor} color="var(--accent-purple)" />
          </div>

          <div className="glass-panel p-6 h-64">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-bold flex items-center uppercase tracking-tighter">
                <Zap size={20} className="mr-2 text-warning" /> Análisis en Tiempo Real
              </h3>
              <div className="text-xs font-mono text-secondary">SYNC: OK</div>
            </div>
            <div className="h-40">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={activityData}>
                  <Line type="monotone" dataKey="load" stroke="var(--accent-cyan)" strokeWidth={3} dot={false} isAnimationActive={false} />
                  <Tooltip 
                    contentStyle={{ background: '#111', border: '1px solid rgba(255,255,255,0.1)' }}
                    itemStyle={{ color: 'var(--accent-cyan)' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="glass-panel overflow-hidden">
            <div className="p-4 border-b border-white border-opacity-5 flex justify-between items-center bg-white bg-opacity-5">
              <h3 className="text-sm font-bold flex items-center uppercase tracking-wider">
                <Terminal size={16} className="mr-2" /> Live Neural Log
              </h3>
              <button 
                onClick={() => setLogs([])}
                className="text-[10px] text-secondary hover:text-white uppercase font-bold"
              >
                Limpiar
              </button>
            </div>
            <div className="p-4 h-48 overflow-y-auto font-mono text-xs space-y-2">
              {logs.length > 0 ? logs.map((log, i) => (
                <div key={i} className="flex justify-between items-start group border-b border-white border-opacity-5 pb-1">
                  <div className="flex space-x-2">
                    <span className={`font-bold
                      ${log.type === 'info' ? 'text-accent-cyan' : ''}
                      ${log.type === 'success' ? 'text-success' : ''}
                      ${log.type === 'warning' ? 'text-warning' : ''}
                      ${log.type === 'error' ? 'text-danger' : ''}
                    `}>[{log.type.toUpperCase()}]</span>
                    <span className="text-zinc-300">{log.msg}</span>
                  </div>
                  <span className="text-[10px] text-zinc-600">{log.time}</span>
                </div>
              )) : (
                <div className="h-full flex items-center justify-center text-zinc-500 italic">No hay actividad reciente</div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Neural Core & Quick Actions */}
        <div className="col-span-12 lg:col-span-4 space-y-6">
          
          <div className="glass-panel p-8 flex flex-col items-center justify-center neon-border overflow-hidden relative min-h-[400px]">
             <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cyan-500/5 to-purple-500/5 pointer-events-none" />
             
             <motion.div 
              animate={isScanning ? {
                scale: [1, 1.15, 1],
                rotate: [0, 90, 180, 270, 360],
              } : { 
                scale: [1, 1.05, 1],
                rotate: [0, 5, -5, 0]
              }}
              transition={isScanning ? { duration: 2, repeat: Infinity, ease: "linear" } : { duration: 6, repeat: Infinity, ease: "easeInOut" }}
              className="relative z-10 w-48 h-48 flex items-center justify-center"
             >
                <div className={`absolute inset-0 ${isScanning ? 'bg-cyan-500/40' : 'bg-cyan-500/20'} blur-3xl rounded-full animate-pulse`} />
                <img 
                  src="/assets/neural_brain_core.png" 
                  alt="Neural Core" 
                  className={`w-full h-full object-contain neural-glow brightness-125 transition-all ${isScanning ? 'hue-rotate-90' : ''}`}
                />
             </motion.div>

             <div className="mt-8 text-center relative z-10">
               <h2 className="text-2xl font-black tracking-tighter mb-1 uppercase">Núcleo Neural</h2>
               <div className="flex items-center justify-center space-x-2">
                 <div className="flex space-x-1">
                   {[1,2,3,4,5].map(i => <div key={i} className={`w-1 h-3 rounded-full animate-bounce ${isScanning ? 'bg-warning' : 'bg-accent-cyan'}`} style={{ animationDelay: `${i*0.2}s` }} />)}
                 </div>
                 <span className={`text-xs font-mono font-bold ${isScanning ? 'text-warning' : 'text-accent-cyan'}`}>
                    {isScanning ? 'ESCANEANDO...' : 'SISTEMA ÓPTIMO'}
                 </span>
               </div>
             </div>

             <button 
                onClick={() => handleAction('scan', 'Escaneo Profundo')}
                disabled={isScanning}
                className={`mt-8 px-8 py-4 rounded-xl font-black transition-all w-full flex items-center justify-center space-x-2 shadow-2xl
                    ${isScanning ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed' : 'bg-gradient-to-r from-cyan-600 to-purple-600 hover:scale-105 active:scale-95 text-white'}
                `}
             >
               <Search size={22} />
               <span>{isScanning ? 'ANÁLISIS EN CURSO' : 'ESCANEO PROFUNDO'}</span>
             </button>
          </div>

          <div className="glass-panel p-6 space-y-4">
             <h3 className="text-sm font-black uppercase tracking-widest text-secondary border-b border-white border-opacity-5 pb-2 text-center">Acciones Críticas</h3>
             <div className="grid grid-cols-2 gap-3">
                <button onClick={() => handleAction('update', 'Actualización de Feeds')} className="flex flex-col items-center justify-center p-4 glass-panel hover:bg-white hover:bg-opacity-5 transition-all hover:scale-105">
                   <Globe size={20} className="text-accent-cyan mb-2" />
                   <span className="text-[10px] font-bold">ACTUALIZAR</span>
                </button>
                <button onClick={() => showNotification("Web Wall Activo", "success")} className="flex flex-col items-center justify-center p-4 glass-panel hover:bg-white hover:bg-opacity-5 transition-all hover:scale-105">
                   <Shield size={20} className="text-success mb-2" />
                   <span className="text-[10px] font-bold">WEB WALL</span>
                </button>
                <button onClick={() => handleAction('stop', 'Protección')} className="flex flex-col items-center justify-center p-4 glass-panel hover:bg-white hover:bg-opacity-5 transition-all hover:scale-105 group">
                   <Lock size={20} className="text-danger mb-2 group-hover:animate-ping" />
                   <span className="text-[10px] font-bold">DETENER</span>
                </button>
                <button onClick={() => showNotification("Módulo de Ajustes en desarrollo", "info")} className="flex flex-col items-center justify-center p-4 glass-panel hover:bg-white hover:bg-opacity-5 transition-all hover:scale-105">
                   <Settings size={20} className="text-zinc-500 mb-2" />
                   <span className="text-[10px] font-bold">CONFIG</span>
                </button>
             </div>
          </div>

        </div>

      </main>

      {/* Footer */}
      <footer className="w-full max-w-6xl mt-12 flex justify-between items-center text-[10px] font-mono text-zinc-500 border-t border-white border-opacity-5 pt-4">
        <div>© 2026 PERALTA TECHNOLOGIES — MOTOR NEURAL: {stats.motor_neural || 'CARGANDO...'}</div>
        <div className="flex space-x-6">
          <span>LATENCIA: 12ms</span>
          <span>UPTIME: {stats.uptime}</span>
          <span className="text-success">CONEXIÓN: SEGURA</span>
        </div>
      </footer>

      {/* Background Decor */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none -z-10 opacity-20 overflow-hidden">
        <div className="absolute top-1/4 -left-20 w-96 h-96 bg-cyan-600 rounded-full blur-[150px] animate-pulse" />
        <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-purple-600 rounded-full blur-[150px] animate-pulse" style={{ animationDelay: '1s' }} />
      </div>
    </div>
  );
}

export default App;
