import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd

# Parámetros de la modulación
M = 8  # Orden de la modulación PSK (16-PSK)
num_symbols = 8  # Número de símbolos a generar
sps = 100       # Muestras por símbolo
fs = 1000       # Frecuencia de muestreo (Hz)
fc = 50         # Frecuencia de la portadora (Hz)

# Generar datos aleatorios
data = np.random.randint(0, M, num_symbols)

# Modulación 16-PSK - Ángulos de cada símbolo
theta = 2 * np.pi * data / M

# Crear señal modulada en el tiempo
t = np.linspace(0, num_symbols * sps/fs, num_symbols * sps, endpoint=False)
signal = np.cos(2 * np.pi * fc * t + np.repeat(theta, sps))

# Crear figura con subplots
plt.figure(figsize=(18, 6))

# 1. Diagrama Fasorial
plt.subplot(1, 3, 1)
plt.title(f'Diagrama Fasorial {M} -PSK')
circle = plt.Circle((0, 0), 1, fill=False, color='gray', linestyle='--')
plt.gca().add_patch(circle)
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
constellation = np.exp(1j * 2 * np.pi * np.arange(M) / M)
for point in constellation:
    plt.arrow(0, 0, point.real, point.imag, 
              head_width=0.05, head_length=0.1, fc='blue', ec='blue')
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
plt.grid(True)
plt.xlabel('Componente In-Phase (I)')
plt.ylabel('Componente Quadrature (Q)')
plt.gca().set_aspect('equal', adjustable='box')

# 2. Diagrama de Constelación
plt.subplot(1, 3, 2)
plt.title(f'Diagrama de Constelación {M}-PSK')
plt.scatter(constellation.real, constellation.imag, color='red', marker='o')
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.grid(True)
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
plt.xlabel('Componente In-Phase (I)')
plt.ylabel('Componente Quadrature (Q)')
plt.gca().set_aspect('equal', adjustable='box')

# 3. Señal 16-PSK en el tiempo con colores randomizados por símbolo
plt.subplot(1, 3, 3)
plt.title(f'Señal {M}-PSK en el Tiempo')
for i in range(num_symbols):
    start = i * sps
    end = (i + 1) * sps
    color = np.random.rand(3,)  # Color aleatorio RGB
    plt.plot(t[start:end], signal[start:end], color=color, linewidth=1)
    start_time = i * sps/fs
    plt.axvline(x=start_time, color='r', linestyle='--', alpha=0.5)
    plt.text(start_time + 0.01, 1.1, f'ϕ={data[i]}', fontsize=8)

plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.ylim(-1.5, 1.5)
plt.xlim(0, num_symbols * sps/fs)

plt.tight_layout()
plt.show()



# Parámetros
M = 16  # Número de fases en PSK

# Coordenadas de la constelación (valores unitarios en el plano complejo)
constellation = np.exp(1j * 2 * np.pi * np.arange(M) / M)

# Crear tabla de verdad con símbolo binario, ángulo en radianes y grados
truth_table = []

for i in range(M):
    bits = f'{i:04b}'  # Conversión a binario de 4 bits
    angle_rad = np.angle(constellation[i])
    angle_deg = np.degrees(angle_rad)
    x = np.real(constellation[i])
    y = np.imag(constellation[i])
    truth_table.append((bits, round(angle_rad, 4), round(angle_deg, 1), round(x, 4), round(y, 4)))

# Crear DataFrame
df_truth = pd.DataFrame(truth_table, columns=["Símbolo (bin)", "Ángulo (rad)", "Ángulo (°)", "I (cos)", "Q (sen)"])

# Mostrar la tabla con print
df_truth.head(16)

print(df_truth)

