#!/bin/bash

# Script para empaquetar el antivirus Peralta para distribución
# Este script crea archivos ZIP para Linux, Windows y macOS

SOURCE_DIR="/home/user/juego unity/antivirus peralta/files"
PROJECT_DIR="/home/user/Descargas/paguina web para antivirus/peralta-shield-main"
OUTPUT_DIR="$PROJECT_DIR/public/installers"

echo "📦 Empezando empaquetado del Antivirus Peralta..."

# Asegurar que el directorio de salida existe
mkdir -p "$OUTPUT_DIR"

# Definir los archivos básicos a incluir
FILES_TO_INCLUDE=(
    "peralta.py"
    "instalar_peralta.py"
    "setup_peralta.py"
    "requirements.txt"
    "tray_icon.png"
    "README.md"
    "gui_build"
)

# Cambiar al directorio fuente temporalmente
cd "$SOURCE_DIR" || exit

# Crear los ZIPs multiplataforma
echo "--- Creando instaladores en $OUTPUT_DIR ---"

# Linux
zip -r "$OUTPUT_DIR/peralta-antivirus-linux.zip" "${FILES_TO_INCLUDE[@]}"
echo "✅ peralta-antivirus-linux.zip creado."

# Windows
zip -r "$OUTPUT_DIR/peralta-antivirus-windows.zip" "${FILES_TO_INCLUDE[@]}"
echo "✅ peralta-antivirus-windows.zip creado."

# macOS
zip -r "$OUTPUT_DIR/peralta-antivirus-macos.zip" "${FILES_TO_INCLUDE[@]}"
echo "✅ peralta-antivirus-macos.zip creado."

echo "🚀 ¡Empaquetado completado en $OUTPUT_DIR!"
