# 🗼 Torre de Hanoi

Un juego interactivo y dinámico de la Torre de Hanoi, hecho en Python con `tkinter`.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)

## 📋 Requisitos

- **Python 3.7 o superior**
- **tkinter** (incluido por defecto en la mayoría de instalaciones de Python)

No necesitas instalar ninguna librería extra (`pip`) — el juego solo usa la librería estándar de Python.

### Verificar que tienes tkinter

En algunas distribuciones de Linux, `tkinter` no viene preinstalado. Verifica con:

```bash
python3 -m tkinter
```

Si se abre una ventanita de prueba, ya lo tienes. Si da error, instálalo según tu sistema:

| Sistema | Comando |
|---|---|
| **Windows** | Ya viene incluido con el instalador oficial de Python (python.org) |
| **macOS** | Ya viene incluido con Python de python.org (no siempre con el de Homebrew) |
| **Ubuntu / Debian** | `sudo apt install python3-tk` |
| **Fedora** | `sudo dnf install python3-tkinter` |
| **Arch Linux** | `sudo pacman -S tk` |

## 📥 Instalación

1. Descarga el archivo `torre_hanoi.py`.
2. Colócalo en cualquier carpeta de tu computadora.
3. ¡Listo! No hace falta compilar ni instalar nada más.

## ▶️ Cómo ejecutar el juego

Abre una terminal (o símbolo del sistema) en la carpeta donde guardaste el archivo y ejecuta:

```bash
python3 torre_hanoi.py
```

> En Windows, si `python3` no funciona, prueba con `python torre_hanoi.py`.

## 🎮 Cómo jugar

1. Haz clic en una torre para **seleccionar** el disco de arriba (se resalta en amarillo).
2. Haz clic en otra torre para **moverlo** ahí.
3. **Objetivo:** mover toda la pila de discos desde la Torre A hasta la Torre C, usando la Torre B como apoyo — sin poner nunca un disco más grande sobre uno más chico.

### Controles disponibles

| Botón | Función |
|---|---|
| 🔄 **Reiniciar** | Vuelve a empezar la partida actual |
| 🔢 **Cambiar # discos** | Elige entre 3 y 8 discos con un control deslizante |
| 🤖 **Resolver automáticamente** | La computadora resuelve el juego paso a paso (modo demostración) |
| ↩️ **Deshacer** | Revierte el último movimiento realizado |

El juego lleva la cuenta de tus **movimientos** y el **tiempo transcurrido**, y te muestra cuál es el mínimo de movimientos posible (2ⁿ − 1). ¡Si lo logras en el mínimo, obtienes puntuación perfecta! 🏆

## 🛠️ Solución de problemas

- **"No module named tkinter"** → instala tkinter según la tabla de arriba y vuelve a intentar.
- **La ventana no se ve bien / muy pequeña o grande** → depende de la resolución de tu pantalla; el tamaño de la ventana es fijo por diseño.
- **No pasa nada al hacer clic** → asegúrate de hacer clic dentro del área de las torres (el lienzo oscuro), no en los botones.

## 📄 Licencia

Libre de usar, modificar y compartir.
