import numpy as np
import matplotlib.pyplot as plt

# Definir los tribits y las correspondientes amplitudes y fases
tribits = ['000', '001', '010', '011', '100', '101', '110', '111']
amplitudes = [0.765, 1.848, 0.765, 1.848, 0.765, 1.848, 0.765, 1.848]
fases = [-135, -135, -45, -45, 135, 135, 45, 45]

# Tiempo total de la señal
total_time = 8  # Suponiendo que cada tribit dura 1 segundo

# Crear una señal de tiempo discreto para cada tribit
t = np.linspace(0, total_time, total_time * 100)  # 100 samples per second
signal = np.zeros_like(t)

# Asignar la amplitud y fase a cada parte de la señal basada en el tribit
for i in range(len(tribits)):
    signal[i * 100:(i + 1) * 100] = amplitudes[i] * np.cos(2 * np.pi * t[i * 100:(i + 1) * 100] + np.deg2rad(fases[i]))

# Graficar la señal
plt.figure(figsize=(15, 5))
plt.plot(t, signal, label='8-QAM Signal')

# Anotar los tribits en la señal
for i, tribit in enumerate(tribits):
    plt.text(i + 0.5, 1.5, tribit, horizontalalignment='center')

# Ajustar detalles del gráfico
plt.title('8-QAM Signal Modulation')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.ylim(-2, 2)

# Mostrar el gráfico
plt.show()