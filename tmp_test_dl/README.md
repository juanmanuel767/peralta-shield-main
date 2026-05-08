# 🛡️ PERALTA ANTIVIRUS NEURAL v1.0
**Por: Juan Manuel Peralta, Ingeniero de Sistemas**

Antivirus de alto rendimiento con **Motor Neuronal Propietario** — privacidad total, análisis local sin internet.

---

## ⚡ Instalación automática

```bash
# Linux (como root/sudo):
sudo python3 instalar_peralta.py

# Windows (como Administrador):
python instalar_peralta.py
```

El instalador hace todo automáticamente:
1. Instala las dependencias especializadas
2. Configura el Motor Neuronal Peralta
3. Descarga el modelo de inteligencia (v3.2 o compatible)
4. Crea el servicio del sistema (autoarranque profesional)
5. Guarda la configuración segura

---

## 🚀 Comandos

```bash
# Protección en tiempo real (modo daemon)
python3 peralta.py --daemon

# Escaneo rápido de un directorio
python3 peralta.py --scan /home/usuario

# Escaneo profundo con análisis de IA
python3 peralta.py --scan /tmp --deep

# Verificar si una URL/sitio web es peligroso
python3 peralta.py --url https://sitio-sospechoso.com

# Ver archivos en cuarentena
python3 peralta.py --quarantine list

# Restaurar archivo de cuarentena
python3 peralta.py --quarantine restore 20240101_120000_archivo.sh

# Actualizar listas de amenazas desde internet
python3 peralta.py --update

# Ver estado del antivirus
python3 peralta.py --status

# Activar / desactivar alertas de voz
python3 peralta.py --voz on
python3 peralta.py --voz off
```

---

## 🔍 ¿Qué detecta Peralta?

### 📦 Monitor de aplicaciones
- Detecta en tiempo real cualquier archivo ejecutable nuevo (`.exe`, `.msi`, `.sh`, `.deb`, `.run`, etc.)
- En Windows también monitorea el registro para detectar apps instaladas
- Analiza automáticamente con IA cada archivo nuevo

### 🌐 Protección web
- Bloquea dominios maliciosos conocidos (botnets, phishing, mineros web)
- Detecta typosquatting (dominios que imitan a bancos, Google, PayPal, etc.)
- Detecta URLs con IP directa (bypass de DNS)
- Se actualiza con feeds de threat intelligence (`--update`)

### 🔒 Detección de intrusos (IDS)
- Monitorea conexiones de red activas
- Detecta conexiones a IPs y puertos de backdoor conocidos
- Detecta escaneos de puertos desde IPs externas
- Detecta procesos maliciosos (xmrig, nmap, mimikatz, netcat reverse shell, etc.)

### 🤖 Análisis Neuronal Propietario
- Analiza el contenido de archivos sospechosos mendiante redes neuronales locales
- Detecta reverse shells, ransomware, miners, webshells
- Clasifica la amenaza con alto porcentaje de precisión
- Todo el análisis ocurre en tu PC — privacidad garantizada

### 🔊 Alertas de voz
- Habla en español cuando detecta amenazas
- Voz urgente para amenazas críticas
- Se puede activar/desactivar con `--voz on/off`

### 🔒 Cuarentena automática
- Los archivos maliciosos se mueven automáticamente a cuarentena
- Se guardan los metadatos (ruta original, hashes, fecha)
- Puedes restaurarlos si fue una falsa alarma

---

## ⚙️ Configuración

El archivo de configuración se guarda en `~/.peralta_config.json`:

```json
{
  "modelo_neuronal": "v3.2",
  "motor_url": "http://localhost:11434",
  "voz_activada": true,
  "velocidad_voz": 145,
  "escaneo_apps": true,
  "escaneo_web": true,
  "escaneo_red": true,
  "proteccion_tiempo_real": true
}
```

### Modelos compatibles
```bash
# Modelos optimizados para el Motor Neuronal Peralta
peralta --model-pull v3.2        # Recomendado (buena velocidad y precisión)
peralta --model-pull mistral     # Muy bueno para análisis de código
peralta --model-pull codellama   # Especializado en código
peralta --model-pull gemma2      # Ligero y eficiente
peralta --model-pull phi3        # Muy ligero para PCs modestos
```

---

## 📁 Estructura de archivos

```
~/.peralta/
├── quarantine/         # Archivos en cuarentena
│   ├── 20240101_*.sh       # Archivo en cuarentena
│   └── 20240101_*.sh.meta  # Metadatos
└── logs/
    └── peralta_20240101.log  # Log diario

~/.peralta_config.json   # Configuración del usuario
```

---

## 🖥️ Como servicio del sistema

**Linux (systemd):**
```bash
sudo systemctl start peralta     # Iniciar
sudo systemctl stop peralta      # Detener
sudo systemctl status peralta    # Ver estado
sudo journalctl -u peralta -f    # Ver logs en tiempo real
```

**Windows:**
Peralta se agrega automáticamente al inicio de Windows. También puedes ejecutarlo manualmente como Administrador.

---

## ⚠️ Notas importantes

- Ejecutar con **sudo/Administrador** para bloquear dominios en `/etc/hosts`
- **Motor Neuronal Peralta funciona completamente local**
