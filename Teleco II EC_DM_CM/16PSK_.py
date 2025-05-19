import numpy as np
import matplotlib.pyplot as plt

# Número de símbolos 16-PSK (4 bits)
M = 16
bits_list = [format(i, '04b') for i in range(M)]

# Amplitud constante para PSK
amplitude = 1

# Fases igualmente espaciadas entre 0 y 2pi
phases_rad = np.linspace(0, 2 * np.pi, M, endpoint=False)

# Calcular coordenadas I, Q
constellation_points = amplitude * np.column_stack((np.cos(phases_rad), np.sin(phases_rad)))

print(f"{'Bits':>6} | {'I':>6} {'Q':>6} | {'Amplitud':>8} | {'Fase (rad)':>10} | {'Fase (°)':>9} | {'Rectangular (I+jQ)':>22}")
print("-" * 85)

for bits, (I, Q), phase_rad in zip(bits_list, constellation_points, phases_rad):
    phase_deg = np.degrees(phase_rad)
    rect = complex(I, Q)
    print(f"{bits:>6} | {I:6.3f} {Q:6.3f} | {amplitude:8.3f} | {phase_rad:10.3f} | {phase_deg:9.1f} | {rect.real:+6.3f}{rect.imag:+6.3f}j")

# Graficar constelación
plt.figure(figsize=(7, 7))
plt.scatter(constellation_points[:, 0], constellation_points[:, 1], color='red', s=150)

for i, (I, Q, bits) in enumerate(zip(constellation_points[:, 0], constellation_points[:, 1], bits_list)):
    label = f"{bits}\nΦ={np.degrees(phases_rad[i]):.1f}°"
    plt.text(I + 0.05, Q + 0.05, label, fontsize=10)

plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.title("Diagrama de Constelación 16-PSK")
plt.xlabel("Componente In-phase (I)")
plt.ylabel("Componente Quadrature (Q)")
plt.grid(True)
plt.axis('equal')
plt.show()

# Parámetros
fs = 500  # Frecuencia de muestreo (Hz)
fc = 10   # Frecuencia portadora (Hz)
Tb = 0.1  # Duración de cada símbolo (s)
M = 16    # Número de símbolos PSK (16PSK)
num_symbols = 16

# Definir las fases para 16PSK (espaciadas cada 22.5° o π/8 radianes)
phases = np.linspace(0, 2 * np.pi, M, endpoint=False)

# Colores para cada símbolo (16 colores distintos, se repiten si hay más símbolos)
colors = [
    'blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'cyan',
    'magenta', 'lime', 'yellow', 'navy', 'grey', 'maroon', 'teal', 'black'
]

# Generar símbolos aleatorios (valores entre 0 y 15)
symbols = np.random.randint(0, M, num_symbols)

# Mapear símbolos a fases
phase_symbols = phases[symbols]

# Crear la señal baseband (solo para mostrar la fase)
t = np.arange(0, num_symbols * Tb, 1 / fs)
baseband_phase = np.zeros_like(t)

for i in range(num_symbols):
    start_idx = int(i * Tb * fs)
    end_idx = int((i + 1) * Tb * fs)
    baseband_phase[start_idx:end_idx] = phase_symbols[i]

# Señal 16PSK modulada con colores por símbolo
psk_signal = np.zeros_like(t)

# Graficar señal con colores por símbolo
fig, axs = plt.subplots(3, 1, figsize=(12, 12))

for i in range(num_symbols):
    start_idx = int(i * Tb * fs)
    end_idx = int((i + 1) * Tb * fs)
    time_slice = t[start_idx:end_idx]
    segment = np.cos(2 * np.pi * fc * time_slice + phase_symbols[i])
    psk_signal[start_idx:end_idx] = segment
    axs[1].plot(time_slice, segment, color=colors[symbols[i] % len(colors)])

# Espectro de frecuencia
fft_signal = np.fft.fft(psk_signal)
frequencies = np.fft.fftfreq(len(fft_signal), 1 / fs)
fft_magnitude = np.abs(fft_signal)

# Graficar componentes
# Fase baseband
axs[0].plot(t, baseband_phase, color='orange')
axs[0].set_title("Baseband Phase Component (16PSK)")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Phase (radians)")
axs[0].grid()

# Señal 16PSK (ya graficada por símbolos con colores)
axs[1].set_title("16PSK Signal with Colors per Symbol")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Amplitude")
axs[1].grid()

# Espectro de frecuencia
axs[2].plot(frequencies[:len(frequencies)//2], fft_magnitude[:len(frequencies)//2], color='blue')
axs[2].set_title("16PSK Frequency Spectrum")
axs[2].set_xlabel("Frequency (Hz)")
axs[2].set_ylabel("Magnitude")
axs[2].grid()

plt.tight_layout()
plt.show()

# Número de símbolos para 16PSK
N = 16

# Ángulos en radianes (espaciados uniformemente en un círculo)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

# Magnitud constante (puede ajustarse, por defecto 3 para mantener similar al rango del 16QAM)
magnitude = 3

# Coordenadas (I, Q) basadas en los ángulos y magnitud
A_k = magnitude * np.cos(angles)
B_k = magnitude * np.sin(angles)

# Configurar la figura
plt.figure(figsize=(8, 8))
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.grid(alpha=0.5, linestyle='--')
plt.title('Diagrama Fasorial 16PSK')
plt.xlabel('Componente In-phase (I)')
plt.ylabel('Componente Quadrature (Q)')
plt.axis('equal')
plt.xlim(-4, 4)
plt.ylim(-4, 4)

# Dibujar los fasores
for x, y in zip(A_k, B_k):
    # Dibujar el fasor desde el origen al punto (x, y)
    plt.arrow(0, 0, x, y, head_width=0.1, head_length=0.15, fc='blue', ec='blue', alpha=0.7)

# Etiquetas binarias para 16PSK (4 bits por símbolo)
labels = [f"{i:04b}" for i in range(N)]

# Añadir etiquetas binarias
for i, (x, y) in enumerate(zip(A_k, B_k)):
    plt.text(x * 1.1, y * 1.1, labels[i], fontsize=10, ha='center', va='center')

plt.show()


