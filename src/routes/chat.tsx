import { createFileRoute } from '@tanstack/react-router';
import { Send, Bot, User, Shield, Sparkles, Terminal, ArrowLeft, BrainCircuit } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
import { Link } from '@tanstack/react-router';

export const Route = createFileRoute('/chat')({
  component: NeuralChat,
});

interface Message {
  id: string;
  text: string;
  sender: 'ai' | 'user';
  timestamp: string;
}

function NeuralChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hola, soy el Núcleo de Inteligencia de Peralta. ¿En qué puedo ayudarte hoy?',
      sender: 'ai',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [scanStatus, setScanStatus] = useState<{activo: boolean, progreso: number, total: number, archivo: string, amenazas: number} | null>(null);
  const [wasScanning, setWasScanning] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, scanStatus]);

  useEffect(() => {
    const fetchScanStatus = async () => {
      try {
        const res = await fetch('http://localhost:5005/api/scan-status');
        if (res.ok) {
          const data = await res.json();
          setScanStatus(data);
        }
      } catch (e) {
        // Ignore polling errors
      }
    };
    
    fetchScanStatus();
    const interval = setInterval(fetchScanStatus, 500);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (scanStatus?.activo) {
      if (!wasScanning) setWasScanning(true);
    } else if (wasScanning) {
      setWasScanning(false);
      const msg = scanStatus?.amenazas && scanStatus.amenazas > 0 
        ? `Escaneo completado. Encontré ${scanStatus.amenazas} amenazas y las envié a cuarentena.`
        : 'Listo, escaneo completado. El sistema se encuentra 100% limpio y seguro.';
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        text: msg,
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    }
  }, [scanStatus, wasScanning]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    // Real-time Neural Integration with Demo Fallback
    try {
      const response = await fetch('http://localhost:5005/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensaje: input }),
      });

      if (!response.ok) throw new Error('Backend Offline');

      const data = await response.json();
      const aiMsg: Message = {
        id: Date.now().toString(),
        text: data.respuesta || "No pude procesar tu solicitud.",
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      // Fallback for Web Demo session when local daemon is not reachable
      const isCommand = userMsg.text.toLowerCase().includes('analiza') || userMsg.text.toLowerCase().includes('escanea');
      const responseText = isCommand 
        ? `[DEMO] He programado un escaneo profundo para "${userMsg.text.replace(/analiza|escanea|la carpeta/gi, '').trim() || 'el sistema'}". Este es un entorno de demostración en línea. Instalando la aplicación nativa conectarás directamente con el Motor Neuronal Peralta 3.2 localmente.`
        : `[DEMO] Entiendo tu mensaje "${userMsg.text}". Como esta es la versión de demostración web, mi capacidad de acción está limitada. Para usar todo el poder de Peralta Antivirus, descarga la versión de escritorio.`;
        
      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        text: responseText,
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, aiMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#05070a] text-white pt-24 pb-12 flex flex-col font-['Space_Grotesk'] overflow-hidden">
      <div className="max-w-4xl mx-auto w-full flex-1 flex flex-col px-4">
        
        {/* Chat Header */}
        <div className="flex items-center justify-between mb-8 bg-white/5 p-6 rounded-3xl border border-white/10 backdrop-blur-xl">
          <div className="flex items-center gap-4">
            <Link to="/security" className="p-2 hover:bg-white/10 rounded-xl transition-all">
              <ArrowLeft className="w-6 h-6" />
            </Link>
            <div className="relative">
              <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/20">
                <BrainCircuit className="w-7 h-7 text-white" />
              </div>
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-4 border-[#05070a] animate-pulse"></div>
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">Asistente Neural</h1>
              <p className="text-blue-400 text-xs font-bold uppercase tracking-widest flex items-center gap-2">
                <Sparkles className="w-3 h-3" /> Motor Llama 3.2 Activo
              </p>
            </div>
          </div>
          <div className="hidden md:flex flex-col items-end">
            <div className="text-xs text-gray-500 font-medium">Latencia Local</div>
            <div className="text-sm font-mono text-green-500">~12ms</div>
          </div>
        </div>

        {/* Messages Area */}
        <div 
          ref={scrollRef}
          className="flex-1 overflow-y-auto mb-6 space-y-6 pr-2 custom-scrollbar"
        >
          {messages.map((msg) => (
            <div 
              key={msg.id} 
              className={`flex items-start gap-4 ${msg.sender === 'user' ? 'flex-row-reverse' : ''} animate-in fade-in slide-in-from-bottom-4 duration-300`}
            >
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 border ${msg.sender === 'ai' ? 'bg-blue-600/20 border-blue-500/30 text-blue-400' : 'bg-purple-600/20 border-purple-500/30 text-purple-400'}`}>
                {msg.sender === 'ai' ? <Bot className="w-5 h-5" /> : <User className="w-5 h-5" />}
              </div>
              <div className={`max-w-[80%] p-5 rounded-2xl border ${msg.sender === 'ai' ? 'bg-[#0a0c12] border-white/5 rounded-tl-none' : 'bg-blue-600 border-blue-500/30 rounded-tr-none shadow-lg shadow-blue-600/10'}`}>
                <div className="text-sm leading-relaxed">{msg.text}</div>
                <div className={`text-[10px] mt-2 opacity-50 font-medium ${msg.sender === 'user' ? 'text-right' : ''}`}>
                  {msg.timestamp}
                </div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex items-start gap-4 animate-pulse">
              <div className="w-10 h-10 rounded-xl bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                <Bot className="w-5 h-5" />
              </div>
              <div className="bg-[#0a0c12] border border-white/5 p-5 rounded-2xl rounded-tl-none flex gap-1">
                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce"></div>
                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              </div>
            </div>
          )}
          
          {scanStatus && scanStatus.activo && (
            <div className="flex items-start gap-4 animate-in fade-in slide-in-from-bottom-4 duration-300">
              <div className="w-10 h-10 rounded-xl bg-green-600/20 border border-green-500/30 flex items-center justify-center text-green-400 shrink-0">
                <Shield className="w-5 h-5 animate-pulse" />
              </div>
              <div className="w-full max-w-[80%] bg-[#0a0c12] border border-green-500/30 p-5 rounded-2xl rounded-tl-none shadow-lg shadow-green-500/10">
                <div className="flex justify-between items-center mb-3">
                  <div className="text-sm font-bold text-green-400 flex items-center gap-2">
                    <Sparkles className="w-4 h-4 animate-spin-slow" /> Escaneo Neuronal Activo
                  </div>
                  <div className="text-xs font-mono text-green-500">
                    {Math.round((scanStatus.progreso / Math.max(1, scanStatus.total)) * 100)}%
                  </div>
                </div>
                
                <div className="w-full h-2 bg-black/50 rounded-full overflow-hidden mb-3 border border-white/5">
                  <div 
                    className="h-full bg-gradient-to-r from-green-500 to-emerald-400 transition-all duration-300" 
                    style={{ width: `${(scanStatus.progreso / Math.max(1, scanStatus.total)) * 100}%` }}
                  ></div>
                </div>
                
                <div className="flex justify-between text-[11px]">
                  <div className="text-white/50 truncate max-w-[70%]">
                    Analizando: <span className="text-white/80">{scanStatus.archivo}</span>
                  </div>
                  <div className={scanStatus.amenazas > 0 ? "text-red-400 font-bold" : "text-green-500"}>
                    {scanStatus.amenazas} Amenazas
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <form 
          onSubmit={handleSend}
          className="relative bg-white/5 p-2 rounded-[2rem] border border-white/10 backdrop-blur-2xl focus-within:border-blue-500/50 transition-all shadow-2xl"
        >
          <div className="absolute left-6 top-1/2 -translate-y-1/2 text-gray-500">
            <Terminal className="w-5 h-5" />
          </div>
          <input 
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe una orden o pregunta (ej. 'analiza mi carpeta descargas')..."
            className="w-full bg-transparent border-none focus:ring-0 py-4 pl-14 pr-16 text-sm md:text-base font-medium placeholder:text-gray-600"
          />
          <button 
            type="submit"
            disabled={loading || !input.trim()}
            className="absolute right-2 top-2 p-3 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:hover:bg-blue-600 rounded-[1.5rem] transition-all shadow-lg shadow-blue-500/30"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
        <div className="text-center mt-4 text-[10px] text-gray-600 uppercase tracking-[0.2em] font-black">
          Powered by Peralta Neural Engine
        </div>
      </div>
    </div>
  );
}
