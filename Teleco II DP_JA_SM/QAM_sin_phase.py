import numpy as np
import matplotlib.pyplot as plt

# Definir coordenadas de 16-QAM según la imagen (valores normalizados)
levels = [-3/np.sqrt(5), -1/np.sqrt(5), 1/np.sqrt(5), 3/np.sqrt(5)]
qam_points = []
bit_labels = []

# Crear los puntos y sus etiquetas de bits
bit_index = 0
for q in reversed(levels):  # cuadrante superior primero (imagen)
    for i in levels:
        point = complex(i, q)
        qam_points.append(point)
        bit_labels.append(f'{bit_index:04b}')
        bit_index += 1

qam_points = np.array(qam_points)

# Calcular amplitudes y fases (en grados)
amplitudes = np.abs(qam_points)
phases = np.angle(qam_points, deg=True)

# Graficar la constelación y valores de amplitud/fase
fig, ax = plt.subplots(figsize=(8, 8))
ax.axhline(0, color='gray', linestyle='--')
ax.axvline(0, color='gray', linestyle='--')
ax.grid(True)
ax.set_title("Constelación 16-QAM con Amplitudes y Fases")
ax.set_xlabel("Componente In-Phase (I)")
ax.set_ylabel("Componente Quadrature (Q)")

for point, label, amp, phase in zip(qam_points, bit_labels, amplitudes, phases):
    ax.plot(point.real, point.imag, 'ko')
    ax.text(point.real, point.imag + 0.05, f'{label}\nA={amp:.2f}, ϕ={phase:.1f}°',
            ha='center', va='bottom', fontsize=8)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
plt.show()

# Generar la señal en el tiempo por símbolo con su amplitud y fase
t_base = np.linspace(0, 2 * np.pi, 1000)
fig, ax = plt.subplots(figsize=(14, 6))

for i, (symbol, amplitude, phase_rad) in enumerate(zip(bit_labels, amplitudes, np.angle(qam_points))):
    t_shifted = t_base + i * 2 * np.pi
    y = amplitude * np.sin(t_shifted + phase_rad)
    ax.plot(t_shifted, y, label=f'{symbol} | A={amplitude:.2f}, ϕ={np.degrees(phase_rad):.1f}°')

    if i < len(bit_labels) - 1:
        ax.axvline(x=(i + 1) * 2 * np.pi, color='black', linestyle='--', linewidth=0.5)

ax.set_xticks([i * 2 * np.pi for i in range(len(bit_labels))])
ax.set_xticklabels(bit_labels, rotation=45)
ax.set_xlabel('Símbolos (bits)')
ax.set_ylabel('Amplitud')
ax.set_title('Señal de 16-QAM en el Tiempo por Símbolos (con Amplitud y Fase)')
ax.grid(True)
plt.tight_layout()
plt.show()
