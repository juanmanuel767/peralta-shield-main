#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║   PERALTA ANTIVIRUS — INSTALADOR AUTOMÁTICO          ║
║   Desarrollado por: Ing. Juan Manuel Peralta         ║
║   Compatible: Linux / Windows 10/11 / macOS          ║
╚══════════════════════════════════════════════════════╝

Ejecutar como administrador / sudo:
  Linux:   sudo python3 instalar_peralta.py
  Windows: python instalar_peralta.py  (como Administrador)
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import shutil
import time
import json
from pathlib import Path
import webbrowser


# ─────────────────────────────────────────────
SISTEMA = platform.system()  # "Linux" | "Windows" | "Darwin"
ES_WINDOWS = SISTEMA == "Windows"
ES_LINUX = SISTEMA == "Linux"
ES_MAC = SISTEMA == "Darwin"
VERSION = "1.0.0"

# Colores ANSI
R = "\033[91m"; G = "\033[92m"; Y = "\033[93m"
C = "\033[96m"; B = "\033[1m"; X = "\033[0m"

OLLAMA_MODELOS = ["llama3.2", "llama3.2:1b", "llama3"]

def titulo():
    os.system("cls" if ES_WINDOWS else "clear")
    print(f"""{C}{B}
  ██████  ███████ ██████   █████  ██      ████████  █████
  ██████  █████   ██████  ███████ ██         ██    ███████
  ██      ██      ██   ██ ██   ██ ██         ██    ██   ██
  ██      ███████ ██   ██ ██   ██ ███████    ██    ██   ██

         A N T I V I R U S  —  I N S T A L A D O R
         Ing. Juan Manuel Peralta | IA Neural Propietaria
    
""")

def paso(n, total, msg):
    print(f"\n{C}[{n}/{total}]{X} {B}{msg}{X}")

def ok(msg):    print(f"  {G}✓{X} {msg}")
def fallo(msg): print(f"  {R}✗{X} {msg}")
def info(msg):  print(f"  {Y}→{X} {msg}")

# ══════════════════════════════════════════════
# 1. VERIFICAR PYTHON
# ══════════════════════════════════════════════
def verificar_python():
    paso(1, 7, "Verificando Python")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        fallo(f"Python {version.major}.{version.minor} detectado. Se requiere Python 3.8+")
        sys.exit(1)
    ok(f"Python {version.major}.{version.minor}.{version.micro}")

# ══════════════════════════════════════════════
# 2. INSTALAR DEPENDENCIAS PYTHON
# ══════════════════════════════════════════════
def instalar_dependencias():
    paso(2, 7, "Instalando dependencias Python")
    paquetes = [
        "requests",
        "rich",
        "watchdog",
        "pyttsx3",
        "psutil",
        "dnspython",
        "pystray",
        "Pillow",
        "flask",
        "flask-cors",
        "yara-python",
    ]
    # En Windows necesitamos extras
    if ES_WINDOWS:
        paquetes += ["pywin32", "winapps"]

    for pkg in paquetes:
        info(f"Instalando {pkg}...")
        try:
            resultado = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg, "--quiet",
                 "--break-system-packages" if (ES_LINUX or ES_MAC) else ""],
                capture_output=True, text=True, timeout=120
            )
            if resultado.returncode == 0:
                ok(pkg)
            else:
                # Intentar sin --break-system-packages
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                    capture_output=True, timeout=120
                )
                ok(f"{pkg} (modo alternativo)")
        except Exception as e:
            fallo(f"{pkg}: {e}")

# ══════════════════════════════════════════════
# 3. INSTALAR OLLAMA
# ══════════════════════════════════════════════
def ollama_instalado() -> bool:
    return shutil.which("ollama") is not None

def instalar_ollama():
    paso(3, 7, "Configurando Motor Neuronal Peralta (Cerebro IA)")

    if ollama_instalado():
        ok("Motor Neuronal ya está configurado")
        return

    if ES_LINUX:
        info("Descargando componentes del Motor Neuronal...")
        try:
            subprocess.run(
                "curl -fsSL https://ollama.com/install.sh | sh > /dev/null 2>&1",
                shell=True, check=True
            )
            ok("Motor Neuronal configurado en Linux")
        except subprocess.CalledProcessError:
            fallo("Error configurando el Motor Neuronal.")

    if not ES_LINUX:
        if ES_WINDOWS:
            url = "https://ollama.com/download/OllamaSetup.exe"
            ext = ".exe"
        elif ES_MAC:
            url = "https://ollama.com/download/Ollama-darwin.zip"
            ext = ".zip"
        else:
            url = "https://ollama.com/install.sh"
            ext = ".sh"

        destino = Path(os.environ.get("TEMP", "/tmp")) / f"NeuralSetup{ext}"
        info(f"Descargando componentes del Motor Neuronal...")
        try:
            urllib.request.urlretrieve(url, destino)
            info("Configurando Motor Neuronal...")
            if ES_WINDOWS:
                subprocess.run([str(destino), "/S"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                ok("Motor Neuronal configurado en Windows")
            elif ES_MAC:
                info("En macOS, abre el archivo .zip descargado para instalar Ollama.")
                info(f"Ruta: {destino}")
        except Exception as e:
            fallo(f"Error: {e}")
            info("Descarga manual: https://ollama.com/download")

# ══════════════════════════════════════════════
# 4. INICIAR OLLAMA Y DESCARGAR MODELO
# ══════════════════════════════════════════════
def iniciar_ollama():
    """Inicia ollama serve en background."""
    import subprocess
    try:
        if ES_WINDOWS:
            subprocess.Popen(["ollama", "serve"],
                             creationflags=subprocess.CREATE_NO_WINDOW,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(["ollama", "serve"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
    except FileNotFoundError:
        pass

def descargar_modelo():
    paso(4, 7, "Sincronizando Base de Datos de Inteligencia")

    if not ollama_instalado():
        fallo("Motor Neuronal no disponible")
        return None

    iniciar_ollama()

    for modelo in OLLAMA_MODELOS:
        try:
            info(f"Sincronizando núcleo de conocimiento...")
            resultado = subprocess.run(
                ["ollama", "pull", modelo],
                capture_output=True, timeout=600
            )
            if resultado.returncode == 0:
                ok(f"Base de datos sincronizada")
                return modelo
        except subprocess.TimeoutExpired:
            fallo(f"Timeout descargando {modelo}")
        except Exception as e:
            info(f"No disponible: {modelo}")

    fallo("No se pudo descargar ningún modelo. Verifica tu conexión a internet.")
    info("Puedes descargarlo después con: ollama pull llama3")
    return None

# ══════════════════════════════════════════════
# 5. CREAR DIRECTORIO DE INSTALACIÓN
# ══════════════════════════════════════════════
def crear_directorio():
    paso(5, 7, "Creando directorio de instalación")

    if ES_WINDOWS:
        install_dir = Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "Peralta"
    elif ES_MAC:
        install_dir = Path.home() / "Library" / "Application Support" / "Peralta"
    else:
        install_dir = Path.home() / ".local" / "share" / "peralta"

    install_dir.mkdir(parents=True, exist_ok=True)

    # Crear subdirectorios
    for sub in ["quarantine", "logs", "db", "config"]:
        (install_dir / sub).mkdir(exist_ok=True)

    ok(f"Directorio creado: {install_dir}")

    # Copiar peralta.py al directorio de instalación
    script_dir = Path(__file__).parent
    peralta_src = script_dir / "peralta.py"
    if peralta_src.exists():
        shutil.copy2(peralta_src, install_dir / "peralta.py")
        ok("peralta.py copiado")

    # Copiar tray_icon.png
    tray_icon_src = script_dir / "tray_icon.png"
    if tray_icon_src.exists():
        shutil.copy2(tray_icon_src, install_dir / "tray_icon.png")
        ok("tray_icon.png copiado")

    return install_dir

# ══════════════════════════════════════════════
# 6. CREAR SERVICIO / AUTOARRANQUE
# ══════════════════════════════════════════════
def crear_servicio(install_dir: Path, modelo: str):
    paso(6, 7, "Configurando autoarranque del sistema")

    if ES_LINUX:
        servicio = f"""[Unit]
Description=Peralta Antivirus - Protección con IA
After=network.target

[Service]
Type=simple
WorkingDirectory={install_dir}
ExecStart={sys.executable} {install_dir}/peralta.py --daemon
Restart=always
RestartSec=5
Environment=PERALTA_MODEL={modelo or 'llama3.2'}

[Install]
WantedBy=default.target
"""
        service_dir = Path.home() / ".config" / "systemd" / "user"
        service_dir.mkdir(parents=True, exist_ok=True)
        service_path = service_dir / "peralta.service"
        try:
            service_path.write_text(servicio)
            subprocess.run(["systemctl", "--user", "daemon-reload"], capture_output=True)
            subprocess.run(["systemctl", "--user", "enable", "peralta"], capture_output=True)
            ok("Servicio systemd de usuario creado y habilitado")
            info("Inicia con: systemctl --user start peralta")
        except Exception as e:
            fallo(f"Error creando servicio de usuario: {e}")

            info(f"Inicio manual: python {install_dir}\\peralta.py")

    elif ES_MAC:
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.peralta.antivirus</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{install_dir}/peralta.py</string>
        <string>--daemon</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>{install_dir}</string>
    <key>StandardErrorPath</key>
    <string>{install_dir}/logs/launchd_error.log</string>
</dict>
</plist>
"""
        plist_dir = Path.home() / "Library" / "LaunchAgents"
        plist_dir.mkdir(parents=True, exist_ok=True)
        plist_path = plist_dir / "com.peralta.antivirus.plist"
        try:
            plist_path.write_text(plist_content)
            # Intentar cargar
            subprocess.run(["launchctl", "unload", str(plist_path)], capture_output=True)
            subprocess.run(["launchctl", "load", str(plist_path)], capture_output=True)
            ok("Agent de launchd creado y cargado en macOS")
        except Exception as e:
            fallo(f"Error creando launchd plist: {e}")

# ══════════════════════════════════════════════
# 7. GUARDAR CONFIGURACIÓN
# ══════════════════════════════════════════════
def guardar_config(install_dir: Path, modelo: str):
    paso(7, 7, "Guardando configuración")

    if ES_WINDOWS:
        install_dir_str = str(install_dir)
    else:
        install_dir_str = str(install_dir)

    config = {
        "version": VERSION,
        "sistema": SISTEMA,
        "modelo_ollama": modelo or "llama3",
        "ollama_url": "http://localhost:11434",
        "install_dir": install_dir_str,
        "quarantine_dir": str(install_dir / "quarantine"),
        "log_dir": str(install_dir / "logs"),
        "voz_activada": True,
        "velocidad_voz": 150,
        "idioma_voz": "es",
        "escaneo_web": True,
        "escaneo_apps": True,
        "escaneo_red": True,
        "proteccion_tiempo_real": True,
        "max_file_size_ia": 512000,
        "instalado": True,
        "fecha_instalacion": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    config_path = install_dir / "config" / "peralta.json"
    config_path.write_text(json.dumps(config, indent=2))
    ok(f"Configuración guardada en {config_path}")

    # También guardar en home del usuario
    home_config = Path.home() / ".peralta_config.json"
    home_config.write_text(json.dumps(config, indent=2))
    ok(f"Config de usuario: {home_config}")

    return config

# ══════════════════════════════════════════════
# FLUJO PRINCIPAL
# ══════════════════════════════════════════════
def main():
    titulo()

    if "--yes" not in sys.argv:
        print(f"{Y}Este instalador configurará Peralta Antivirus Neural en tu sistema.{X}")
        print(f"{Y}Se instalará el Motor Neuronal propietario para análisis avanzado.{X}")
        print(f"\n{B}¿Continuar? (s/n):{X} ", end="")

        try:
            respuesta = input().strip().lower()
            if respuesta not in ["s", "si", "sí", "y", "yes", ""]:
                print(f"\n{Y}Instalación cancelada.{X}")
                sys.exit(0)
        except KeyboardInterrupt:
            print(f"\n{Y}Cancelado.{X}")
            sys.exit(0)
    else:
        info("Iniciando instalación automatizada (--yes)")

    print()

    verificar_python()
    instalar_dependencias()
    instalar_ollama()
    modelo = descargar_modelo()
    install_dir = crear_directorio()
    crear_servicio(install_dir, modelo)
    config = guardar_config(install_dir, modelo)

    # Iniciar Peralta inmediatamente para el usuario
    info("Iniciando Peralta Antivirus (Protección Activa)...")
    try:
        if ES_WINDOWS:
            os.startfile(install_dir / "peralta.py")
        else:
            subprocess.Popen([sys.executable, str(install_dir / "peralta.py"), "--daemon"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ok("Protección Neural activa")
        
        # Abrir el Dashboard Táctico automáticamente
        dashboard_url = "http://localhost:5173/chat"
        info(f"Desplegando Interfaz de Control: {dashboard_url}")
        webbrowser.open(dashboard_url)
    except Exception:
        pass

    # ── RESUMEN FINAL ──
    print(f"""
{G}{B}
╔══════════════════════════════════════════════════╗
║   ✅  PERALTA ANTIVIRUS INSTALADO CORRECTAMENTE  ║
╚══════════════════════════════════════════════════╝{X}

{B}Información:{X}
  • Directorio:  {install_dir}
  • Modelo IA:   {modelo or 'llama3 (descargar manualmente)'}
  • Sistema:     {SISTEMA}

{B}Para iniciar Peralta ahora:{X}
""")
    if ES_LINUX or ES_MAC:
        cmd_start = "launchctl load" if ES_MAC else "systemctl --user start peralta"
        print(f"  {C}{cmd_start}{X}      # como servicio")
        print(f"  {C}python3 {install_dir}/peralta.py{X}  # manualmente")
    else:
        print(f"  {C}python \"{install_dir}\\peralta.py\"{X}  # manualmente")
        print(f"  {C}Reinicia Windows para el autoarranque{X}")

    print(f"""
{B}Comandos útiles:{X}
  peralta.py --scan /ruta        Escanear directorio
  peralta.py --status            Ver estado de protección
  peralta.py --orden "analiza"   Dar una orden al sistema
  peralta.py --daemon            Modo protección continua

{Y}⚠  Peralta Neural funciona completamente local — privacidad absoluta.{X}
""")

if __name__ == "__main__":
    main()
