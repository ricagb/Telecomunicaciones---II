import numpy as np
import matplotlib.pyplot as plt

# Función para generar la constelación QAM
def generate_qam_constellation(order):
    if order == 8:
        tribits = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]
        amplitudes = [0.765, 1.848] * 4
        phases = [-135, -135, -45, -45, 135, 135, 45, 45]
        puntos = [amp * np.exp(1j * np.radians(phase)) for amp, phase in zip(amplitudes, phases)]
        return tribits, puntos

    elif order == 16:
        levels = [-3, -1, 1, 3]
        tribits = []
        puntos = []
        index = 0
        for i in levels:
            for q in levels:
                bits = tuple(map(int, list(f'{index:04b}')))
                tribits.append(bits)
                puntos.append(complex(i, q))
                index += 1
        # Normalizar energía promedio
        puntos = np.array(puntos)
        puntos /= np.sqrt((np.mean(np.abs(puntos)**2)))
        return tribits, puntos

    else:
        raise ValueError("Solo se admite 8-QAM o 16-QAM")

# Parámetro para cambiar entre 8-QAM y 16-QAM
order = 16  # Cambiar entre 8 o 16

# Obtener la constelación
tribits, constellation = generate_qam_constellation(order)

# Crear mapeo
mapping = dict(zip(tribits, constellation))

# Diagrama de constelación
plt.figure(figsize=(6,6))
for tribit in tribits:
    point = mapping[tribit]
    plt.scatter(point.real, point.imag, label=str(tribit))
plt.grid(True)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.xlabel('In-Phase (I)')
plt.ylabel('Quadrature (Q)')
plt.title(f'Diagrama de Constelación {order}-QAM')
plt.legend(fontsize=8)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

# Diagrama vectorial
plt.figure(figsize=(8,8))
for tribit in tribits:
    point = mapping[tribit]
    plt.quiver(0, 0, point.real, point.imag, angles='xy', scale_units='xy', scale=1, label=str(tribit))

# Anotaciones
for tribit, point in mapping.items():
    plt.text(point.real, point.imag, f'{tribit}', fontsize=8, ha='right')

# Configuración del gráfico
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.xlabel('In-Phase (I)')
plt.ylabel('Quadrature (Q)')
plt.title(f'Diagrama Vectorial {order}-QAM')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
