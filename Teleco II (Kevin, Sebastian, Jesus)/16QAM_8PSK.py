import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython
from IPython.display import display
from itertools import product


# 1. Entrada del usuario
V1 = float(input("Ingrese el voltaje para el C = 1: "))  # Ej: 1.309
V0 = float(input("Ingrese el voltaje para el C = 0: "))  # Ej: 0.541

fs = 1000               # Frecuencia de muestreo
f_c = 1000              # Frecuencia de la portadora
t_symbol = 1 / f_c      # Un ciclo por símbolo

# Tabla de verdad – 8QAM
mapa_8qam = {
    '000': ( V0,  V1),
    '001': ( V1,  V0),
    '010': ( V0, -V1),
    '011': (-V1,  V0),
    '100': ( V1,  V1),
    '101': (-V1, -V1),
    '110': ( V1, -V1),
    '111': (-V1,  V1)
}

# Tabla de verdad – 8PSK
mapa_8psk = {
    '000': 22.5,
    '001': 67.5,
    '010': 157.5,
    '011': 112.5,
    '100': -112.5,
    '101': -157.5,
    '110': -67.5,
    '111': -22.5
}

# Tabla de verdad – 16QAM
niveles = {
    '00': -V1,
    '01': -V0,
    '11':  V0,
    '10':  V1
}

mapa_16qam = {}
bits_16qam = []
for b in product('01', repeat=4):
    bits = ''.join(b)
    I = niveles[bits[0:2]]
    Q = niveles[bits[2:4]]
    mapa_16qam[bits] = (I, Q)
    bits_16qam.append(bits)

bits_list = list(mapa_8qam.keys())
colores = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'teal', 'magenta']
t = np.linspace(0, t_symbol, fs)

# --- Fase de salida – 8QAM ---
plt.figure(figsize=(12, 4))
for i, bits in enumerate(bits_list):
    I, Q = mapa_8qam[bits]
    señal = I * np.cos(2*np.pi*f_c*t) + Q * np.sin(2*np.pi*f_c*t)
    plt.plot(t + i*t_symbol, señal, color=colores[i])
    fase = np.angle(complex(I, Q), deg=True)
    plt.text(i*t_symbol + 0.0001, 1.6, bits, color=colores[i])
    plt.text(i*t_symbol + 0.0001, -1.8, f"{fase:.1f}°", color=colores[i])
plt.title("Fase de salida – 8QAM (1 ciclo por símbolo)")
plt.grid(True)
plt.ylim(-2, 2)
plt.tight_layout()
plt.show()

# --- Fase de salida – 8PSK ---
plt.figure(figsize=(12, 4))
for i, bits in enumerate(bits_list):
    fase_rad = np.deg2rad(mapa_8psk[bits])
    señal = np.sin(2*np.pi*f_c*t + fase_rad)
    plt.plot(t + i*t_symbol, señal, color=colores[i])
    plt.text(i*t_symbol + 0.0001, 1.6, bits, color=colores[i])
    plt.text(i*t_symbol + 0.0001, -1.8, f"{mapa_8psk[bits]}°", color=colores[i])
plt.title("Fase de salida – 8PSK (1 ciclo por símbolo)")
plt.grid(True)
plt.ylim(-2, 2)
plt.tight_layout()
plt.show()

# --- Fase de salida – 16QAM ---
plt.figure(figsize=(16, 4))
for i, bits in enumerate(bits_16qam):
    I, Q = mapa_16qam[bits]
    señal = I * np.cos(2*np.pi*f_c*t) + Q * np.sin(2*np.pi*f_c*t)
    plt.plot(t + i*t_symbol, señal, color=colores[i % len(colores)])
    fase = np.angle(complex(I, Q), deg=True)
    plt.text(i*t_symbol + 0.0001, 1.6, bits, color=colores[i % len(colores)])
    plt.text(i*t_symbol + 0.0001, -1.8, f"{fase:.1f}°", color=colores[i % len(colores)])
plt.title("Fase de salida – 16QAM (1 ciclo por símbolo)")
plt.grid(True)
plt.ylim(-2*V1, 2*V1)
plt.tight_layout()
plt.show()

# --- Constelación – 8QAM ---
plt.figure(figsize=(6, 6))
for bits, (I, Q) in mapa_8qam.items():
    plt.plot(I, Q, 'o', color='black')
    plt.text(I + 0.05, Q + 0.05, bits, fontsize=10)
plt.title("Constelación – 8QAM")
plt.axhline(0, color='gray')
plt.axvline(0, color='gray')
plt.grid(True)
plt.xlim(-1.6, 1.6)
plt.ylim(-1.6, 1.6)
plt.gca().set_aspect('equal')
plt.show()

# --- Constelación – 8PSK ---
plt.figure(figsize=(6, 6))
for bits, fase in mapa_8psk.items():
    rad = np.deg2rad(fase)
    I = np.cos(rad)
    Q = np.sin(rad)
    plt.plot(I, Q, 'o', color='black')
    plt.text(I + 0.05, Q + 0.05, bits, fontsize=10)
circle = plt.Circle((0, 0), radius=1, fill=False, linestyle='--', color='blue')
plt.gca().add_patch(circle)
plt.title("Constelación – 8PSK")
plt.axhline(0, color='gray')
plt.axvline(0, color='gray')
plt.grid(True)
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
plt.gca().set_aspect('equal')
plt.show()

# --- Constelación – 16QAM ---
plt.figure(figsize=(6, 6))
for bits, (I, Q) in mapa_16qam.items():
    plt.plot(I, Q, 'o', color='black')
    plt.text(I + 0.05, Q + 0.05, bits, fontsize=9)
plt.title("Constelación – 16QAM")
plt.axhline(0, color='gray')
plt.axvline(0, color='gray')
plt.grid(True)
plt.xlim(-1.5*V1, 1.5*V1)
plt.ylim(-1.5*V1, 1.5*V1)
plt.gca().set_aspect('equal')
plt.show()

# --- Diagrama vectorial – 8QAM ---
plt.figure(figsize=(6, 6))
for i, bits in enumerate(bits_list):
    I, Q = mapa_8qam[bits]
    color = colores[i]
    plt.arrow(0, 0, I, Q, head_width=0.1, color=color, length_includes_head=True)
    plt.text(1.1*I, 1.1*Q, bits, fontsize=10, color=color)
plt.title("Vectorial – 8QAM")
plt.axhline(0, color='gray')
plt.axvline(0, color='gray')
plt.grid(True)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.gca().set_aspect('equal')
plt.show()

# --- Diagrama vectorial – 8PSK ---
plt.figure(figsize=(6, 6))
for i, bits in enumerate(bits_list):
    fase = np.deg2rad(mapa_8psk[bits])
    I = np.cos(fase)
    Q = np.sin(fase)
    color = colores[i]
    plt.arrow(0, 0, I, Q, head_width=0.1, color=color, length_includes_head=True)
    plt.text(1.1*I, 1.1*Q, bits, fontsize=10, color=color)
plt.title("Vectorial – 8PSK")
plt.axhline(0, color='gray')
plt.axvline(0, color='gray')
plt.grid(True)
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
plt.gca().set_aspect('equal')
plt.show()

# --- Diagrama vectorial – 16QAM ---
plt.figure(figsize=(6, 6))
for i, bits in enumerate(bits_16qam):
    I, Q = mapa_16qam[bits]
    color = colores[i % len(colores)]
    plt.arrow(0, 0, I, Q, head_width=0.1, color=color, length_includes_head=True)
    plt.text(1.05*I, 1.05*Q, bits, fontsize=9, color=color)
plt.title("Vectorial – 16QAM")
plt.axhline(0, color='gray')
plt.axvline(0, color='gray')
plt.grid(True)
plt.xlim(-1.5*V1, 1.5*V1)
plt.ylim(-1.5*V1, 1.5*V1)
plt.gca().set_aspect('equal')
plt.show()
