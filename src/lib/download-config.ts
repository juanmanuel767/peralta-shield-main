export const DOWNLOAD_CONFIG = {
  version: "3.2.0",
  lastUpdated: "2026-05-08",
  platforms: {
    windows: {
      name: "Windows",
      icon: "Monitor",
      version: "Windows 10, 11 (64-bit)",
      size: "45 MB",
      url: "https://github.com/manuel-peralta/peralta-shield/releases/download/v3.2.0/PeraltaShield_Setup.exe",
      terminalCommand: "Invoke-WebRequest -Uri https://peralta-shield.com/installers/PeraltaShield_Setup.exe -OutFile PeraltaShield_Setup.exe; .\\PeraltaShield_Setup.exe",
      checksum: "sha256-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
      steps: [
        "Descarga y descomprime el archivo ZIP",
        "Haz clic derecho en 'instalar_peralta.py' → Ejecutar como administrador",
        "El motor neuronal se instalará y configurará automáticamente",
        "Peralta se iniciará y protegerá tu sistema en tiempo real"
      ]
    },
    macos: {
      name: "macOS",
      icon: "Apple",
      version: "macOS 12.0 (Monterey) o superior",
      size: "38 MB",
      url: "/installers/peralta-antivirus-macos.zip",
      terminalCommand: "curl -L -O https://peralta-shield.com/installers/peralta-antivirus-macos.zip && unzip peralta-antivirus-macos.zip && sudo python3 instalar_peralta.py",
      checksum: "sha256-b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2a1",
      steps: [
        "Descarga y descomprime el archivo ZIP",
        "Abre una Terminal en la carpeta extraída",
        "Ejecuta: sudo python3 instalar_peralta.py",
        "Otorga permisos de accesibilidad cuando Peralta lo solicite",
        "Tu Mac ahora está bajo protección de IA neuronal"
      ]
    },
    linux: {
      name: "Linux",
      icon: "Tux",
      version: "Ubuntu 22.04+, Fedora 38+, Debian 12+",
      size: "52 MB",
      url: "/installers/peralta-antivirus-linux.zip",
      terminalCommand: "curl -L -O http://localhost:5173/installers/peralta-antivirus-linux.zip && unzip -o peralta-antivirus-linux.zip && python3 instalar_peralta.py --yes",
      checksum: "sha256-c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2a1b2",
      steps: [
        "Descarga y descomprime el archivo ZIP",
        "Abre una terminal en la carpeta extraída",
        "Ejecuta: sudo python3 instalar_peralta.py",
        "El instalador configurará el servicio systemd automáticamente",
        "Verifica el estado con: peralta --status"
      ]
    }
  }
};
