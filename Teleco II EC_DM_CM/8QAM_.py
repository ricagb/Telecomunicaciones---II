import numpy as np
import matplotlib.pyplot as plt

# Definición de símbolos 8QAM (3 bits) con sus coordenadas (I, Q)
bits_list = ['000', '001', '010', '011', '100', '101', '110', '111']
constellation_points = np.array([
    [1, 1],    # 000
    [2, 2],    # 001
    [-1, 1],   # 010
    [-2, 2],   # 011
    [-1, -1],  # 100
    [-2, -2],  # 101
    [1, -1],   # 110
    [2, -2]    # 111
])

print(f"{'Bits':>5} | {'I':>3} {'Q':>3} | {'Amplitud':>8} | {'Fase (rad)':>10} | {'Fase (°)':>9} | {'Rectangular (I+jQ)':>22}")
print("-"*70)

for bits, (I, Q) in zip(bits_list, constellation_points):
    amplitude = np.sqrt(I**2 + Q**2)
    phase_rad = np.arctan2(Q, I)
    phase_deg = np.degrees(phase_rad)
    rect = complex(I, Q)
    print(f"{bits:>5} | {I:3d} {Q:3d} | {amplitude:8.3f} | {phase_rad:10.3f} | {phase_deg:9.1f} | {rect.real:+6.1f}{rect.imag:+6.1f}j")

# Graficar constelación con etiquetas
plt.figure(figsize=(7,7))
plt.scatter(constellation_points[:, 0], constellation_points[:, 1], color='red', s=100)

for i, (I, Q) in enumerate(constellation_points):
    label = f"{bits_list[i]}\nA={np.sqrt(I**2+Q**2):.2f}\nΦ={np.degrees(np.arctan2(Q, I)):.1f}°"
    plt.text(I + 0.1, Q + 0.1, label, fontsize=10)

plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.title("Diagrama de Constelación 8QAM con Amplitud y Fase")
plt.xlabel("Componente In-phase (I)")
plt.ylabel("Componente Quadrature (Q)")
plt.grid(True)
plt.axis('equal')
plt.show()


# Parámetros
fs = 500  # Frecuencia de muestreo (Hz)
fc = 10   # Frecuencia portadora (Hz)
Tb = 0.1   # Duración de cada símbolo (s)
M = 8      # Número de símbolos QAM (8QAM)
num_symbols = 16

# Definir niveles para I y Q
# Usamos 4 niveles en I y 2 niveles en Q (4*2=8 símbolos)
levels_I = np.array([-3, -1, 1, 3])
levels_Q = np.array([-1, 1])

# Generar símbolos aleatorios (valores entre 0 y 7)
symbols = np.random.randint(0, M, num_symbols)

# Mapear símbolos a I y Q
# bits altos (2 bits) para I, bit bajo (1 bit) para Q
I_symbols = levels_I[(symbols // 2) % 4]
Q_symbols = levels_Q[symbols % 2]

# Crear la señal baseband
t = np.arange(0, num_symbols * Tb, 1 / fs)
baseband_I = np.zeros_like(t)
baseband_Q = np.zeros_like(t)

# Colores para cada símbolo
colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'cyan']

for i in range(num_symbols):
    start_idx = int(i * Tb * fs)
    end_idx = int((i + 1) * Tb * fs)
    baseband_I[start_idx:end_idx] = I_symbols[i]
    baseband_Q[start_idx:end_idx] = Q_symbols[i]

# Señal 8QAM modulada
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
axs[0].set_title("Baseband I Component (8-QAM)")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Amplitude")
axs[0].grid()

# Baseband Q
axs[1].plot(t, baseband_Q, color='green')
axs[1].set_title("Baseband Q Component (8-QAM)")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Amplitude")
axs[1].grid()

# Señal 8QAM con colores
for i in range(num_symbols):
    start_idx = int(i * Tb * fs)
    end_idx = int((i + 1) * Tb * fs)
    axs[2].plot(t[start_idx:end_idx], qam_signal[start_idx:end_idx], color=colors[symbols[i] % len(colors)])

axs[2].set_title("8-QAM Signal with Colors")
axs[2].set_xlabel("Time (s)")
axs[2].set_ylabel("Amplitude")
axs[2].grid()

# Espectro de frecuencia
axs[3].plot(frequencies[:len(frequencies)//2], fft_magnitude[:len(frequencies)//2], color='blue')
axs[3].set_title("8-QAM Frequency Spectrum")
axs[3].set_xlabel("Frequency (Hz)")
axs[3].set_ylabel("Magnitude")
axs[3].grid()

plt.tight_layout()
plt.show()

# Coordenadas de los símbolos 8QAM según la imagen
constellation_points = np.array([
    [1, 1],    # 000
    [2, 2],    # 001
    [-1, 1],   # 010
    [-2, 2],   # 011
    [-1, -1],  # 100
    [-2, -2],  # 101
    [1, -1],   # 110
    [2, -2]    # 111
])

# Etiquetas binarias para los puntos
labels = ['000', '001', '010', '011', '100', '101', '110', '111']

# Configurar el gráfico
plt.figure(figsize=(8, 8))
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.grid(alpha=0.5, linestyle='--')
plt.title("Diagrama Fasorial 8QAM")
plt.xlabel("Componente In-phase (I)")
plt.ylabel("Componente Quadrature (Q)")
plt.axis('equal')
plt.xlim(-3, 3)
plt.ylim(-3, 3)

# Dibujar fasores
for i, (x, y) in enumerate(constellation_points):
    # Dibujar vector desde el origen al punto
    plt.arrow(0, 0, x, y, head_width=0.1, head_length=0.15, fc='red', ec='red', alpha=0.7)

    # Mostrar etiqueta
    plt.text(x * 1.1, y * 1.1, labels[i], fontsize=12)

plt.show()
