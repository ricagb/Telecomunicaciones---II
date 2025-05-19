import numpy as np
import matplotlib.pyplot as plt

# Definición de símbolos 16QAM (4 bits) con sus coordenadas (I, Q)
# Niveles típicos para 16QAM: [-3, -1, 1, 3]
levels = [-3, -1, 1, 3]

bits_list = []
constellation_points = []

# Generar tabla de verdad y puntos para 16QAM (orden Gray o natural)
# Usamos el orden natural aquí: bits [b3 b2 b1 b0], b3 b2 para I, b1 b0 para Q
for i in range(16):
    bits = format(i, '04b')
    bits_list.append(bits)
    # Mapear bits: b3b2 -> I, b1b0 -> Q
    I_bits = int(bits[:2], 2)  # Primeros 2 bits
    Q_bits = int(bits[2:], 2)  # Últimos 2 bits
    I = levels[I_bits]
    Q = levels[Q_bits]
    constellation_points.append([I, Q])

constellation_points = np.array(constellation_points)

print(f"{'Bits':>5} | {'I':>3} {'Q':>3} | {'Amplitud':>8} | {'Fase (rad)':>10} | {'Fase (°)':>9} | {'Rectangular (I+jQ)':>22}")
print("-"*80)

for bits, (I, Q) in zip(bits_list, constellation_points):
    amplitude = np.sqrt(I**2 + Q**2)
    phase_rad = np.arctan2(Q, I)
    phase_deg = np.degrees(phase_rad)
    rect = complex(I, Q)
    print(f"{bits:>5} | {I:3d} {Q:3d} | {amplitude:8.3f} | {phase_rad:10.3f} | {phase_deg:9.1f} | {rect.real:+6.1f}{rect.imag:+6.1f}j")

# Graficar constelación con etiquetas
plt.figure(figsize=(8,8))
plt.scatter(constellation_points[:, 0], constellation_points[:, 1], color='red', s=100)

for i, (I, Q) in enumerate(constellation_points):
    label = f"{bits_list[i]}\nA={np.sqrt(I**2+Q**2):.2f}\nΦ={np.degrees(np.arctan2(Q, I)):.1f}°"
    plt.text(I + 0.15, Q + 0.15, label, fontsize=9)

plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.title("Diagrama de Constelación 16QAM con Amplitud y Fase")
plt.xlabel("Componente In-phase (I)")
plt.ylabel("Componente Quadrature (Q)")
plt.grid(True)
plt.axis('equal')
plt.xlim(-4, 4)
plt.ylim(-4, 4)
plt.show()

# Parámetros
fs = 500  # Frecuencia de muestreo (Hz)
fc = 10   # Frecuencia portadora (Hz)
Tb = 0.1   # Duración de cada símbolo (s)
M = 16     # Número de símbolos QAM (16QAM)
num_symbols = 16

# Niveles para I y Q en 16QAM (4 niveles cada uno)
levels_I = np.array([-3, -1, 1, 3])
levels_Q = np.array([-3, -1, 1, 3])

# Generar símbolos aleatorios (valores entre 0 y 15)
symbols = np.random.randint(0, M, num_symbols)

# Mapear símbolos a I y Q
# Usamos 2 bits para I (bits altos), 2 bits para Q (bits bajos)
I_symbols = levels_I[(symbols // 4) % 4]
Q_symbols = levels_Q[symbols % 4]

# Crear la señal baseband
t = np.arange(0, num_symbols * Tb, 1 / fs)
baseband_I = np.zeros_like(t)
baseband_Q = np.zeros_like(t)

# Colores para 16 símbolos (puedes definir más colores si quieres)
colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'cyan',
          'magenta', 'lime', 'yellow', 'gray', 'navy', 'olive', 'teal', 'coral']

for i in range(num_symbols):
    start_idx = int(i * Tb * fs)
    end_idx = int((i + 1) * Tb * fs)
    baseband_I[start_idx:end_idx] = I_symbols[i]
    baseband_Q[start_idx:end_idx] = Q_symbols[i]

# Señal 16QAM modulada
qam_signal = np.zeros_like(t)
for i in range(num_symbols):
    start_idx = int(i * Tb * fs)
    end_idx = int((i + 1) * Tb * fs)
    time_slice = t[start_idx:end_idx]
    carrier_I = np.cos(2 * np.pi * fc * time_slice)
    carrier_Q = np.sin(2 * np.pi * fc * time_slice)
    segment = I_symbols[i] * carrier_I - Q_symbols[i] * carrier_Q
    qam_signal[start_idx:end_idx] = segment

# Espectro de frecuencia
fft_signal = np.fft.fft(qam_signal)
frequencies = np.fft.fftfreq(len(fft_signal), 1 / fs)
fft_magnitude = np.abs(fft_signal)

# Graficar
fig, axs = plt.subplots(4, 1, figsize=(12, 16))

# Baseband I
axs[0].plot(t, baseband_I, color='orange')
axs[0].set_title("Baseband I Component (16-QAM)")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Amplitude")
axs[0].grid()

# Baseband Q
axs[1].plot(t, baseband_Q, color='green')
axs[1].set_title("Baseband Q Component (16-QAM)")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Amplitude")
axs[1].grid()

# Señal 16QAM con colores por símbolo
for i in range(num_symbols):
    start_idx = int(i * Tb * fs)
    end_idx = int((i + 1) * Tb * fs)
    axs[2].plot(t[start_idx:end_idx], qam_signal[start_idx:end_idx], color=colors[symbols[i] % len(colors)])

axs[2].set_title("16-QAM Signal with Colors")
axs[2].set_xlabel("Time (s)")
axs[2].set_ylabel("Amplitude")
axs[2].grid()

# Espectro de frecuencia
axs[3].plot(frequencies[:len(frequencies)//2], fft_magnitude[:len(frequencies)//2], color='blue')
axs[3].set_title("16-QAM Frequency Spectrum")
axs[3].set_xlabel("Frequency (Hz)")
axs[3].set_ylabel("Magnitude")
axs[3].grid()

plt.tight_layout()
plt.show()

# 4 niveles por eje para 16QAM
levels = np.array([-3, -1, 1, 3])

# Generar la cuadrícula de puntos 16QAM
A_k, B_k = np.meshgrid(levels, levels)
A_k = A_k.flatten()
B_k = B_k.flatten()

# Configurar la figura
plt.figure(figsize=(8, 8))
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.grid(alpha=0.5, linestyle='--')
plt.title('Diagrama Fasorial 16QAM')
plt.xlabel('Componente In-phase (I)')
plt.ylabel('Componente Quadrature (Q)')
plt.axis('equal')
plt.xlim(-4, 4)
plt.ylim(-4, 4)

# Dibujar los fasores
for x, y in zip(A_k, B_k):
    # Dibujar el fasor desde el origen al punto (x, y)
    plt.arrow(0, 0, x, y, head_width=0.1, head_length=0.15, fc='blue', ec='blue', alpha=0.7)

plt.show()
