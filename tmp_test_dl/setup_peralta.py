#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import time
import json
from pathlib import Path

# Configuración
INSTALL_DIR = Path.home() / ".local" / "share" / "peralta"
CONFIG_DIR = INSTALL_DIR / "config"
LOG_DIR = INSTALL_DIR / "logs"
QUARANTINE_DIR = INSTALL_DIR / "quarantine"
SERVICE_NAME = "peralta"

# Estética Rich opcional (se instalará en el proceso)
def print_status(msg, ok=True):
    icon = "✓" if ok else "!"
    print(f"[{icon}] {msg}")

def run_cmd(cmd, msg=None):
    if msg: print_status(msg)
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def main():
    print("\n" + "="*50)
    print("   PERALTA ANTIVIRUS - INSTALADOR PROFESIONAL")
    print("="*50 + "\n")

    # 1. Dependencias Críticas
    print_status("Instalando dependencias de sistema...")
    deps = ["rich", "requests", "flask", "flask-cors", "psutil", "watchdog", "pystray", "Pillow"]
    run_cmd(f"{sys.executable} -m pip install {' '.join(deps)} --quiet --break-system-packages")

    # 2. Crear Directorios
    print_status("Creando estructura de archivos...")
    for d in [INSTALL_DIR, CONFIG_DIR, LOG_DIR, QUARANTINE_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    # 3. Copiar Archivos (Buscando en el directorio actual)
    files_to_copy = ["peralta.py", "tray_icon.png", "setup_peralta.py"]
    src_dir = Path(__file__).parent
    for f in files_to_copy:
        src = src_dir / f
        if src.exists():
            shutil.copy2(src, INSTALL_DIR / f)
            print_status(f"Copiado: {f}")
        else:
            print_status(f"Error: No se encontró {f}", ok=False)

    # Copiar gui_build
    gui_src = src_dir / "gui_build"
    if gui_src.exists():
        if (INSTALL_DIR / "gui_build").exists():
            shutil.rmtree(INSTALL_DIR / "gui_build")
        shutil.copytree(gui_src, INSTALL_DIR / "gui_build")
        print_status("Copiado: gui_build")

    # 4. Configuración Systemd (Modo Usuario)
    print_status("Configurando servicio de protección en segundo plano...")
    service_content = f"""[Unit]
Description=Peralta Antivirus - Neural Core
After=network.target

[Service]
Type=simple
WorkingDirectory={INSTALL_DIR}
ExecStart={sys.executable} {INSTALL_DIR}/peralta.py --daemon
Restart=always
RestartSec=5
Environment=PYTHONPATH={INSTALL_DIR}

[Install]
WantedBy=default.target
"""
    user_systemd = Path.home() / ".config" / "systemd" / "user"
    user_systemd.mkdir(parents=True, exist_ok=True)
    (user_systemd / f"{SERVICE_NAME}.service").write_text(service_content)
    
    run_cmd("systemctl --user daemon-reload")
    run_cmd(f"systemctl --user enable {SERVICE_NAME}")
    run_cmd(f"systemctl --user restart {SERVICE_NAME}")

    # 5. Configuración Inicial
    config = {
        "version": "1.1.0",
        "install_dir": str(INSTALL_DIR),
        "voz_activada": True,
        "escaneo_web": True,
        "proteccion_tiempo_real": True,
        "instalado": True,
        "fecha": time.ctime()
    }
    (CONFIG_DIR / "peralta.json").write_text(json.dumps(config, indent=2))
    (Path.home() / ".peralta_config.json").write_text(json.dumps(config, indent=2))

    print("\n" + "="*50)
    print("   ¡PERALTA ANTIVIRUS INSTALADO CON ÉXITO!")
    print("   La protección neural ya está activa.")
    print("="*50 + "\n")
    
    # Abrir Dashboard (Opcional)
    print_status("Abriendo Neural Interface...")
    try:
        # Intentar detectar el puerto del servidor de desarrollo o la landing
        run_cmd("xdg-open http://localhost:5173/landing.html") 
    except:
        pass

if __name__ == "__main__":
    main()
