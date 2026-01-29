# 🚀 Quick Start Guide

## 📹 Opción 1: Crear Video Demo para LinkedIn

El método más fácil para generar contenido para redes sociales:

```bash
python create_simple_demo.py
```

**Resultado**: `output/linkedin_demo_simple.avi`

**Layout del video:**
```
┌────────────────────────────────────────┐
│  Face Privacy Protection (YOLOv11)    │
├──────────────────┬─────────────────────┤
│    ORIGINAL      │      PROTECTED      │
└──────────────────┴─────────────────────┘
```

**Duración**: Según el video de entrada (test/video_003.mp4)

---

## 🎥 Opción 2: Tiempo Real con Webcam

Para demostración en vivo desde tu cámara:

### A. Demo Interactivo Simple
```bash
python main.py
# Selecciona opción [2] - Face Pixelation/Blur
```

**Controles:**
- `q` - Salir
- `+` - Más pixelación
- `-` - Menos pixelación
- `b` - Cambiar a modo blur
- `s` - Guardar screenshot

### B. Demo con Efectos Múltiples (6 efectos)
```bash
python face_privacy_demo.py
```

**Efectos disponibles:**
1. Pixelation
2. Blur
3. Black Box
4. Emoji 😊
5. Witness Protection
6. Colorize

**Controles:**
- `1-6` - Cambiar efecto
- `SPACE` - Vista dividida (antes/después)
- `+/-` - Ajustar intensidad
- `h` - Mostrar/ocultar ayuda

---

## 📊 Para LinkedIn - Workflow Recomendado

### Paso 1: Generar Video
```bash
python create_simple_demo.py
```

### Paso 2: Revisar Video
```
output/linkedin_demo_simple.avi
```

### Paso 3: Subir a LinkedIn
- Abre LinkedIn
- Crear publicación
- Adjunta el video
- Usa un post template de `LINKEDIN_POST.md`

### Paso 4: (Opcional) Demo en Vivo
Graba tu pantalla mientras ejecutas:
```bash
python face_privacy_demo.py
```

---

## 🎯 Comparación Rápida

| Característica | Video Demo | Tiempo Real |
|----------------|------------|-------------|
| Para LinkedIn | ✅ Perfecto | ⚠️ Requiere grabación |
| Calidad | Alta | Media |
| Facilidad | Muy fácil | Requiere webcam |
| Editable | No | Sí (en vivo) |
| Tiempo | ~1-2 min | Inmediato |

---

## 💡 Tips

### Para mejor calidad de video:
- Usa videos con buena iluminación
- Rostros frontales funcionan mejor
- Resolución 720p o superior

### Para demostración en vivo:
- Asegúrate de tener buena iluminación
- Posiciónate de frente a la cámara
- Prueba antes de grabar

---

## 🔧 Troubleshooting

**Video no se reproduce:**
- El formato AVI funciona en Windows Media Player
- Para otros reproductores, convierte a MP4 con VLC

**Detección no funciona:**
- Verifica que `models/yolov11s-face.pt` exista
- Baja el threshold de confianza en el código

**Cámara no abre:**
- Cierra otras apps que usen la cámara
- Verifica permisos de cámara en Windows

---

## 📝 Archivos Principales

```
create_simple_demo.py       → Genera video para LinkedIn
face_privacy_demo.py        → Demo interactivo con 6 efectos
main.py                     → Menú con todas las opciones
LINKEDIN_POST.md            → Templates de posts
```

---

## ⚡ Comando Todo-en-Uno

Para ejecutar todo el workflow:

```bash
# 1. Instalar dependencias (primera vez)
pip install -r requirements.txt

# 2. Generar video demo
python create_simple_demo.py

# 3. Abrir carpeta de output
start output
```

¡Listo para LinkedIn! 🚀
