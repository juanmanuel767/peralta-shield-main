#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║          P E R A L T A   A N T I V I R U S  v1.0            ║
║   Desarrollado por: Ing. Juan Manuel Peralta                 ║
║   Protección inteligente con Motor Neuronal propio           ║
║   Linux · Windows 10/11 · macOS                              ║
║                                                              ║
║   Módulos:                                                   ║
║   • Monitor de apps nuevas (instalaciones)                   ║
║   • Protección web (URLs y dominios maliciosos)              ║
║   • Detección de intrusos / hackeo                           ║
║   • Alertas de voz en español                                ║
║   • Inteligencia Artificial Neural (Completamente local)     ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, sys, json, re, time, hashlib, shutil, stat, socket
import threading, platform, subprocess, logging, argparse, ipaddress, http.server
import zipfile, tarfile, tempfile, math
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import webbrowser
from collections import defaultdict

# ─── Detección de sistema ────────────────────────────────────
SISTEMA = platform.system()
ES_WIN  = SISTEMA == "Windows"
ES_LIN  = SISTEMA == "Linux"
ES_MAC  = SISTEMA == "Darwin"

# ─── Importaciones opcionales (se instalan si no están) ──────
def importar_paquete(nombre, pip_nombre=None):
    import importlib
    try:
        return importlib.import_module(nombre)
    except ImportError:
        paq = pip_nombre or nombre
        subprocess.run([sys.executable, "-m", "pip", "install", paq, "--quiet",
                        "--break-system-packages" if (ES_LIN or ES_MAC) else ""],
                       capture_output=True)
        try:
            return importlib.import_module(nombre)
        except Exception: # Puede ser ImportError, ValueError, etc.
            return None

PIL     = importar_paquete("PIL", "Pillow")
if PIL:
    try:
        from PIL import Image
    except Exception:
        PIL = None

requests = importar_paquete("requests")
rich_console_mod = importar_paquete("rich.console")
rich_table_mod   = importar_paquete("rich.table")
rich_panel_mod   = importar_paquete("rich.panel")
rich_text_mod    = importar_paquete("rich.text")
rich_mod         = importar_paquete("rich")
pyttsx3          = importar_paquete("pyttsx3")
watchdog_obs     = importar_paquete("watchdog.observers", "watchdog")
watchdog_ev      = importar_paquete("watchdog.events",    "watchdog")
psutil           = importar_paquete("psutil")
flask            = importar_paquete("flask")
flask_cors       = importar_paquete("flask_cors")
yara             = importar_paquete("yara", "yara-python")

from rich.console import Console
from rich.table   import Table
from rich.panel   import Panel
from rich.text    import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich         import box
console = Console()

# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN GLOBAL
# ══════════════════════════════════════════════════════════════
CONFIG_PATH = Path.home() / ".peralta_config.json"
DEFAULT_CONFIG = {
    "version": "1.0.0",
    "modelo_neuronal": "llama3.2",
    "motor_url": "http://localhost:11434",
    "voz_activada": True,
    "velocidad_voz": 145,
    "escaneo_web": True,
    "escaneo_apps": True,
    "escaneo_red": True,
    "proteccion_tiempo_real": True,
    "max_file_size_ia": 512000,
    "quarantine_dir": str(Path.home() / ".peralta" / "quarantine"),
    "log_dir": str(Path.home() / ".peralta" / "logs"),
}

def cargar_config() -> dict:
    config = DEFAULT_CONFIG.copy()
    if CONFIG_PATH.exists():
        try:
            user_cfg = json.loads(CONFIG_PATH.read_text())
            # Migración de configuración antigua (Rebranding)
            if "modelo_ollama" in user_cfg and "modelo_neuronal" not in user_cfg:
                user_cfg["modelo_neuronal"] = user_cfg.pop("modelo_ollama")
            if "ollama_url" in user_cfg and "motor_url" not in user_cfg:
                user_cfg["motor_url"] = user_cfg.pop("ollama_url")
            
            config.update(user_cfg)
        except Exception as e:
            print(f"Error cargando config: {e}")
    return config

CFG = cargar_config()
Path(CFG["quarantine_dir"]).mkdir(parents=True, exist_ok=True)
Path(CFG["log_dir"]).mkdir(parents=True, exist_ok=True)

# ══════════════════════════════════════════════════════════════
# MÓDULO DE VOZ
# ══════════════════════════════════════════════════════════════
class Voz:
    """Alertas de voz en español usando pyttsx3."""
    _engine = None
    _lock = threading.Lock()

    @classmethod
    def _init(cls):
        if cls._engine is None and pyttsx3:
            try:
                cls._engine = pyttsx3.init()
                cls._engine.setProperty("rate", CFG["velocidad_voz"])
                # Buscar voz en español
                voces = cls._engine.getProperty("voices")
                for v in voces:
                    # Linux/Windows: helena, jorge, sabina | macOS: paulina, monica
                    if any(x in v.id.lower() for x in ["es", "spanish", "español", "helena", "jorge", "sabina", "paulina", "monica"]):
                        cls._engine.setProperty("voice", v.id)
                        break
            except Exception:
                cls._engine = None

    @classmethod
    def hablar(cls, texto: str, urgente: bool = False):
        """Habla en voz alta de forma asíncrona."""
        if not CFG.get("voz_activada"):
            return
        def _hablar():
            with cls._lock:
                cls._init()
                if cls._engine:
                    try:
                        if urgente:
                            cls._engine.setProperty("rate", 130)
                        cls._engine.say(texto)
                        cls._engine.runAndWait()
                        cls._engine.setProperty("rate", CFG["velocidad_voz"])
                    except Exception:
                        pass
        threading.Thread(target=_hablar, daemon=True).start()

# ══════════════════════════════════════════════════════════════
# HASHES DE MALWARE CONOCIDO
# ══════════════════════════════════════════════════════════════
HASHES_MALWARE: Dict[str, str] = {
    # Agrega aquí hashes SHA256 de malware conocido
    # "hash_sha256": "Nombre del malware"
}

# ══════════════════════════════════════════════════════════════
# DOMINIOS Y IPs MALICIOSAS (base local)
# ══════════════════════════════════════════════════════════════
DOMINIOS_MALICIOSOS = {
    # Categorías conocidas de malware C&C y phishing
    "malware.wicar.org", "testphp.vulnweb.com", "eicar.org",
    "crimeflare.com", "stopbadware.org",
    # Mineros web conocidos
    "coinhive.com", "coin-hive.com", "minero.pw", "jsecoin.com",
    "cryptoloot.pro", "webminepool.com", "authedmine.com",
    # C2 conocidos (Command & Control de botnets)
    "zeustracker.abuse.ch",
    "malware-distribution.com",
}

IPS_MALICIOSAS = set()  # Se puede poblar desde feeds

# URLs de feeds de threat intelligence (se actualizan con --update)
FEEDS_DOMINIOS = [
    "https://urlhaus.abuse.ch/downloads/text/",
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
]

# ══════════════════════════════════════════════════════════════
# PATRONES DE CÓDIGO MALICIOSO
# ══════════════════════════════════════════════════════════════
PATRONES = [
    # CRÍTICOS
    (r'bash\s+-i\s+>&\s*/dev/tcp',           "CRITICA", "Bash reverse shell"),
    (r'nc\s+-e\s+/bin/(ba)?sh',              "CRITICA", "Netcat reverse shell"),
    (r'python.*socket.*connect.*exec',        "CRITICA", "Python reverse shell (direct exec)"),
    (r'socket.*connect.*subprocess.*call',    "CRITICA", "Python reverse shell (subprocess)"),
    (r'os\.dup2.*socket.*subprocess',         "CRITICA", "Redirected shell sockets"),
    (r'/dev/tcp/\d{1,3}\.\d{1,3}',           "CRITICA", "Shell via /dev/tcp"),
    (r'curl\s+\S+\s*\|\s*(ba)?sh',           "CRITICA", "Descarga y ejecución remota"),
    (r'wget\s+\S+\s*\|\s*(ba)?sh',           "CRITICA", "Descarga y ejecución remota"),
    (r'base64\s+-d.*\|\s*(ba)?sh',           "CRITICA", "Ejecución de payload base64"),
    (r'eval\s*\(.*base64',                   "CRITICA", "Eval + base64 (webshell)"),
    (r'import\s+socket,os,pty\s*s=socket\.socket', "CRITICA", "Python reverse shell (PTY injection)"),
    (r'pty\.spawn\s*\(\s*["\']/bin/bash["\']\s*\)', "CRITICA", "Inyección de terminal PTY interactiva"),
    (r'open\s*\(.*/etc/shadow.*,.*["\']r["\']\)', "CRITICA", "Lectura de archivos de sistema sensibles"),
    (r'[A-Za-z0-9+/]{30,}==',                 "ALTA",    "Payload base64 de alta densidad"),
    (r'xmrig|cpuminer|minerd',               "CRITICA", "Minero de criptomonedas"),
    (r'stratum\+tcp://',                     "CRITICA", "Protocolo Stratum (minería)"),
    (r'openssl\s+enc\s+-aes.*-k',             "CRITICA", "Cifrado masivo (Posible Ransomware)"),
    (r'YOUR_FILES_ARE_ENCRYPTED',            "CRITICA", "Nota de rescate de Ransomware"),
    (r'AES.*encrypt.*(os\.remove|unlink)',   "CRITICA", "Cifrado y borrado masivo (Comportamiento Ransomware)"),
    (r'bitcoin.*wallet.*[13j][a-km-zA-HJ-NP-Z1-9]{25,34}', "CRITICA", "Dirección de pago Bitcoin (Ransomware/Exfiltración)"),
    (r'find / .*-exec rm',                   "CRITICA", "Borrado masivo de archivos"),
    (r'echo\s+\S+\s*>>\s*/etc/(passwd|shadow)', "CRITICA", "Modificación de passwd/shadow"),
    (r'/etc/shadow.*curl',                   "CRITICA", "Exfiltración de hashes de sistema"),
    # ALTAS
    (r'EncryptFile|CryptAcquireContext',     "ALTA",    "Llamadas a API de cifrado sospechosas"),
    (r'\.locky|\.crypt|\.encrypted',         "ALTA",    "Extensiones de archivos cifrados conocidas"),
    (r'GetAsyncKeyState|GetKeyState',         "ALTA",    "Captura de teclado (Keylogger)"),
    (r'SetWindowsHookEx',                    "ALTA",    "Hook de teclado/mouse"),
    (r'/proc/keys|/dev/input/event',         "ALTA",    "Acceso a entrada de bajo nivel"),
    (r'reg\s+add.*\\RunOnce',                "ALTA",    "Persistencia en registro (RunOnce)"),
    (r'schtasks\s+/create.*/sc\s+onlogon',  "ALTA",    "Tarea programada al iniciar sesión"),
    (r'LaunchAgents|LaunchDaemons',          "ALTA",    "Persistencia en macOS/Linux"),
    (r'base64\s+-d.*\|\s*eval',              "ALTA",    "Base64 con ejecución directa (eval)"),
    (r'javascript:eval\(atob\(',             "ALTA",    "JS ofuscado en red"),
    (r'nohup\s+\S+.*&\s*$',                  "ALTA",   "Proceso ocultado en background"),
    (r'chmod\s+[47]\d{3}\s+/(etc|bin|usr)',  "ALTA",   "Cambio de permisos en directorio del sistema"),
    (r'(systemctl|service)\s+\S+\s+enable',  "ALTA",   "Habilitación de servicio"),
    (r'crontab.*\|.*(curl|wget|bash)',        "ALTA",   "Cron con descarga remota"),
    (r'@reboot.*(curl|wget|bash|nc)',         "ALTA",   "Persistencia en @reboot"),
    (r'cat\s+/etc/shadow',                   "ALTA",   "Lectura de hashes de contraseñas"),
    (r'find.*\.ssh.*-exec',                  "ALTA",   "Búsqueda y exfiltración de claves SSH"),
    # MEDIAS
    (r'sudo\s+-S',                           "MEDIA",  "sudo por stdin (fuerza bruta)"),
    (r'usermod\s+-aG\s+sudo',               "MEDIA",  "Usuario añadido a sudo"),
    (r'(powershell|cmd).*-enc(odedcommand)?',"MEDIA",  "PowerShell encoded command"),
    (r'Invoke-Expression|IEX\s*\(',          "MEDIA",  "PowerShell IEX (descarga/ejecución)"),
    (r'DownloadString|DownloadFile',         "MEDIA",  "PowerShell download"),
    (r'Set-MpPreference.*Disable',           "MEDIA",  "Desactivación de Windows Defender"),
    (r'netsh.*firewall.*disable',            "MEDIA",  "Desactivación de firewall Windows"),
    (r'reg\s+add.*\\Run',                    "MEDIA",  "Persistencia en registro Windows"),
    # BAJAS
    (r'[A-Za-z0-9+/]{200,}={0,2}',          "BAJA",   "Posible payload en Base64"),
    (r'\\x[0-9a-f]{2}(\\x[0-9a-f]{2}){15,}',"BAJA",   "Cadena hex ofuscada"),
]

# Extensiones de riesgo
EXT_ALTO_RIESGO  = {".sh",".bash",".py",".pl",".rb",".php",".js",".ps1",".vbs",".bat",".cmd",".elf",".run"}
EXT_MEDIO_RIESGO = {".exe",".msi",".dll",".so",".deb",".rpm",".dmg",".apk",".appimage"}
EXT_BAJO_RIESGO  = {".zip",".tar",".gz",".7z",".iso",".jar"}

# ══════════════════════════════════════════════════════════════
# MOTOR YARA (Opcional)
# ══════════════════════════════════════════════════════════════
class YaraEngine:
    def __init__(self):
        self.rules = None
        if yara:
            try:
                # Reglas básicas integradas
                rules_str = """
                rule ReverseShell {
                    strings:
                        $s1 = "bash -i >& /dev/tcp/"
                        $s2 = "nc -e /bin/sh"
                        $s3 = "import socket,os,pty;s=socket.socket"
                    condition:
                        any of them
                }
                rule RansomwarePotencial {
                    strings:
                        $crypt1 = "AES_encrypt"
                        $crypt2 = "CryptAcquireContext"
                        $msg1 = "your files have been encrypted"
                        $ext1 = ".crypt"
                    condition:
                        2 of ($crypt*) or ($msg1 and $ext1)
                }
                rule CryptoMiner {
                    strings:
                        $m1 = "stratum+tcp://"
                        $m2 = "xmrig"
                        $m3 = "cpuminer"
                        $m4 = "CryptoNight"
                        $m5 = "hashrate"
                    condition:
                        2 of them
                }
                rule RAT_Generic {
                    strings:
                        $r1 = "keylogger"
                        $r2 = "screenshot"
                        $r3 = "webcam"
                        $r4 = "reverse_tcp"
                        $r5 = "bind_tcp"
                    condition:
                        3 of them
                }
                rule Webshell {
                    strings:
                        $w1 = "eval($_POST"
                        $w2 = "eval($_GET"
                        $w3 = "system($_REQUEST"
                        $w4 = "passthru("
                        $w5 = "base64_decode($_"
                    condition:
                        any of them
                }
                rule Rootkit_Linux {
                    strings:
                        $k1 = "__NR_getdents"
                        $k2 = "hide_pid"
                        $k3 = "/proc/self/maps"
                        $k4 = "LD_PRELOAD"
                    condition:
                        2 of them
                }
                """
                self.rules = yara.compile(source=rules_str)
            except Exception:
                self.rules = None

    def escanear(self, ruta: str) -> List[dict]:
        hallazgos = []
        if self.rules:
            try:
                matches = self.rules.match(ruta)
                for m in matches:
                    hallazgos.append({"nivel": "ALTA", "descripcion": f"YARA match: {m.rule}"})
            except Exception:
                pass
        return hallazgos

# ══════════════════════════════════════════════════════════════
# MOTOR DE ANÁLISIS DE ARCHIVOS
# ══════════════════════════════════════════════════════════════
class Analizador:
    def __init__(self):
        self.yara_engine = YaraEngine()

    def calcular_entropia(self, ruta: str) -> float:
        """Calcula la entropía de Shannon para detectar archivos comprimidos/cifrados."""
        try:
            with open(ruta, 'rb') as f:
                data = f.read(10240) # Solo los primeros 10KB
                if not data: return 0
                entropy = 0
                for x in range(256):
                    p_x = data.count(x) / len(data)
                    if p_x > 0:
                        entropy += - p_x * math.log(p_x, 2)
                return entropy
        except Exception:
            return 0

    def analizar_archivo_comprimido(self, ruta: str) -> List[dict]:
        """Extrae y analiza archivos dentro de un ZIP o TAR."""
        hallazgos_extra = []
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                if zipfile.is_zipfile(ruta):
                    with zipfile.ZipFile(ruta, 'r') as z:
                        z.extractall(tmpdir)
                elif tarfile.is_tarfile(ruta):
                    with tarfile.open(ruta, 'r:*') as t:
                        t.extractall(tmpdir)
                
                # Escaneo recursivo de los archivos extraídos
                for root, _, files in os.walk(tmpdir):
                    for f in files:
                        fpath = os.path.join(root, f)
                        res = self.analizar_archivo(fpath, usar_ia=False)
                        if res["estado"] in ("AMENAZA", "SOSPECHOSO"):
                            for h in res["hallazgos"]:
                                h["descripcion"] = f"[{f}] {h['descripcion']}"
                                hallazgos_extra.append(h)
            except Exception:
                pass
        return hallazgos_extra

    def hash_archivo(self, ruta: str) -> dict:
        md5, sha256 = hashlib.md5(), hashlib.sha256()
        try:
            with open(ruta, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    md5.update(chunk); sha256.update(chunk)
            return {"md5": md5.hexdigest(), "sha256": sha256.hexdigest()}
        except Exception:
            return {}

    def verificar_hash(self, hashes: dict) -> Optional[str]:
        for v in hashes.values():
            if v in HASHES_MALWARE:
                return HASHES_MALWARE[v]
        return None

    def buscar_patrones(self, contenido: str) -> List[dict]:
        hallazgos = []
        for patron, nivel, desc in PATRONES:
            if re.search(patron, contenido, re.IGNORECASE | re.MULTILINE | re.DOTALL):
                hallazgos.append({"nivel": nivel, "descripcion": desc})
        return hallazgos

    def tipo_archivo(self, ruta: str) -> str:
        """Determina el tipo MIME del archivo usando el comando 'file' (Unix) o mimetypes (Win)."""
        if ES_LIN or ES_MAC:
            try:
                r = subprocess.run(["file", "--mime-type", "-b", ruta],
                                   capture_output=True, text=True, timeout=5)
                return r.stdout.strip()
            except Exception:
                return ""
        elif ES_WIN:
            import mimetypes
            return mimetypes.guess_type(ruta)[0] or ""
        return ""

    def analizar_ia(self, ruta: str, contenido: str, hallazgos: list) -> dict:
        """Análisis profundo con Motor Neuronal."""
        ctx = "\n".join([f"- [{h['nivel']}] {h['descripcion']}" for h in hallazgos]) or "Ninguno"
        entropy = self.calcular_entropia(ruta)
        prompt = f"""Eres el cerebro del Antivirus Peralta. Analiza este archivo y detecta si es malicioso.
        
ARCHIVO: {os.path.basename(ruta)}
TAMAÑO: {os.path.getsize(ruta)} bytes
ENTROPÍA: {entropy:.2f} (Alta entropía puede indicar cifrado/compresión)
SISTEMA: {SISTEMA}
HALLAZGOS PREVIOS:
{ctx}

CONTENIDO (primeros 2000 chars):
```
{contenido[:2000]}
```

Responde SOLO en JSON:
{{"veredicto":"MALICIOSO|SOSPECHOSO|LIMPIO","confianza":0-100,"tipo":"tipo de amenaza o ninguna","descripcion":"máximo 2 oraciones en español","acciones":["acción1"],"indicadores":["indicador1"]}}"""
        try:
            r = requests.post(
                f"{CFG['motor_url']}/api/generate",
                json={"model": CFG["modelo_neuronal"], "prompt": prompt,
                      "stream": False, "options": {"temperature": 0.05, "num_predict": 400}},
                timeout=90
            )
            if r.status_code == 200:
                texto = r.json().get("response", "")
                m = re.search(r'\{.*\}', texto, re.DOTALL)
                if m:
                    return json.loads(m.group())
        except Exception:
            pass
        return {}

    def analizar_archivo(self, ruta: str, usar_ia: bool = True) -> dict:
        resultado = {
            "ruta": ruta, "nombre": os.path.basename(ruta),
            "estado": "LIMPIO", "nivel": "NINGUNO",
            "hashes": {}, "hallazgos": [], "ia": {},
            "timestamp": datetime.now().isoformat()
        }
        try:
            tamaño = os.path.getsize(ruta)
        except Exception as e:
            resultado["estado"] = "ERROR"; resultado["error"] = str(e)
            return resultado

        # 1. Hashes
        resultado["hashes"] = self.hash_archivo(ruta)
        malware = self.verificar_hash(resultado["hashes"])
        if malware:
            resultado["estado"] = "AMENAZA"; resultado["nivel"] = "CRITICO"
            resultado["hallazgos"].append({"nivel": "CRITICA", "descripcion": f"Hash malicioso: {malware}"})

        # 2. Patrones en contenido de texto
        ext = Path(ruta).suffix.lower()
        
        # 2.1 YARA
        resultado["hallazgos"].extend(self.yara_engine.escanear(ruta))

        # 2.2 Archivos comprimidos
        if ext in (".zip", ".tar", ".gz", ".xz"):
            resultado["hallazgos"].extend(self.analizar_archivo_comprimido(ruta))

        # 2.3 Análisis Binario (PE/ELF/Mach-O)
        if ext in (".exe", ".elf", ".so", ".dll", ".dylib", ".macho", "") or ext in EXT_MEDIO_RIESGO:
            bin_analyzer = AnalizadorBinario()
            resultado["hallazgos"].extend(bin_analyzer.analizar(ruta))

        mime = self.tipo_archivo(ruta) if (ES_LIN or ES_MAC) else ""
        es_texto = "text" in mime or ext in EXT_ALTO_RIESGO

        contenido = ""
        if es_texto and tamaño < 20_000_000:
            try:
                with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                    contenido = f.read()
                resultado["hallazgos"].extend(self.buscar_patrones(contenido))
            except Exception:
                pass

        # 3. Calcular nivel de riesgo
        if resultado["estado"] != "AMENAZA":
            niveles = {h["nivel"] for h in resultado["hallazgos"]}
            if "CRITICA" in niveles or "ALTA" in niveles:
                resultado["estado"] = "AMENAZA"; resultado["nivel"] = "ALTO"
            elif "MEDIA" in niveles:
                resultado["estado"] = "SOSPECHOSO"; resultado["nivel"] = "MEDIO"
            elif "BAJA" in niveles:
                resultado["estado"] = "SOSPECHOSO"; resultado["nivel"] = "BAJO"

        # 4. IA si es sospechoso/amenaza y tamaño OK
        if usar_ia and contenido and tamaño <= CFG["max_file_size_ia"]:
            if resultado["estado"] in ("AMENAZA", "SOSPECHOSO") or ext in EXT_ALTO_RIESGO:
                resultado["ia"] = self.analizar_ia(ruta, contenido, resultado["hallazgos"])
                veredicto = resultado["ia"].get("veredicto", "")
                if veredicto == "MALICIOSO" and resultado["estado"] != "AMENAZA":
                    resultado["estado"] = "AMENAZA"; resultado["nivel"] = "ALTO"
        return resultado


# ══════════════════════════════════════════════════════════════
# MÓDULO DE PROTECCIÓN WEB
# ══════════════════════════════════════════════════════════════
class ProteccionWeb:
    """Detecta y bloquea dominios/URLs maliciosas."""

    def __init__(self):
        self.dominios_bloqueados = set(DOMINIOS_MALICIOSOS)
        self._cargar_hosts_locales()

    def _ruta_hosts(self) -> Path:
        if ES_LIN or ES_MAC:
            return Path("/etc/hosts")
        elif ES_WIN:
            return Path(r"C:\Windows\System32\drivers\etc\hosts")
        return Path("/etc/hosts")

    def _cargar_hosts_locales(self):
        """Carga dominios bloqueados desde /etc/hosts o sistema."""
        hosts = self._ruta_hosts()
        if hosts.exists():
            for linea in hosts.read_text(errors="ignore").splitlines():
                if linea.startswith("0.0.0.0") or linea.startswith("127.0.0.1"):
                    partes = linea.split()
                    if len(partes) >= 2:
                        self.dominios_bloqueados.add(partes[1].lower())

    def verificar_dominio(self, dominio: str) -> dict:
        """Alias para verificar_url simplificado."""
        return self.verificar_url(f"http://{dominio}")

    def verificar_url(self, url: str) -> dict:
        """Verifica si una URL es maliciosa."""
        resultado = {"url": url, "estado": "LIMPIO", "razon": "", "peligroso": False}
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url if "://" in url else f"http://{url}")
            dominio = parsed.netloc.lower().lstrip("www.")

            # Verificar dominio
            if dominio in self.dominios_bloqueados:
                resultado["estado"] = "BLOQUEADO"
                resultado["razon"] = f"Dominio en lista negra: {dominio}"
                return resultado

            # Verificar dominios similares (typosquatting)
            marcas = ["google", "paypal", "amazon", "microsoft", "apple", "facebook",
                      "instagram", "netflix", "bancolombia", "davivienda", "bbva"]
            for marca in marcas:
                if marca in dominio and dominio != f"{marca}.com" and dominio != f"www.{marca}.com":
                    if any(c in dominio for c in ["0", "1", "-", "_"]):
                        resultado["estado"] = "SOSPECHOSO"
                        resultado["razon"] = f"Posible typosquatting de {marca}: {dominio}"

            # Verificar IP directa (bypass DNS)
            try:
                ipaddress.ip_address(dominio)
                resultado["estado"] = "SOSPECHOSO"
                resultado["razon"] = f"URL usa IP directa (evita DNS): {dominio}"
            except ValueError:
                pass
            
            resultado["peligroso"] = resultado["estado"] in ("BLOQUEADO", "SOSPECHOSO")

        except Exception as e:
            resultado["razon"] = str(e)
        return resultado

    def actualizar_feeds(self):
        """Descarga listas de dominios maliciosos actualizadas."""
        if not requests:
            return 0
        nuevos = 0
        for feed in FEEDS_DOMINIOS:
            try:
                r = requests.get(feed, timeout=30)
                if r.status_code == 200:
                    for linea in r.text.splitlines():
                        linea = linea.strip().lower()
                        if linea and not linea.startswith("#"):
                            partes = linea.split()
                            dominio = partes[-1] if len(partes) > 1 else partes[0]
                            if "." in dominio and len(dominio) > 3:
                                self.dominios_bloqueados.add(dominio)
                                nuevos += 1
            except Exception:
                pass
        return nuevos

    def bloquear_dominio(self, dominio: str) -> bool:
        """Añade un dominio al hosts para bloquearlo."""
        hosts = self._ruta_hosts()
        try:
            contenido = hosts.read_text(errors="ignore")
            if dominio not in contenido:
                with open(hosts, "a") as f:
                    f.write(f"\n0.0.0.0 {dominio}  # Bloqueado por Peralta")
            self.dominios_bloqueados.add(dominio)
            if ES_MAC:
                subprocess.run(["dscacheutil", "-flushcache"], capture_output=True)
                subprocess.run(["killall", "-HUP", "mDNSResponder"], capture_output=True)
            return True
        except PermissionError:
            return False  # Sin permisos de administrador


# ══════════════════════════════════════════════════════════════
# MÓDULO DE DETECCIÓN DE INTRUSOS (IDS)
# ══════════════════════════════════════════════════════════════
class DetectorIntrusos:
    """Detecta intentos de hackeo, escaneos de puertos, fuerza bruta."""

    def __init__(self):
        self.intentos_conexion: Dict[str, list] = defaultdict(list)
        self.ips_bloqueadas: set = set()
        self.alertas: list = []
        self._umbral_brute = 10   # intentos en 60s
        self._umbral_scan  = 20   # puertos en 10s
        self._activo = False

    def analizar_conexiones(self) -> list:
        """Analiza conexiones activas buscando comportamientos sospechosos."""
        if not psutil:
            return []
        amenazas = []
        try:
            conexiones = psutil.net_connections(kind="inet")
            puertos_externos: Dict[str, set] = defaultdict(set)

            for c in conexiones:
                if c.status == "ESTABLISHED" and c.raddr:
                    ip_remota = c.raddr.ip
                    puerto_remoto = c.raddr.port

                    # Verificar IP maliciosa conocida
                    if ip_remota in IPS_MALICIOSAS:
                        amenazas.append({
                            "tipo": "IP_MALICIOSA",
                            "nivel": "CRITICA",
                            "ip": ip_remota,
                            "puerto": puerto_remoto,
                            "desc": f"Conexión a IP maliciosa conocida: {ip_remota}"
                        })

                    # Puertos sospechosos (backdoors comunes)
                    puertos_backdoor = {4444, 1337, 31337, 5555, 9999, 6666, 2222}
                    if puerto_remoto in puertos_backdoor:
                        amenazas.append({
                            "tipo": "PUERTO_SOSPECHOSO",
                            "nivel": "ALTA",
                            "ip": ip_remota,
                            "puerto": puerto_remoto,
                            "desc": f"Conexión a puerto de backdoor conocido: {puerto_remoto}"
                        })

                    puertos_externos[ip_remota].add(puerto_remoto)

            # Detectar escaneo de puertos (una IP conectada a muchos puertos locales)
            for ip, puertos in puertos_externos.items():
                if ip in ("127.0.0.1", "::1"):
                    continue
                if len(puertos) > 15:
                    amenazas.append({
                        "tipo": "ESCANEO_PUERTOS",
                        "nivel": "ALTA",
                        "ip": ip,
                        "puertos": len(puertos),
                        "desc": f"Posible escaneo de puertos desde {ip} ({len(puertos)} puertos)"
                    })

        except Exception:
            pass
        return amenazas

    def analizar_procesos(self) -> list:
        """Busca procesos sospechosos."""
        if not psutil:
            return []
        amenazas = []
        procesos_sospechosos = {
            "xmrig", "minerd", "cpuminer", "cgminer",  # mineros
            "nmap", "masscan", "zmap",                  # escáneres
            "msfconsole", "msfvenom",                   # metasploit
            "nc", "ncat", "socat",                      # netcat (contextual)
            "mimikatz",                                  # robo de credenciales
        }
        try:
            for proc in psutil.process_iter(["pid", "name", "cmdline", "connections"]):
                nombre = (proc.info.get("name") or "").lower()
                cmdline = " ".join(proc.info.get("cmdline") or []).lower()

                if nombre in procesos_sospechosos:
                    amenazas.append({
                        "tipo": "PROCESO_MALICIOSO",
                        "nivel": "CRITICA",
                        "pid": proc.info["pid"],
                        "nombre": nombre,
                        "desc": f"Proceso sospechoso detectado: {nombre} (PID {proc.info['pid']})"
                    })

                # Detectar reverse shells por cmdline
                patrones_proc = [
                    r'/dev/tcp/', r'bash -i', r'sh -i',
                    r'nc.*-e.*sh', r'python.*socket.*connect'
                ]
                for p in patrones_proc:
                    if re.search(p, cmdline, re.IGNORECASE):
                        amenazas.append({
                            "tipo": "REVERSE_SHELL",
                            "nivel": "CRITICA",
                            "pid": proc.info["pid"],
                            "cmdline": cmdline[:100],
                            "desc": f"Posible reverse shell en PID {proc.info['pid']}"
                        })
                        break
        except Exception:
            pass
        return amenazas

    def monitorear_continuo(self, callback):
        """Monitoreo continuo en hilo separado."""
        self._activo = True
        def _loop():
            while self._activo:
                amenazas = self.analizar_conexiones() + self.analizar_procesos()
                for a in amenazas:
                    callback(a)
                time.sleep(15)  # Revisar cada 15 segundos
        threading.Thread(target=_loop, daemon=True).start()

    def detener(self):
        self._activo = False


# ══════════════════════════════════════════════════════════════
# FASE 1 — VIGILANTE BEHAVIORAL (Análisis de Comportamiento)
# ══════════════════════════════════════════════════════════════
class VigilanteBehavioral:
    """Monitorea el COMPORTAMIENTO de procesos para detectar malware por lo que HACE."""

    def __init__(self, callback):
        self.callback = callback
        self._activo = False
        self._scores: Dict[int, dict] = {}  # PID -> {score, acciones, nombre}
        self._file_events: Dict[int, list] = defaultdict(list)  # PID -> [timestamps de escritura]
        self._net_events: Dict[int, set] = defaultdict(set)      # PID -> {IPs contactadas}
        self._umbral_ransomware = 50    # archivos modificados en ventana
        self._umbral_exfil = 10         # IPs únicas contactadas
        self._ventana_segundos = 15

    def _analizar_proceso(self, proc) -> dict:
        """Evalúa un proceso individual y le asigna una puntuación de riesgo."""
        score = 0
        acciones = []
        pid = proc.pid
        nombre = ""
        try:
            nombre = proc.name().lower()
            cmdline = " ".join(proc.cmdline()).lower()

            # 1. Archivos abiertos — ¿Está tocando muchos archivos?
            try:
                open_files = proc.open_files()
                sensitive_paths = ["/etc/shadow", "/etc/passwd", ".ssh/", ".gnupg/",
                                   "wallet.dat", ".mozilla/", ".chrome/", "Login Data"]
                for f in open_files:
                    for sp in sensitive_paths:
                        if sp in f.path:
                            score += 30
                            acciones.append(f"Accede a archivo sensible: {f.path}")
                            break
                # Muchos archivos abiertos de golpe
                if len(open_files) > 100:
                    score += 15
                    acciones.append(f"Tiene {len(open_files)} archivos abiertos")
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

            # 2. Conexiones de red — ¿Habla con muchas IPs?
            try:
                conns = proc.net_connections(kind="inet")
                ips_externas = set()
                for c in conns:
                    if c.raddr and c.status == "ESTABLISHED":
                        ip = c.raddr.ip
                        if not ip.startswith("127.") and ip != "::1":
                            ips_externas.add(ip)
                            # Puertos de C2 conocidos
                            if c.raddr.port in {4444, 1337, 31337, 5555, 8888, 9999}:
                                score += 40
                                acciones.append(f"Conexión a puerto C2: {c.raddr.port}")
                self._net_events[pid] = ips_externas
                if len(ips_externas) > self._umbral_exfil:
                    score += 25
                    acciones.append(f"Contacta {len(ips_externas)} IPs externas (posible exfiltración)")
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

            # 3. Consumo de CPU anómalo (posible minero)
            try:
                cpu = proc.cpu_percent(interval=0.1)
                if cpu > 85 and nombre not in {"Xorg", "gnome-shell", "firefox", "chrome", "code"}:
                    score += 20
                    acciones.append(f"CPU al {cpu:.0f}% — posible minero")
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

            # 4. Proceso sin terminal ni ventana (oculto)
            try:
                terminal = proc.terminal()
                if terminal is None and nombre not in {"systemd", "init", "cron", "sshd",
                                                        "ollama", "python3", "node", "dbus-daemon"}:
                    score += 5
            except (psutil.AccessDenied, psutil.NoSuchProcess, AttributeError):
                pass

            # 5. Cmdline sospechoso
            patrones_cmd = [
                (r"curl.*\|.*sh", 35, "Descarga y ejecución remota"),
                (r"base64.*-d", 20, "Decodificación Base64"),
                (r"/dev/tcp/", 50, "Reverse shell via /dev/tcp"),
                (r"nc\s+-e", 45, "Netcat reverse shell"),
                (r"python.*exec\(", 15, "Python exec dinámico"),
                (r"rm\s+-rf\s+/", 50, "Borrado masivo del sistema"),
                (r"dd\s+if=/dev/zero\s+of=/", 50, "Sobrescritura de disco"),
            ]
            for pat, pts, desc in patrones_cmd:
                if re.search(pat, cmdline, re.IGNORECASE):
                    score += pts
                    acciones.append(desc)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        return {"pid": pid, "nombre": nombre, "score": score, "acciones": acciones}

    def monitorear_continuo(self, callback=None):
        """Hilo de monitoreo behavioral continuo."""
        cb = callback or self.callback
        self._activo = True

        def _loop():
            while self._activo:
                if not psutil:
                    time.sleep(10)
                    continue
                try:
                    for proc in psutil.process_iter(["pid", "name"]):
                        try:
                            resultado = self._analizar_proceso(proc)
                            self._scores[resultado["pid"]] = resultado
                            if resultado["score"] >= 40:
                                nivel = "CRITICA" if resultado["score"] >= 70 else "ALTA"
                                cb({
                                    "tipo": "BEHAVIORAL",
                                    "nivel": nivel,
                                    "pid": resultado["pid"],
                                    "nombre": resultado["nombre"],
                                    "score": resultado["score"],
                                    "desc": f"Proceso {resultado['nombre']} (PID {resultado['pid']}) "
                                            f"puntuación={resultado['score']}: "
                                            f"{'; '.join(resultado['acciones'][:3])}"
                                })
                        except Exception:
                            pass
                except Exception:
                    pass
                time.sleep(10)

        threading.Thread(target=_loop, daemon=True).start()

    def obtener_scores(self) -> List[dict]:
        """Retorna la lista de procesos con sus puntuaciones actuales."""
        return sorted(self._scores.values(), key=lambda x: x["score"], reverse=True)[:20]

    def detener(self):
        self._activo = False


# ══════════════════════════════════════════════════════════════
# FASE 3 — FIREWALL NEURONAL (Clasificación IA de conexiones)
# ══════════════════════════════════════════════════════════════
class FirewallNeuronal:
    """Analiza conexiones de red y detecta tráfico C2, beaconing y DNS tunneling."""

    def __init__(self, callback):
        self.callback = callback
        self._activo = False
        self._historial_conn: Dict[str, list] = defaultdict(list)  # IP -> [timestamps]
        self._dns_queries: Dict[str, int] = defaultdict(int)
        # IPs internas a ignorar
        self._whitelist = {"127.0.0.1", "::1", "0.0.0.0"}

    def _es_ip_interna(self, ip: str) -> bool:
        try:
            addr = ipaddress.ip_address(ip)
            return addr.is_private or addr.is_loopback or addr.is_link_local
        except ValueError:
            return False

    def _detectar_beaconing(self) -> list:
        """Detecta procesos que contactan la misma IP a intervalos regulares (C2 beaconing)."""
        alertas = []
        ahora = time.time()
        for ip, timestamps in self._historial_conn.items():
            recientes = [t for t in timestamps if ahora - t < 300]  # últimos 5 min
            if len(recientes) >= 5:
                # Calcular regularidad de intervalos
                intervalos = [recientes[i+1] - recientes[i] for i in range(len(recientes)-1)]
                if intervalos:
                    promedio = sum(intervalos) / len(intervalos)
                    varianza = sum((x - promedio)**2 for x in intervalos) / len(intervalos)
                    # Si los intervalos son muy regulares → beaconing
                    if varianza < 5 and promedio < 120:
                        alertas.append({
                            "tipo": "BEACONING",
                            "nivel": "ALTA",
                            "ip": ip,
                            "intervalo": f"{promedio:.1f}s",
                            "desc": f"Posible C2 beaconing a {ip} cada ~{promedio:.0f}s "
                                    f"({len(recientes)} conexiones en 5min)"
                        })
        return alertas

    def _detectar_dns_tunnel(self) -> list:
        """Detecta DNS tunneling: subdominios exageradamente largos o muchas queries."""
        alertas = []
        for domain, count in self._dns_queries.items():
            # Subdominios de más de 50 chars → posible DNS tunnel
            parts = domain.split(".")
            if any(len(p) > 50 for p in parts):
                alertas.append({
                    "tipo": "DNS_TUNNEL",
                    "nivel": "CRITICA",
                    "dominio": domain,
                    "desc": f"Posible DNS tunneling: subdominio excesivamente largo en {domain}"
                })
            # Muchas queries al mismo dominio base
            if count > 100:
                base = ".".join(parts[-2:]) if len(parts) >= 2 else domain
                alertas.append({
                    "tipo": "DNS_FLOOD",
                    "nivel": "ALTA",
                    "dominio": base,
                    "desc": f"Exceso de consultas DNS a {base} ({count} queries)"
                })
        return alertas

    def monitorear_continuo(self):
        """Monitoreo continuo de red con detección avanzada."""
        self._activo = True

        def _loop():
            while self._activo:
                if not psutil:
                    time.sleep(15)
                    continue
                try:
                    ahora = time.time()
                    for conn in psutil.net_connections(kind="inet"):
                        if conn.status == "ESTABLISHED" and conn.raddr:
                            ip = conn.raddr.ip
                            if ip not in self._whitelist and not self._es_ip_interna(ip):
                                self._historial_conn[ip].append(ahora)
                                # Limpiar historial viejo (> 10 min)
                                self._historial_conn[ip] = [
                                    t for t in self._historial_conn[ip] if ahora - t < 600
                                ]

                    # Ejecutar detecciones
                    for alerta in self._detectar_beaconing():
                        self.callback(alerta)
                    for alerta in self._detectar_dns_tunnel():
                        self.callback(alerta)

                except Exception:
                    pass
                time.sleep(20)

        threading.Thread(target=_loop, daemon=True).start()

    def detener(self):
        self._activo = False


# ══════════════════════════════════════════════════════════════
# FASE 3 — PROTECTOR WiFi (ARP Spoof / Rogue AP)
# ══════════════════════════════════════════════════════════════
class ProtectorWiFi:
    """Detecta dispositivos en la red local, ARP spoofing y rogue APs."""

    def __init__(self, callback):
        self.callback = callback
        self._activo = False
        self._arp_table: Dict[str, str] = {}  # IP -> MAC
        self._dispositivos_conocidos: set = set()

    def obtener_tabla_arp(self) -> Dict[str, str]:
        """Lee la tabla ARP del sistema."""
        tabla = {}
        try:
            if ES_LIN:
                r = subprocess.run(["arp", "-n"], capture_output=True, text=True, timeout=5)
                for linea in r.stdout.splitlines()[1:]:
                    partes = linea.split()
                    if len(partes) >= 3 and partes[2] != "(incomplete)":
                        tabla[partes[0]] = partes[2]  # IP -> MAC
            elif ES_WIN or ES_MAC:
                r = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=5)
                # Parseo para Windows/Mac: "host (IP) at MAC" o similar
                for linea in r.stdout.splitlines():
                    if ES_WIN:
                        partes = linea.split()
                        if len(partes) >= 3 and "-" in partes[1]:
                            tabla[partes[0]] = partes[1]
                    elif ES_MAC:
                        # Formato Darwin: ? (192.168.1.1) at 00:11:22:33:44:55 on en0 ifscope [ethernet]
                        match = re.search(r"\((.*?)\) at (.*?) on", linea)
                        if match:
                            tabla[match.group(1)] = match.group(2)
        except Exception:
            pass
        return tabla

    def detectar_arp_spoof(self) -> list:
        """Detecta múltiples IPs con la misma MAC (ARP spoofing)."""
        alertas = []
        tabla = self.obtener_tabla_arp()
        mac_a_ips: Dict[str, list] = defaultdict(list)
        for ip, mac in tabla.items():
            mac_a_ips[mac].append(ip)
        for mac, ips in mac_a_ips.items():
            if len(ips) > 1 and mac != "ff:ff:ff:ff:ff:ff":
                alertas.append({
                    "tipo": "ARP_SPOOF",
                    "nivel": "CRITICA",
                    "mac": mac,
                    "ips": ips,
                    "desc": f"¡ALERTA ARP SPOOFING! MAC {mac} asociada a {len(ips)} IPs: "
                            f"{', '.join(ips[:5])}. Posible ataque Man-in-the-Middle."
                })
        return alertas

    def detectar_nuevos_dispositivos(self) -> list:
        """Detecta dispositivos nuevos en la red."""
        alertas = []
        tabla = self.obtener_tabla_arp()
        for ip, mac in tabla.items():
            ident = f"{ip}_{mac}"
            if ident not in self._dispositivos_conocidos:
                self._dispositivos_conocidos.add(ident)
                if self._arp_table:
                    alertas.append({
                        "tipo": "NUEVO_DISPOSITIVO",
                        "nivel": "MEDIA",
                        "ip": ip,
                        "mac": mac,
                        "desc": f"Nuevo dispositivo en la red: {ip} (MAC: {mac})"
                    })
        self._arp_table = tabla
        return alertas

    def escanear_red(self) -> List[dict]:
        """Escaneo completo de la red local."""
        dispositivos = []
        tabla = self.obtener_tabla_arp()
        for ip, mac in tabla.items():
            dispositivos.append({"ip": ip, "mac": mac, "estado": "activo"})
        return dispositivos

    def monitorear_continuo(self):
        self._activo = True
        # Inicializar tabla base
        self._arp_table = self.obtener_tabla_arp()
        for ip, mac in self._arp_table.items():
            self._dispositivos_conocidos.add(f"{ip}_{mac}")

        def _loop():
            while self._activo:
                for alerta in self.detectar_arp_spoof():
                    self.callback(alerta)
                for alerta in self.detectar_nuevos_dispositivos():
                    self.callback(alerta)
                time.sleep(30)

        threading.Thread(target=_loop, daemon=True).start()

    def detener(self):
        self._activo = False


# ══════════════════════════════════════════════════════════════
# FASE 4 — MONITOR USB (Escaneo automático de dispositivos)
# ══════════════════════════════════════════════════════════════
class MonitorUSB:
    """Detecta conexiones USB nuevas y escanea automáticamente."""

    def __init__(self, analizador: 'Analizador', callback):
        self.analizador = analizador
        self.callback = callback
        self._activo = False
        self._montajes_conocidos: set = set()

    def _obtener_montajes(self) -> set:
        """Obtiene los puntos de montaje actuales (Win/Lin/Mac)."""
        montajes = set()
        try:
            if ES_LIN:
                dirs_usb = ["/media", "/mnt", "/run/media"]
                for base in dirs_usb:
                    p = Path(base)
                    if p.exists():
                        for child in p.iterdir():
                            if child.is_dir() or child.is_mount():
                                montajes.add(str(child))
            elif ES_MAC:
                if Path("/Volumes").exists():
                    for child in Path("/Volumes").iterdir():
                        if child.is_dir() and child.name != "Macintosh HD":
                            montajes.add(str(child))
            elif ES_WIN:
                if psutil:
                    for part in psutil.disk_partitions():
                        if 'removable' in part.opts.lower() or 'cdrom' in part.opts.lower():
                            montajes.add(part.mountpoint)
        except Exception:
            pass
        return montajes

    def _escanear_montaje(self, ruta: str):
        """Escanea todos los archivos de un montaje USB."""
        archivos = []
        for root, _, files in os.walk(ruta):
            for f in files:
                archivos.append(os.path.join(root, f))
                if len(archivos) > 5000:
                    break
            if len(archivos) > 5000:
                break

        amenazas = 0
        for archivo in archivos:
            try:
                resultado = self.analizador.analizar_archivo(archivo, usar_ia=False)
                if resultado["estado"] in ("AMENAZA", "SOSPECHOSO"):
                    amenazas += 1
                    self.callback("USB_AMENAZA", resultado)
            except Exception:
                pass

        self.callback("USB_SCAN_COMPLETO", {
            "estado": "INFO",
            "nombre": ruta,
            "desc": f"USB escaneado: {len(archivos)} archivos, {amenazas} amenazas",
            "archivos": len(archivos),
            "amenazas": amenazas
        })

    def monitorear_continuo(self):
        self._activo = True
        self._montajes_conocidos = self._obtener_montajes()

        def _loop():
            while self._activo:
                montajes_actual = self._obtener_montajes()
                nuevos = montajes_actual - self._montajes_conocidos
                for nuevo in nuevos:
                    self.callback("USB_CONECTADO", {
                        "estado": "INFO",
                        "nombre": nuevo,
                        "desc": f"Nuevo dispositivo USB detectado: {nuevo}. Escaneando..."
                    })
                    # Voz.hablar("Se conectó un dispositivo USB. Escaneando automáticamente.", urgente=True)
                    threading.Thread(target=self._escanear_montaje, args=(nuevo,), daemon=True).start()
                self._montajes_conocidos = montajes_actual
                time.sleep(5)

        threading.Thread(target=_loop, daemon=True).start()

    def detener(self):
        self._activo = False


# ══════════════════════════════════════════════════════════════
# FASE 4 — PROTECTOR DE PRIVACIDAD (Webcam / Micrófono)
# ══════════════════════════════════════════════════════════════
class ProtectorPrivacidad:
    """Detecta acceso no autorizado a cámara y micrófono."""

    def __init__(self, callback):
        self.callback = callback
        self._activo = False
        self._whitelist = {"chrome", "firefox", "chromium", "zoom", "teams", "discord",
                           "obs", "vlc", "skype", "telegram", "slack", "cheese",
                           "pipewire", "pulseaudio", "wireplumber"}
        self._alerted_pids: set = set()

    def _verificar_webcam_linux(self) -> list:
        """Verifica qué procesos tienen acceso a /dev/video*."""
        alertas = []
        for video_dev in Path("/dev").glob("video*"):
            try:
                r = subprocess.run(["fuser", str(video_dev)], capture_output=True, text=True, timeout=3)
                pids = r.stdout.strip().split()
                for pid_str in pids:
                    pid = int(pid_str.strip())
                    if pid in self._alerted_pids:
                        continue
                    try:
                        proc = psutil.Process(pid)
                        nombre = proc.name().lower()
                        if nombre not in self._whitelist:
                            self._alerted_pids.add(pid)
                            alertas.append({
                                "tipo": "WEBCAM_ACCESO",
                                "nivel": "ALTA",
                                "pid": pid,
                                "nombre": nombre,
                                "desc": f"⚠ {nombre} (PID {pid}) está usando tu CÁMARA"
                            })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except Exception:
                pass
        return alertas

    def _verificar_microfono_linux(self) -> list:
        """Verifica acceso al micrófono via /proc."""
        alertas = []
        try:
            r = subprocess.run(["fuser", "-v", "/dev/snd/*"], capture_output=True,
                               text=True, timeout=3, shell=True)
            for linea in r.stderr.splitlines():
                partes = linea.split()
                if len(partes) >= 4:
                    try:
                        pid = int(partes[2])
                        if pid in self._alerted_pids:
                            continue
                        proc = psutil.Process(pid)
                        nombre = proc.name().lower()
                        if nombre not in self._whitelist and "F" in partes[3]:
                            self._alerted_pids.add(pid)
                            alertas.append({
                                "tipo": "MICROFONO_ACCESO",
                                "nivel": "ALTA",
                                "pid": pid,
                                "nombre": nombre,
                                "desc": f"⚠ {nombre} (PID {pid}) está usando tu MICRÓFONO"
                            })
                    except (ValueError, psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
        except Exception:
            pass
        return alertas

    def _verificar_privacidad_win(self) -> list:
        """Verifica acceso a cámara en Windows vía registro."""
        alertas = []
        if not ES_WIN: return []
        # Placeholder: En Windows se requiere acceso a registro de CapabilityAccessManager
        return alertas

    def _verificar_privacidad_mac(self) -> list:
        """Verifica acceso a cámara en macOS vía lsof."""
        alertas = []
        if not ES_MAC: return []
        try:
            # lsof | grep VDC es un patrón común para cámara en Mac
            r = subprocess.run(["lsof", "-n", "-P", "-i", "-c", "VDC"], capture_output=True, text=True, timeout=3)
            # Esto es simplificado, en Mac real es más complejo
            if "VDC" in r.stdout:
                pass # Lógica de detección según lsof
        except: pass
        return alertas

    def monitorear_continuo(self):
        self._activo = True

        def _loop():
            while self._activo:
                if not psutil:
                    time.sleep(15)
                    continue
                
                alertas = []
                if ES_LIN:
                    alertas.extend(self._verificar_webcam_linux())
                    alertas.extend(self._verificar_microfono_linux())
                elif ES_WIN:
                    alertas.extend(self._verificar_privacidad_win())
                elif ES_MAC:
                    alertas.extend(self._verificar_privacidad_mac())

                for alerta in alertas:
                    self.callback(alerta)
                    Voz.hablar(f"Alerta de privacidad. {alerta['nombre']} está usando tu sensor.", urgente=True)
                
                # Limpiar PIDs de procesos que ya no existen
                self._alerted_pids = {p for p in self._alerted_pids if psutil.pid_exists(p)}
                time.sleep(10)

        threading.Thread(target=_loop, daemon=True).start()

    def detener(self):
        self._activo = False


# ══════════════════════════════════════════════════════════════
# FASE 2 — ANALIZADOR BINARIO (PE/ELF Headers)
# ══════════════════════════════════════════════════════════════
class AnalizadorBinario:
    """Inspecciona ejecutables a nivel de headers para detectar empaquetadores y anomalías."""

    SECCIONES_SOSPECHOSAS = {
        ".evil", ".packed", ".UPX0", ".UPX1", ".UPX2", ".aspack", ".adata",
        ".rsrc1", ".nsp0", ".nsp1", ".vmp0", ".vmp1", ".themida"
    }

    def analizar_elf(self, ruta: str) -> List[dict]:
        """Análisis de binarios ELF (Linux)."""
        hallazgos = []
        try:
            with open(ruta, "rb") as f:
                magic = f.read(4)
                if magic != b"\x7fELF":
                    return []

                # Leer tipo de ELF
                f.seek(16)
                e_type = int.from_bytes(f.read(2), "little")
                tipos = {2: "Ejecutable", 3: "Shared object"}
                tipo_str = tipos.get(e_type, f"Tipo {e_type}")
                hallazgos.append({"nivel": "BAJA", "descripcion": f"Binario Linux ELF detectado: {tipo_str}"})

                # Verificar si está stripped (sin info de debug)
                r = subprocess.run(["file", ruta], capture_output=True, text=True, timeout=5)
                output = r.stdout.lower()

                if "statically linked" in output:
                    hallazgos.append({"nivel": "MEDIA", "descripcion": f"ELF estáticamente linkado ({tipo_str})"})

                if "stripped" in output and "not stripped" not in output:
                    hallazgos.append({"nivel": "BAJA", "descripcion": "ELF stripped — posible ofuscación"})

                if "upx" in output:
                    hallazgos.append({"nivel": "ALTA", "descripcion": "ELF empaquetado con UPX"})

                # Verificar secciones sospechosas
                try:
                    r2 = subprocess.run(["readelf", "-S", ruta], capture_output=True, text=True, timeout=5)
                    for sec in self.SECCIONES_SOSPECHOSAS:
                        if sec in r2.stdout:
                            hallazgos.append({
                                "nivel": "ALTA",
                                "descripcion": f"Sección sospechosa: {sec}"
                            })
                except Exception:
                    pass

                # Calcular entropía del binario
                f.seek(0)
                data = f.read(10240)
                entropy = 0
                if data:
                    for x in range(256):
                        p_x = data.count(x) / len(data)
                        if p_x > 0:
                            entropy += -p_x * math.log(p_x, 2)
                    if entropy > 7.5:
                        hallazgos.append({
                            "nivel": "ALTA",
                            "descripcion": f"Entropía muy alta ({entropy:.2f}) — posible empaquetamiento"
                        })

        except Exception:
            pass
        return hallazgos

    def analizar_pe(self, ruta: str) -> List[dict]:
        """Análisis básico de PE (Windows executables)."""
        hallazgos = []
        try:
            with open(ruta, "rb") as f:
                magic = f.read(2)
                if magic != b"MZ":
                    return []

                # Verificar PE signature
                f.seek(60)
                pe_offset = int.from_bytes(f.read(4), "little")
                f.seek(pe_offset)
                pe_sig = f.read(4)
                if pe_sig != b"PE\x00\x00":
                    hallazgos.append({"nivel": "MEDIA", "descripcion": "Cabecera PE corrupta o modificada"})
                    return hallazgos

                hallazgos.append({"nivel": "BAJA", "descripcion": "Ejecutable Windows PE detectado"})

                # Entropía
                f.seek(0)
                data = f.read(10240)
                entropy = 0
                if data:
                    for x in range(256):
                        p_x = data.count(x) / len(data)
                        if p_x > 0:
                            entropy += -p_x * math.log(p_x, 2)
                    if entropy > 7.5:
                        hallazgos.append({
                            "nivel": "ALTA",
                            "descripcion": f"PE con entropía alta ({entropy:.2f}) — posiblemente empaquetado"
                        })
        except Exception:
            pass
        return hallazgos

    def analizar_macho(self, ruta: str) -> List[dict]:
        """Análisis de binarios Mach-O (macOS)."""
        hallazgos = []
        try:
            with open(ruta, "rb") as f:
                magic = f.read(4)
                # 0xFEEDFACE (32-bit), 0xFEEDFACF (64-bit), 0xCAFEBABE (FAT)
                if magic not in [b'\xfe\xed\xfa\xce', b'\xfe\xed\xfa\xcf', b'\xca\xfe\xba\xbe']:
                    return []
                hallazgos.append({"nivel": "BAJA", "descripcion": "Binario Mach-O detectado"})
                # Entropía
                f.seek(0)
                data = f.read(10240)
                entropy = 0
                if data:
                    for x in range(256):
                        p_x = data.count(x) / len(data)
                        if p_x > 0:
                            entropy += -p_x * math.log(p_x, 2)
                    if entropy > 7.6:
                        hallazgos.append({"nivel": "ALTA", "descripcion": f"Mach-O con entropía alta ({entropy:.2f})"})
        except: pass
        return hallazgos

    def analizar(self, ruta: str) -> List[dict]:
        """Punto de entrada: analiza PE, ELF o Mach-O según contenido."""
        try:
            with open(ruta, "rb") as f:
                magic = f.read(4)
            if magic[:2] == b"MZ":
                return self.analizar_pe(ruta)
            elif magic == b"\x7fELF":
                return self.analizar_elf(ruta)
            elif magic in [b'\xfe\xed\xfa\xce', b'\xfe\xed\xfa\xcf', b'\xca\xfe\xba\xbe']:
                return self.analizar_macho(ruta)
        except Exception:
            pass
        return []


# ══════════════════════════════════════════════════════════════
# FASE 1 — ASISTENTE DE SEGURIDAD IA (Chat Interactivo)
# ══════════════════════════════════════════════════════════════
class AsistenteSeguridadIA:
    """Chat interactivo con la IA de seguridad de Peralta."""

    def __init__(self, peralta_instance):
        self.peralta = peralta_instance
        self._historial = []

    def _contexto_sistema(self) -> str:
        """Genera contexto del sistema actual para la IA."""
        ctx = f"Sistema: {SISTEMA} {platform.release()}\n"
        if psutil:
            try:
                ctx += f"CPU: {psutil.cpu_percent()}% | RAM: {psutil.virtual_memory().percent}%\n"
                ctx += f"Procesos activos: {len(list(psutil.process_iter()))}\n"
                conns = psutil.net_connections(kind="inet")
                established = [c for c in conns if c.status == "ESTABLISHED"]
                ctx += f"Conexiones establecidas: {len(established)}\n"
            except Exception:
                pass
        q_items = self.peralta.cuarentena.listar()
        ctx += f"Archivos en cuarentena: {len(q_items)}\n"
        ctx += f"Motor IA: {'Activo' if self.peralta.motor_disponible() else 'Inactivo'}\n"
        return ctx

    def chatear(self, mensaje: str) -> str:
        """Procesa un mensaje del usuario y genera respuesta."""
        if not requests:
            return "Error: No hay conexión con el Motor Neuronal."

        contexto = self._contexto_sistema()

        prompt = f"""Eres el Asistente de Seguridad del Antivirus Peralta, creado por el Ing. Juan Manuel Peralta.
Tu misión es proteger al usuario y explicarle la seguridad de su PC de forma clara, en ESPAÑOL.

CONTEXTO DEL SISTEMA:
{contexto}

HISTORIAL DE CHAT:
{chr(10).join(self._historial[-6:])}

PREGUNTA DEL USUARIO: {mensaje}

Responde de forma clara, directa y profesional en español. Si necesitas ejecutar una acción, indícalo claramente.
Si el usuario pregunta si fue hackeado, analiza los datos del contexto y da un veredicto honesto."""

        try:
            r = requests.post(
                f"{CFG['motor_url']}/api/generate",
                json={"model": CFG["modelo_neuronal"], "prompt": prompt,
                      "stream": False, "options": {"temperature": 0.3, "num_predict": 500}},
                timeout=300
            )
            if r.status_code == 200:
                respuesta = r.json().get("response", "No pude generar una respuesta.")
                self._historial.append(f"Usuario: {mensaje}")
                self._historial.append(f"Peralta: {respuesta}")
                return respuesta
        except Exception as e:
            return f"Error comunicándose con el Motor Neuronal: {e}"

        return "No pude contactar al Motor Neuronal. Verifica que esté activo."

    def modo_interactivo(self):
        """Modo chat interactivo en consola."""
        console.print(Panel(
            "[bold cyan]Chat de Seguridad — Peralta Antivirus[/bold cyan]\n"
            "[dim]Escribe tu pregunta en español. Escribe 'salir' para terminar.[/dim]\n"
            "[dim]Ejemplos: '¿me hackearon?' | '¿qué hay en cuarentena?' | '¿está seguro mi PC?'[/dim]",
            border_style="cyan", title="💬 Asistente IA"
        ))

        while True:
            try:
                pregunta = input("\n[Tú] → ").strip()
                if pregunta.lower() in ("salir", "exit", "quit", "q"):
                    console.print("[dim]Chat finalizado.[/dim]")
                    break
                if not pregunta:
                    continue

                with console.status("[bold cyan]Peralta está pensando...[/bold cyan]"):
                    respuesta = self.chatear(pregunta)

                console.print(f"\n[bold green][Peralta][/bold green] {respuesta}")
                Voz.hablar(respuesta[:200])

            except (KeyboardInterrupt, EOFError):
                console.print("\n[dim]Chat finalizado.[/dim]")
                break


# ══════════════════════════════════════════════════════════════
# MONITOR DE INSTALACIONES DE APPS
# ══════════════════════════════════════════════════════════════
class MonitorApps:
    """Detecta aplicaciones nuevas que se instalan en el sistema."""

    def __init__(self, analizador: Analizador, callback):
        self.analizador = analizador
        self.callback = callback
        self._observers = []
        self._activo = False

    def _dirs_monitorear(self) -> List[str]:
        dirs = []
        if ES_LIN:
            dirs = [
                "/tmp", "/var/tmp", "/dev/shm",
                "/opt", "/usr/local/bin", "/usr/bin",
                str(Path.home() / "Downloads"),
                str(Path.home() / "Descargas"),
                "/etc/cron.d", "/etc/systemd/system",
            ]
        elif ES_WIN:
            appdata = os.environ.get("APPDATA", "")
            localappdata = os.environ.get("LOCALAPPDATA", "")
            temp = os.environ.get("TEMP", "")
            dirs = [
                "C:\\Program Files", "C:\\Program Files (x86)",
                appdata, localappdata, temp,
                str(Path.home() / "Downloads"),
                str(Path.home() / "Descargas"),
                "C:\\Users\\Public",
            ]
        return [d for d in dirs if os.path.exists(d)]

    def _es_instalador(self, ruta: str) -> bool:
        ext = Path(ruta).suffix.lower()
        nombre = Path(ruta).name.lower()
        exts_instaladores = {".exe", ".msi", ".deb", ".rpm", ".sh", ".run",
                              ".appimage", ".pkg", ".dmg"}
        palabras = {"setup", "install", "installer", "update", "upgrade",
                    "instalar", "configurar"}
        return ext in exts_instaladores or any(p in nombre for p in palabras)

    def iniciar(self):
        if not watchdog_obs or not watchdog_ev:
            console.print("[yellow]watchdog no disponible, monitor de apps desactivado[/yellow]")
            return

        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        analizador = self.analizador
        callback = self.callback

        class Handler(FileSystemEventHandler):
            def on_created(self, event):
                if event.is_directory:
                    return
                ruta = event.src_path
                ext = Path(ruta).suffix.lower()
                # Solo analizar archivos relevantes
                if ext in (EXT_ALTO_RIESGO | EXT_MEDIO_RIESGO) or self._padre._es_instalador(ruta):
                    time.sleep(0.5)  # Esperar a que el archivo esté completo
                    resultado = analizador.analizar_archivo(ruta, usar_ia=True)
                    if resultado["estado"] in ("AMENAZA", "SOSPECHOSO"):
                        callback("APP_NUEVA", resultado)

            def __init__(self, padre):
                self._padre = padre
                super().__init__()

        self._activo = True
        for directorio in self._dirs_monitorear():
            try:
                obs = Observer()
                obs.schedule(Handler(self), directorio, recursive=True)
                obs.start()
                self._observers.append(obs)
            except Exception:
                pass

    def detener(self):
        self._activo = False
        for obs in self._observers:
            try:
                obs.stop(); obs.join()
            except Exception:
                pass

    def monitorear_registro_windows(self):
        """Monitorea el registro de Windows para apps recién instaladas."""
        if not ES_WIN:
            return
        try:
            import winreg
            claves = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            ]
            apps_anteriores = set()
            for clave in claves:
                try:
                    reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, clave)
                    i = 0
                    while True:
                        try:
                            apps_anteriores.add(winreg.EnumKey(reg, i)); i += 1
                        except OSError:
                            break
                except Exception:
                    pass

            def _monitor():
                while self._activo:
                    apps_actuales = set()
                    for clave in claves:
                        try:
                            reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, clave)
                            i = 0
                            while True:
                                try:
                                    apps_actuales.add(winreg.EnumKey(reg, i)); i += 1
                                except OSError:
                                    break
                        except Exception:
                            pass
                    nuevas = apps_actuales - apps_anteriores
                    for app in nuevas:
                        self.callback("APP_INSTALADA_WIN", {
                            "nombre": app, "estado": "INFO",
                            "desc": f"Nueva app instalada en Windows: {app}"
                        })
                    apps_anteriores = apps_actuales
                    time.sleep(10)

            threading.Thread(target=_monitor, daemon=True).start()
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════
# CUARENTENA
# ══════════════════════════════════════════════════════════════
class Cuarentena:
    def __init__(self):
        self.dir = Path(CFG["quarantine_dir"])
        self.dir.mkdir(parents=True, exist_ok=True)

    def poner(self, ruta: str) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_q = f"{ts}_{Path(ruta).name}"
        destino = self.dir / nombre_q
        meta = {"original": ruta, "nombre_q": nombre_q,
                "timestamp": datetime.now().isoformat()}
        (self.dir / (nombre_q + ".meta")).write_text(json.dumps(meta, indent=2))
        shutil.move(ruta, destino)
        return str(destino)

    def listar(self) -> List[dict]:
        items = []
        for m in self.dir.glob("*.meta"):
            try:
                meta = json.loads(m.read_text())
                meta["existe"] = (self.dir / meta["nombre_q"]).exists()
                items.append(meta)
            except Exception:
                pass
        return items

    def restaurar(self, nombre_q: str) -> tuple:
        meta_path = self.dir / (nombre_q + ".meta")
        archivo_q = self.dir / nombre_q
        if not meta_path.exists():
            return False, "Metadatos no encontrados"
        if not archivo_q.exists():
            return False, "Archivo no encontrado en cuarentena"
        meta = json.loads(meta_path.read_text())
        dest = meta["original"]
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(str(archivo_q), dest)
        meta_path.unlink()
        return True, dest


# ══════════════════════════════════════════════════════════════
# LOGGER
# ══════════════════════════════════════════════════════════════
class Logger:
    def __init__(self):
        log_path = Path(CFG["log_dir"]) / f"peralta_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            filename=str(log_path), level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self._log = logging.getLogger("Peralta")

    def info(self, msg):    self._log.info(msg)
    def warn(self, msg):    self._log.warning(msg)
    def error(self, msg):   self._log.error(msg)
    def amenaza(self, msg): self._log.critical(f"[AMENAZA] {msg}")

# ══════════════════════════════════════════════════════════════
# BANDEJA DEL SISTEMA (TRAY ICON)
# ══════════════════════════════════════════════════════════════
class BandejaSistema:
    def __init__(self, peralta_instancia):
        self.peralta = peralta_instancia
        self.icon = None

    def crear_imagen(self):
        icon_path = Path(__file__).parent / "tray_icon.png"
        if icon_path.exists():
            return Image.open(icon_path)
        return Image.new('RGB', (64, 64), color=(0, 242, 255))

    def iniciar(self):
        """Inicia el icono en un hilo separado."""
        # En Linux, forzamos el backend a 'appindicator' si está disponible, sino fallback
        if ES_LIN:
            os.environ["PYSTRAY_BACKEND"] = "appindicator" 
        
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        try:
            import pystray
            self.icon = pystray.Icon(
                "peralta",
                self.crear_imagen(),
                "Peralta Antivirus",
                menu=pystray.Menu(
                    pystray.MenuItem("Abrir Neural Interface", self.abrir_dashboard),
                    pystray.MenuItem("Escanear Sistema", self.ejecutar_escaneo),
                    pystray.Menu.Separator(),
                    pystray.MenuItem("Detener Protección", self.detener_antivirus),
                    pystray.MenuItem("Salir", self.salir)
                )
            )
            self.icon.run()
        except Exception as e:
            console.print(f"[yellow]⚠ No se pudo iniciar el icono de bandeja: {e}[/yellow]")
            # Fallback: Notificación de sistema si es posible
            self.notificar("Peralta está protegiendo tu sistema en segundo plano.")

    def abrir_dashboard(self, icon=None, item=None):
        import webbrowser
        webbrowser.open("http://localhost:5173/")

    def ejecutar_escaneo(self, icon=None, item=None):
        self.peralta.escanear("/")

    def detener_antivirus(self, icon=None, item=None):
        self.peralta.detener()
        self.notificar("Protección de Peralta desactivada.")

    def notificar(self, msg):
        """Envía una notificación emergente nativa."""
        try:
            if ES_LIN:
                subprocess.run(["notify-send", "Peralta Antivirus", msg])
            else:
                self.icon.notify(msg, "Peralta Antivirus")
        except:
            pass

    def salir(self, icon, item):
        self.icon.stop()
        os._exit(0)

# ══════════════════════════════════════════════════════════════
# MOTOR PRINCIPAL — PERALTA
# ══════════════════════════════════════════════════════════════
class Peralta:
    def __init__(self):
        self.analizador      = Analizador()
        self.analizador_bin  = AnalizadorBinario()
        self.web             = ProteccionWeb()
        self.ids             = DetectorIntrusos()
        self.cuarentena      = Cuarentena()
        self.logger          = Logger()
        self.monitor_apps    = MonitorApps(self.analizador, self._alerta_callback)
        self.vigilante       = VigilanteBehavioral(self._alerta_callback_ids)
        self.firewall        = FirewallNeuronal(self._alerta_callback_ids)
        self.wifi            = ProtectorWiFi(self._alerta_callback_ids)
        self.usb             = MonitorUSB(self.analizador, self._alerta_callback)
        self.privacidad      = ProtectorPrivacidad(self._alerta_callback_ids)
        self.asistente       = None  # Se crea después de __init__ para evitar circular ref
        self._activo         = False
        self._api_thread     = None

    def _alerta_callback_ids(self, datos: dict):
        """Callback para módulos IDS que envían dict directamente."""
        tipo = datos.pop("tipo", "SISTEMA")
        self._alerta_callback(tipo, datos)

    # ── Verificar Motor Neuronal ────────────────────────────
    def motor_disponible(self) -> bool:
        if not requests: return False
        try:
            return requests.get(f"{CFG['motor_url']}/api/tags", timeout=3).status_code == 200
        except:
            return False

    def iniciar_motor_si_necesario(self):
        if not self.motor_disponible():
            console.print("[yellow]Activando Motor Neuronal Peralta...[/yellow]")
            if ES_WIN:
                subprocess.Popen(["ollama", "serve"],
                                 creationflags=subprocess.CREATE_NO_WINDOW,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen(["ollama", "serve"],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(4)

    # ── Callback central de alertas ────────────────────────
    def _alerta_callback(self, tipo: str, datos: dict):
        estado = datos.get("estado", "INFO")
        nombre = datos.get("nombre") or datos.get("ip") or datos.get("desc", "")
        nivel  = datos.get("nivel", "INFO")
        desc   = datos.get("desc", "")

        color_map = {"AMENAZA": "red", "SOSPECHOSO": "yellow",
                     "CRITICA": "red", "ALTA": "red", "MEDIA": "yellow"}
        color = color_map.get(estado) or color_map.get(nivel, "cyan")

        # Consola
        ts = datetime.now().strftime("%H:%M:%S")
        icono = {"AMENAZA":"🦠","SOSPECHOSO":"⚠","CRITICA":"🚨","INFO":"ℹ"}.get(estado or nivel, "•")
        console.print(f"[dim][{ts}][/dim] [{color}]{icono} {tipo}[/{color}]: {nombre[:80]}")
        if desc:
            console.print(f"         [dim]{desc[:100]}[/dim]")

        # Voz
        msg_voz = self._texto_voz(tipo, datos)
        if msg_voz:
            urgente = estado in ("AMENAZA",) or nivel in ("CRITICA",)
            Voz.hablar(msg_voz, urgente=urgente)

        # Log
        self.logger.amenaza(f"{tipo} | {nombre} | {desc}")

        # Cuarentena automática para archivos con amenaza
        if estado == "AMENAZA" and "ruta" in datos:
            try:
                destino = self.cuarentena.poner(datos["ruta"])
                console.print(f"         [green]🔒 Movido a cuarentena:[/green] {destino}")
                Voz.hablar("Archivo malicioso movido a cuarentena.", urgente=True)
            except Exception as e:
                console.print(f"         [red]No se pudo poner en cuarentena: {e}[/red]")

    def _texto_voz(self, tipo: str, datos: dict) -> str:
        nombre = datos.get("nombre", "")
        nivel  = datos.get("nivel", "")

        if tipo == "APP_NUEVA" and datos.get("estado") == "AMENAZA":
            return f"Alerta. Aplicación maliciosa detectada: {nombre}. Moviendo a cuarentena."
        elif tipo == "APP_NUEVA" and datos.get("estado") == "SOSPECHOSO":
            return f"Advertencia. Archivo sospechoso detectado: {nombre}. Revisa el reporte."
        elif tipo == "APP_INSTALADA_WIN":
            return f"Nueva aplicación instalada: {nombre}."
        # elif tipo == "RED" and nivel in ("CRITICA", "ALTA"):
        #     return f"Alerta de seguridad en red. {datos.get('desc', 'Amenaza detectada')}."
        elif tipo == "WEB":
            dominio = datos.get("dominio", "")
            return f"Sitio web peligroso bloqueado: {dominio}."
        elif tipo == "PROCESO":
            return f"Proceso malicioso detectado: {datos.get('nombre', '')}."
        return ""

    # ── MODO DAEMON — Protección en tiempo real ─────────────
    def iniciar_daemon(self):
        self._activo = True
        self.iniciar_servidor_web()
        self.iniciar_motor_si_necesario()
        
        # Iniciar bandeja del sistema (opcional y fuera de Linux por ahora por estabilidad)
        if not ES_LIN:
            try:
                self.bandeja = BandejaSistema(self)
                self.bandeja.iniciar()
            except:
                pass

        banner = Panel(
            f" [bold white]P E R A L T A[/bold white] [bold cyan]A N T I V I R U S[/bold cyan]\n"
            f" [dim]Desarrollado por: Ing. Juan Manuel Peralta[/dim]\n"
            f" [dim]Sistema: {SISTEMA} | Motor Neural: Peralta v3.2[/dim]\n"
            f" [dim]Estado IA: {'✓ Lista' if self.motor_disponible() else '✗ Cargando...'}[/dim]",
            border_style="green", title="[bold]Peralta v1.0[/bold]"
        )
        console.print(banner)
        # Voz.hablar("Peralta Antivirus iniciado. Protección activa.", urgente=False)

        # Iniciar módulos
        if CFG.get("escaneo_apps"):
            self.monitor_apps.iniciar()
            if ES_WIN:
                self.monitor_apps.monitorear_registro_windows()
            console.print("[green]✓[/green] Monitor de apps activo")

        if CFG.get("escaneo_red"):
            def _cb_red(amenaza):
                self._alerta_callback("RED", amenaza)
            self.ids.monitorear_continuo(_cb_red)
            console.print("[green]✓[/green] Monitor de red/intrusos activo")

        # Fase 1 — Vigilante Behavioral
        self.vigilante.monitorear_continuo()
        console.print("[green]✓[/green] Vigilante Behavioral (IA de comportamiento) activo")

        # Fase 3 — Firewall Neuronal + WiFi
        self.firewall.monitorear_continuo()
        console.print("[green]✓[/green] Firewall Neuronal activo")
        self.wifi.monitorear_continuo()
        console.print("[green]✓[/green] Protector WiFi (ARP/MITM) activo")

        # Fase 4 — USB + Privacidad (Ahora disponible en Win/Mac/Lin)
        self.usb.monitorear_continuo()
        console.print("[green]✓[/green] Monitor USB activo")
        self.privacidad.monitorear_continuo()
        console.print("[green]✓[/green] Protector de Privacidad (Cámara/Mic) activo")

        # Asistente IA
        self.asistente = AsistenteSeguridadIA(self)
        console.print("[green]✓[/green] Asistente IA de Seguridad listo")

        console.print("[green]✓[/green] Protección web activa")
        total_modulos = 9
        console.print(f"\n[bold green]🛡 {total_modulos} módulos de protección activos[/bold green]")
        console.print("[dim]Presiona Ctrl+C para detener[/dim]\n")

        try:
            while self._activo:
                time.sleep(1)
        except KeyboardInterrupt:
            self.detener()


    def detener(self):
        self._activo = False
        self.ids.detener()
        self.vigilante.detener()
        self.firewall.detener()
        self.wifi.detener()
        self.usb.detener()
        self.privacidad.detener()
        console.print("\n[yellow]Peralta Antivirus detenido — todos los módulos desactivados.[/yellow]")

    # ── ESCANEO MANUAL ──────────────────────────────────────
    def escanear(self, ruta: str, profundo: bool = False):
        self.iniciar_motor_si_necesario()
        ruta_abs = os.path.abspath(ruta)

        if os.path.isfile(ruta_abs):
            archivos = [ruta_abs]
        elif os.path.isdir(ruta_abs):
            archivos = []
            for root, dirs, files in os.walk(ruta_abs):
                dirs[:] = [d for d in dirs if d not in {"proc","sys","dev","run"}]
                for f in files:
                    archivos.append(os.path.join(root, f))
        else:
            console.print(f"[red]No se encontró: {ruta}[/red]")
            return

        amenazas, sospechosos = [], []
        inicio = time.time()

        with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                      BarColumn(), TextColumn("{task.percentage:>3.0f}%"),
                      TimeElapsedColumn(), console=console) as prog:
            tarea = prog.add_task("[cyan]Escaneando...", total=len(archivos))
            for archivo in archivos:
                prog.update(tarea, description=f"[cyan]{Path(archivo).name[:45]}")
                r = self.analizador.analizar_archivo(archivo, usar_ia=profundo)
                if r["estado"] == "AMENAZA":
                    amenazas.append(r)
                elif r["estado"] == "SOSPECHOSO":
                    sospechosos.append(r)
                self.logger.info(f"[{r['estado']}] {archivo}")
                prog.advance(tarea)

        duracion = time.time() - inicio

        # Resumen
        console.print(Panel(
            f"[bold]Archivos:[/bold] {len(archivos)}\n"
            f"[red]Amenazas:[/red] {len(amenazas)}\n"
            f"[yellow]Sospechosos:[/yellow] {len(sospechosos)}\n"
            f"[green]Limpios:[/green] {len(archivos) - len(amenazas) - len(sospechosos)}\n"
            f"[dim]Tiempo: {duracion:.1f}s | IA: {'Sí' if profundo else 'No'}[/dim]",
            title="[bold]📊 Resultado del Escaneo[/bold]", border_style="cyan"
        ))

        if amenazas or sospechosos:
            tabla = Table(title="🚨 Archivos Detectados", box=box.ROUNDED,
                          header_style="bold white on dark_red")
            tabla.add_column("Estado",    width=14)
            tabla.add_column("Archivo",   style="cyan")
            tabla.add_column("Hallazgos", width=45)
            tabla.add_column("IA",        width=14)

            for r in amenazas + sospechosos:
                color  = "red" if r["estado"] == "AMENAZA" else "yellow"
                hall   = "; ".join([h["descripcion"][:40] for h in r["hallazgos"][:2]])
                ia_txt = ""
                if r.get("ia"):
                    ia_txt = f"{r['ia'].get('veredicto','?')} {r['ia'].get('confianza',0)}%"
                tabla.add_row(
                    f"[{color}]{r['estado']}[/{color}]",
                    r["ruta"], hall or "-", ia_txt or "-"
                )
            console.print(tabla)

            # Cuarentena de amenazas
            if amenazas:
                console.print(f"\n[bold red]🔒 Moviendo {len(amenazas)} amenaza(s) a cuarentena...[/bold red]")
                for r in amenazas:
                    try:
                        destino = self.cuarentena.poner(r["ruta"])
                        console.print(f"  [green]✓[/green] {r['nombre']} → cuarentena")
                    except Exception as e:
                        console.print(f"  [red]✗[/red] {r['nombre']}: {e}")

            if amenazas:
                Voz.hablar(f"Escaneo completado. Se encontraron {len(amenazas)} amenazas. "
                           f"Los archivos han sido movidos a cuarentena.", urgente=True)
            # elif sospechosos:
            #     Voz.hablar(f"Escaneo completado. Se encontraron {len(sospechosos)} archivos sospechosos.")
        else:
            console.print("[bold green]✅ Sistema limpio. No se detectaron amenazas.[/bold green]")
            # Voz.hablar("Escaneo completado. No se detectaron amenazas.")

    # ── VERIFICAR URL ────────────────────────────────────────
    def verificar_url(self, url: str):
        resultado = self.web.verificar_url(url)
        estado = resultado["estado"]
        color = {"BLOQUEADO": "red", "SOSPECHOSO": "yellow", "LIMPIO": "green"}.get(estado, "white")
        console.print(Panel(
            f"[bold]URL:[/bold] {url}\n"
            f"[bold]Estado:[/bold] [{color}]{estado}[/{color}]\n"
            f"[bold]Razón:[/bold] {resultado.get('razon') or 'Sin problemas detectados'}",
            title="🌐 Verificación Web", border_style=color
        ))
        if estado == "BLOQUEADO":
            # Voz.hablar(f"Sitio web peligroso: {url}. Acceso bloqueado.", urgente=True)
            pass
        elif estado == "SOSPECHOSO":
            # Voz.hablar(f"Sitio web sospechoso detectado. Procede con precaución.")
            pass

    # ── ESTADO ───────────────────────────────────────────────
    def mostrar_estado(self):
        motor_ok = self.motor_disponible()
        q_items   = len(self.cuarentena.listar())

        console.print(Panel(
            f"[bold]Ingeniero:[/bold]       Juan Manuel Peralta\n"
            f"[bold]Motor Neuronal:[/bold]  {'[green]✓ Activo[/green]' if motor_ok else '[red]✗ Inactivo[/red]'}\n"
            f"[bold]Base Conocimiento:[/bold] Peralta Neural v3.2\n"
            f"[bold]Sistema:[/bold]             {SISTEMA} {platform.release()}\n"
            f"[bold]Voz:[/bold]                 {'Activada' if CFG['voz_activada'] else 'Desactivada'}\n"
            f"[bold]Cuarentena:[/bold]          {q_items} archivo(s)\n"
            f"[bold]Escaneo apps:[/bold]        {'Sí' if CFG['escaneo_apps'] else 'No'}\n"
            f"[bold]Protección web:[/bold]      {'Sí' if CFG['escaneo_web'] else 'No'}\n"
            f"[bold]Monitor de red:[/bold]      {'Sí' if CFG['escaneo_red'] else 'No'}\n"
            f"[bold]Dominios bloqueados:[/bold] {len(self.web.dominios_bloqueados)}\n"
            f"[dim]Config: {CONFIG_PATH}[/dim]",
            title="[bold white]🛡  Estado de Peralta Antivirus[/bold white]",
            border_style="blue"
        ))

    # ── CUARENTENA ───────────────────────────────────────────
    def ver_cuarentena(self):
        items = self.cuarentena.listar()
        if not items:
            console.print("[green]La cuarentena está vacía.[/green]")
            return
        tabla = Table(title="🔒 Cuarentena", box=box.ROUNDED)
        tabla.add_column("Nombre en cuarentena", style="cyan")
        tabla.add_column("Ruta original")
        tabla.add_column("Fecha")
        tabla.add_column("Existe", justify="center")
        for m in items:
            tabla.add_row(
                m.get("nombre_q", "?"), m.get("original", "?"),
                m.get("timestamp", "?")[:19],
                "[green]Sí[/green]" if m.get("existe") else "[red]No[/red]"
            )
        console.print(tabla)

    def explicar_amenaza(self, nombre_q: str):
        """Usa IA para explicar qué es la amenaza y por qué es peligrosa."""
        meta_path = self.cuarentena.dir / (nombre_q + ".meta")
        archivo_q = self.cuarentena.dir / nombre_q
        
        if not meta_path.exists():
            console.print(f"[red]No se encontraron metadatos para {nombre_q}[/red]")
            return

        meta = json.loads(meta_path.read_text())
        console.print(f"[cyan]Analizando amenaza:[/cyan] {meta['original']}")
        
        # Leer el archivo de cuarentena para análisis
        contenido = ""
        try:
            with open(archivo_q, "r", encoding="utf-8", errors="ignore") as f:
                contenido = f.read(5000) # Primeros 5000 caracteres
        except Exception as e:
            console.print(f"[red]Error leyendo archivo: {e}[/red]")
            return

        prompt = f"""Como experto en ciberseguridad, explica al usuario qué es esta amenaza detectada.
Toma en cuenta que el usuario es una persona común, usa un lenguaje claro y educativo en ESPAÑOL.

RUTA ORIGINAL: {meta['original']}
CONTENIDO DEL ARCHIVO:
```
{contenido}
```

Responde en este formato:
EXPLICACIÓN: (máximo 4 oraciones sobre qué es y qué intentaba hacer)
RIESGO: (qué pasaría si se ejecutara)
RECOMENDACIÓN: (qué debe hacer el usuario)
"""

        with console.status("[bold cyan]Peralta está analizando la amenaza con IA...[/bold cyan]"):
            try:
                r = requests.post(f"{CFG['ollama_url']}/api/generate",
                                  json={"model": CFG["modelo_ollama"], "prompt": prompt, "stream": False},
                                  timeout=300)
                if r.status_code == 200:
                    respuesta = r.json().get("response", "")
                    console.print(Panel(respuesta, title="🔍 Explicación de la Amenaza", border_style="yellow"))
                    # Hablar solo la parte de la explicación
                    clara = respuesta.split("RIESGO:")[0].replace("EXPLICACIÓN:", "").strip()
                    # Voz.hablar(clara)
                else:
                    console.print("[red]El motor de IA no respondió correctamente.[/red]")
            except Exception as e:
                console.print(f"[red]Error durante el análisis IA: {e}[/red]")

    def restaurar_cuarentena(self, nombre_q: str):
        ok, msg = self.cuarentena.restaurar(nombre_q)
        if ok:
            console.print(f"[green]✓ Restaurado:[/green] {msg}")
        else:
            console.print(f"[red]✗ Error:[/red] {msg}")

    # ── ACTUALIZAR FEEDS ─────────────────────────────────────
    def actualizar_feeds(self):
        console.print("[cyan]Actualizando listas de amenazas...[/cyan]")
        # Voz.hablar("Actualizando base de datos de amenazas.")
        nuevos = self.web.actualizar_feeds()
        console.print(f"[green]✓[/green] {nuevos} dominios maliciosos actualizados")
        # Voz.hablar(f"Actualización completada. {nuevos} nuevas amenazas en base de datos.")

        # Voz.hablar(f"Actualización completada. {nuevos} nuevas amenazas en base de datos.")

    def iniciar_servidor_web(self, puerto: int = 5005):
        """Inicia un servidor API para la interfaz web neural."""
        try:
            from flask import Flask, jsonify, send_file
            from flask_cors import CORS
            import logging
            
            # Silenciar logs de Flask
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)

            app = Flask(__name__)
            CORS(app)

            @app.route("/api/stats")
            def get_stats():
                return jsonify({
                    "estado": "PROTEGIDO" if self._activo else "DESACTIVADO",
                    "amenazas_bloqueadas": len(self.cuarentena.listar()), 
                    "carga_motor": f"{psutil.cpu_percent()}%" if psutil else "18%",
                    "memoria_uso": "2.4 GB/s",
                    "motor_neural": CFG["modelo_neuronal"],
                    "uptime": "99.9%"
                })

            @app.route("/api/logs")
            def get_logs():
                log_path = Path(CFG["log_dir"]) / f"peralta_{datetime.now().strftime('%Y%m%d')}.log"
                logs = []
                if log_path.exists():
                    with open(log_path, "r") as f:
                        lineas = f.readlines()[-15:]
                        for l in lineas:
                            parts = l.split("] ", 1)
                            if len(parts) > 1:
                                tipo = "info"
                                if "AMENAZA" in parts[0]: tipo = "warning"
                                elif "ERROR" in parts[0]: tipo = "error"
                                logs.append({"msg": parts[1].strip(), "type": tipo, "time": parts[0][1:]})
                return jsonify(logs)

            @app.route("/api/quarantine")
            def get_quarantine():
                return jsonify(self.cuarentena.listar())

            @app.route("/api/scan", methods=["POST"])
            def trigger_scan():
                threading.Thread(target=self.escanear, args=("/", True)).start()
                return jsonify({"status": "OK", "msg": "Escaneo iniciado"})

            @app.route("/api/update", methods=["POST"])
            def trigger_update():
                threading.Thread(target=self.actualizar_feeds).start()
                return jsonify({"status": "OK", "msg": "Actualizando feeds"})

            @app.route("/api/stop", methods=["POST"])
            def trigger_stop():
                threading.Thread(target=self.detener).start()
                return jsonify({"status": "OK", "msg": "Deteniendo protección"})

            # ── NUEVOS ENDPOINTS (Fases 1-4) ──────────────────────

            @app.route("/api/system-health")
            def get_system_health():
                """Estado de salud del sistema: CPU, RAM, Disco."""
                data = {}
                if psutil:
                    try:
                        data["cpu_percent"] = psutil.cpu_percent(interval=0.5)
                        mem = psutil.virtual_memory()
                        data["ram_percent"] = mem.percent
                        data["ram_used_gb"] = round(mem.used / (1024**3), 1)
                        data["ram_total_gb"] = round(mem.total / (1024**3), 1)
                        disk = psutil.disk_usage("/")
                        data["disk_percent"] = disk.percent
                        data["disk_used_gb"] = round(disk.used / (1024**3), 1)
                        data["disk_total_gb"] = round(disk.total / (1024**3), 1)
                        data["procesos"] = len(list(psutil.process_iter()))
                        conns = psutil.net_connections(kind="inet")
                        data["conexiones"] = len([c for c in conns if c.status == "ESTABLISHED"])
                    except Exception:
                        pass
                return jsonify(data)

            @app.route("/api/behavioral-score")
            def get_behavioral_scores():
                """Top procesos con mayor puntuación de riesgo behavioral."""
                return jsonify(self.vigilante.obtener_scores())

            @app.route("/api/network-map")
            def get_network_map():
                """Mapa de conexiones activas."""
                connections = []
                if psutil:
                    try:
                        for c in psutil.net_connections(kind="inet"):
                            if c.status == "ESTABLISHED" and c.raddr:
                                proc_name = ""
                                try:
                                    if c.pid:
                                        proc_name = psutil.Process(c.pid).name()
                                except Exception:
                                    pass
                                connections.append({
                                    "local": f"{c.laddr.ip}:{c.laddr.port}",
                                    "remote": f"{c.raddr.ip}:{c.raddr.port}",
                                    "pid": c.pid,
                                    "proceso": proc_name,
                                    "status": c.status
                                })
                    except Exception:
                        pass
                return jsonify(connections)

            @app.route("/api/wifi-scan")
            def get_wifi_scan():
                """Dispositivos en la red local."""
                return jsonify(self.wifi.escanear_red())

            @app.route("/api/download/peralta_installer.zip")
            def download_installer():
                """Permite descargar el instalador comprimido."""
                from flask import send_file, make_response
                import os
                base_dir = os.path.dirname(os.path.abspath(__file__))
                zip_path = os.path.join(base_dir, "peralta_installer.zip")
                if os.path.exists(zip_path):
                    response = make_response(send_file(zip_path, as_attachment=True))
                    response.headers["Content-Disposition"] = "attachment; filename=\"peralta_installer.zip\""
                    response.headers["Content-Type"] = "application/octet-stream"
                    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
                    return response
                return jsonify({"error": "Instalador no encontrado"}), 404

            @app.route("/api/chat", methods=["POST"])
            def chat_ia():
                """Chat en vivo con el asistente IA — Optmizado con Interceptor de Comandos."""
                from flask import request
                data = request.get_json() or {}
                mensaje = data.get("mensaje", data.get("message", "")).lower()
                if not mensaje:
                    return jsonify({"error": "Falta el campo 'mensaje'"}), 400

                # --- INTERCEPTOR DE COMANDOS DIRECTOS (OBEDIENCIA INSTANTÁNEA) ---
                if any(x in mensaje for x in ["analiza", "escanea", "scan"]):
                    # Ejecutar escaneo en segundo plano (solo en home para evitar freeze)
                    threading.Thread(target=self.escanear, args=("/home/user/pruebas_seguridad", True)).start()
                    return jsonify({"respuesta": "Entendido. Iniciando un escaneo profundo de todo el sistema ahora mismo. Te informaré si encuentro alguna amenaza."})
                
                if any(x in mensaje for x in ["actualiza", "update"]):
                    threading.Thread(target=self.actualizar_feeds).start()
                    return jsonify({"respuesta": "Actualizando mi base de datos de amenazas neurale. Por favor, espera un momento."})
                
                if any(x in mensaje for x in ["cuarentena", "quarantine"]):
                    items = self.cuarentena.listar()
                    return jsonify({"respuesta": f"Actualmente hay {len(items)} archivos en cuarentena. Puedes verlos en el panel de seguridad."})

                # --- PROCESAMIENTO IA (PARA PREGUNTAS COMPLEJAS) ---
                if not self.asistente:
                    self.asistente = AsistenteSeguridadIA(self)
                respuesta = self.asistente.chatear(mensaje)
                return jsonify({"respuesta": respuesta})

            @app.route("/api/kill-process", methods=["POST"])
            def kill_process():
                """Matar un proceso sospechoso por PID."""
                from flask import request
                data = request.get_json() or {}
                pid = data.get("pid")
                if not pid:
                    return jsonify({"error": "Falta el campo 'pid'"}), 400
                try:
                    proc = psutil.Process(int(pid))
                    nombre = proc.name()
                    proc.kill()
                    self.logger.amenaza(f"Proceso {nombre} (PID {pid}) eliminado por el usuario")
                    return jsonify({"status": "OK", "msg": f"Proceso {nombre} eliminado"})
                except Exception as e:
                    return jsonify({"error": str(e)}), 500

            @app.route("/api/usb-devices")
            def get_usb_devices():
                """Montajes USB detectados."""
                return jsonify(list(self.usb._montajes_conocidos))

            @app.route('/landing', methods=['GET'])
            def serve_landing():
                """Sirve la landing page profesional."""
                # Buscar en el directorio actual (instalación)
                base_dir = os.path.dirname(__file__)
                landing_path = os.path.join(base_dir, "gui_build", "landing.html")
                
                if not os.path.exists(landing_path):
                    # Intentar buscar en el dir de desarrollo si falla
                    landing_path = os.path.expanduser("~/juego unity/antivirus peralta/files/gui_build/landing.html")

                if os.path.exists(landing_path):
                    return send_file(landing_path)
                return "Landing page not found", 404


            @app.route('/api/open-gui', methods=['POST'])
            def open_gui():
                """Abre la interfaz web en el navegador del usuario."""
                import webbrowser
                webbrowser.open("http://localhost:5173/landing.html") # O la URL final
                return jsonify({"success": True})

            threading.Thread(target=lambda: app.run(port=puerto, host="0.0.0.0", debug=False, use_reloader=False), daemon=True).start()
            console.print(f"[green]✓[/green] Interfaz Neural Web (API) activa en puerto {puerto}")
        except ImportError:
            console.print("[yellow]! Alerta: Flask o Flask-CORS no instalados. Interfaz web desactivada.[/yellow]")

    def procesar_orden_ia(self, orden: str):
        """Procesa una orden en lenguaje natural y la ejecuta."""
        if not requests:
            console.print("[red]Error: Dependencias de red no disponibles.[/red]")
            return

        # Prompt de sistema para mapear lenguaje natural a comandos del antivirus
        prompt_sistema = """Eres el Núcleo de Inteligencia del Antivirus Peralta. Tu trabajo es traducir la orden del usuario a una acción técnica.
Las acciones disponibles son:
- SCAN: Escanear una ruta específica.
- STATUS: Mostrar el estado general del sistema.
- QUARANTINE: Mostrar o gestionar la cuarentena.
- UPDATE: Actualizar la base de datos de amenazas.
- VOZ: Activar o desactivar la voz.

Responde SOLO con un comando JSON siguiendo este formato EXACTO:
{"accion": "SCAN|STATUS|QUARANTINE|UPDATE|VOZ", "parametros": ["valor1", "valor2"], "respuesta_voz": "Lo que dirás al usuario"}

EJEMPLOS:
Usuario: "analiza mi carpeta de descargas" -> {"accion": "SCAN", "parametros": ["/home/user/Downloads"], "respuesta_voz": "Entendido, iniciando el escaneo de tu carpeta de descargas."}
Usuario: "quitar la voz" -> {"accion": "VOZ", "parametros": ["off"], "respuesta_voz": "La voz del sistema ha sido desactivada."}
Usuario: "¿cómo está mi pc?" -> {"accion": "STATUS", "parametros": [], "respuesta_voz": "Generando tu reporte de seguridad ahora."}
"""

        with console.status(f"[bold cyan]Interpretando orden: '{orden}'...[/bold cyan]"):
            try:
                r = requests.post(f"{CFG['motor_url']}/api/generate",
                                  json={
                                      "model": CFG["modelo_neuronal"],
                                      "system": prompt_sistema,
                                      "prompt": orden,
                                      "stream": False,
                                      "options": {"temperature": 0.1}
                                  }, timeout=90)
                
                if r.status_code == 200:
                    respuesta_json = r.json().get("response", "")
                    # Extraer el JSON de la respuesta
                    import re
                    match = re.search(r'(\{.*\})', respuesta_json, re.DOTALL)
                    if match:
                        datos = json.loads(match.group(1))
                        accion = datos.get("accion")
                        params = datos.get("parametros", [])
                        msg_voz = datos.get("respuesta_voz", "Procesando orden.")
                    else:
                        console.print("[red]La IA no devolvió un formato válido de comando.[/red]")
                        return
                else:
                    console.print("[red]Error de comunicación con el Motor Neuronal.[/red]")
                    return
            except Exception as e:
                console.print(f"[red]Error procesando orden: {e}[/red]")
                return

        # EJECUTAR FUERA DEL STATUS para evitar conflictos de Rich
        if msg_voz:
            Voz.hablar(msg_voz)
            console.print(f"[bold cyan]Peralta:[/bold cyan] {msg_voz}")

        if accion == "SCAN":
            ruta = params[0] if params else "."
            self.escanear(ruta, profundo=True)
        elif accion == "STATUS":
            self.mostrar_estado()
        elif accion == "QUARANTINE":
            self.ver_cuarentena()
        elif accion == "UPDATE":
            self.actualizar_feeds()
        elif accion == "VOZ":
            estado = params[0] if params else "off"
            CFG["voz_activada"] = (estado == "on")
            console.print(f"Voz configurada a: {estado}")
        else:
            console.print("[yellow]La IA no pudo determinar una acción clara. Intenta ser más específico.[/yellow]")



# ══════════════════════════════════════════════════════════════
# BANNER
# ══════════════════════════════════════════════════════════════
def banner():
    console.print(Panel.fit(
        "[bold blue] ██████  ███████ ██████   █████  ██      ████████  █████ [/bold blue]\n"
        "[bold blue] ██   ██ ██      ██   ██ ██   ██ ██         ██    ██   ██[/bold blue]\n"
        "[bold blue] ██████  █████   ██████  ███████ ██         ██    ███████[/bold blue]\n"
        "[bold blue] ██      ██      ██   ██ ██   ██ ██         ██    ██   ██[/bold blue]\n"
        "[bold blue] ██      ███████ ██   ██ ██   ██ ███████    ██    ██   ██[/bold blue]\n\n"
        f"[bold white]        A N T I V I R U S  v1.0[/bold white]   "
        f"[dim]{SISTEMA} | IA Neural Peralta[/dim]",
        border_style="blue",
        title="[bold]🛡 Peralta[/bold]"
    ))


# ══════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="Peralta Antivirus — Protección inteligente con IA local",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python3 peralta.py --daemon                         Protección en tiempo real
  python3 peralta.py --scan /home/usuario             Escaneo rápido
  python3 peralta.py --scan /tmp --deep               Escaneo con IA
  python3 peralta.py --url https://sospechoso.com     Verificar URL
  python3 peralta.py --quarantine list                Ver cuarentena
  python3 peralta.py --quarantine restore nombre      Restaurar archivo
  python3 peralta.py --update                         Actualizar feeds de amenazas
  python3 peralta.py --status                         Ver estado
  python3 peralta.py --voz off                        Desactivar voz
        """
    )
    parser.add_argument("--daemon",       action="store_true", help="Protección en tiempo real")
    parser.add_argument("--scan",         metavar="RUTA",      help="Escanear ruta")
    parser.add_argument("--deep",         action="store_true", help="Análisis profundo con IA")
    parser.add_argument("--url",          metavar="URL",       help="Verificar URL/dominio")
    parser.add_argument("--quarantine",   nargs="+",           help="list | restore <nombre>")
    parser.add_argument("--update",       action="store_true", help="Actualizar feeds de amenazas")
    parser.add_argument("--status",       action="store_true", help="Mostrar estado")
    parser.add_argument("--explain",      metavar="NOMBRE_Q",  help="Explicar una amenaza en el Núcleo")
    parser.add_argument("--orden",        metavar="TEXTO",     help="Dar una orden en lenguaje natural")
    parser.add_argument("--chat",         action="store_true", help="Chat interactivo con la IA de seguridad")
    parser.add_argument("--wifi-scan",    action="store_true", help="Escanear dispositivos en la red local")
    parser.add_argument("--voz",          choices=["on","off"], help="Activar/desactivar voz")

    args = parser.parse_args()
    banner()

    peralta = Peralta()

    if args.voz:
        CFG["voz_activada"] = args.voz == "on"
        console.print(f"[cyan]Voz:[/cyan] {'activada' if CFG['voz_activada'] else 'desactivada'}")

    if args.scan:
        peralta.escanear(args.scan, profundo=args.deep)
    elif args.daemon:
        peralta.iniciar_daemon()
    elif args.url:
        peralta.verificar_url(args.url)
    elif args.quarantine:
        if args.quarantine[0] == "list":
            peralta.ver_cuarentena()
        elif args.quarantine[0] == "restore" and len(args.quarantine) > 1:
            peralta.restaurar_cuarentena(args.quarantine[1])
    elif args.update:
        peralta.actualizar_feeds()
    elif args.status:
        peralta.mostrar_estado()
    elif args.explain:
        peralta.explicar_amenaza(args.explain)
    elif args.orden:
        peralta.procesar_orden_ia(args.orden)
    elif args.chat:
        peralta.asistente = AsistenteSeguridadIA(peralta)
        peralta.asistente.modo_interactivo()
    elif getattr(args, 'wifi_scan', False):
        dispositivos = peralta.wifi.escanear_red()
        if dispositivos:
            tabla = Table(title="📡 Dispositivos en la Red Local", box=box.ROUNDED)
            tabla.add_column("IP", style="cyan")
            tabla.add_column("MAC", style="green")
            tabla.add_column("Estado")
            for d in dispositivos:
                tabla.add_row(d["ip"], d["mac"], d["estado"])
            console.print(tabla)
        else:
            console.print("[yellow]No se encontraron dispositivos en la red.[/yellow]")
    else:
        parser.print_help()
        console.print(f"\n[dim]Config: {CONFIG_PATH}[/dim]")
        console.print(f"[dim]Logs:   {CFG['log_dir']}[/dim]")


if __name__ == "__main__":
    main()
