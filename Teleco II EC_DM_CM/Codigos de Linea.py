import matplotlib.pyplot as plt
import numpy as np

# Codificadores
def rz_encode(bits):
    signal = []
    for bit in bits:
        if bit == 1:
            signal.extend([1, 0])
        else:
            signal.extend([0, 0])
    return signal

def nrz_encode(bits):
    return [bit for bit in bits for _ in range(2)]

def ami_encode(bits):
    signal = []
    polarity = 1
    for bit in bits:
        if bit == 1:
            signal.extend([polarity, polarity])
            polarity *= -1
        else:
            signal.extend([0, 0])
    return signal

def cmi_encode(bits):
    signal = []
    last = -1
    for bit in bits:
        if bit == 0:
            signal.extend([0, 1])
        else:
            last *= -1
            signal.extend([last, 1])
    return signal

def manchester_encode(bits):
    signal = []
    for bit in bits:
        if bit == 1:
            signal.extend([1, -1])
        else:
            signal.extend([-1, 1])
    return signal

def manchester_differential(bits):
    signal = []
    current = 1  # Estado inicial
    for bit in bits:
        if bit == 1:
            current *= -1  # Transición al inicio
        signal.extend([current, -current])
    return signal

# Graficador
def plot_signal(signal, title):
    y = np.repeat(signal, 2)
    t = np.arange(len(y))
    plt.figure(figsize=(12, 3))
    plt.plot(t, y, drawstyle='steps-pre')
    plt.title(f"Codificación {title}")
    plt.ylim([-2, 2])
    plt.grid(True)
    plt.xlabel("Tiempo")
    plt.ylabel("Nivel")
    plt.yticks([-1, 0, 1])
    plt.show()

# Programa principal
def main():
    print("=== CÓDIGOS DE LÍNEA ===")
    print("1 - RZ (Return to Zero)")
    print("2 - NRZ (Non-Return to Zero)")
    print("3 - AMI (Alternate Mark Inversion)")
    print("4 - CMI (Coded Mark Inversion)")
    print("5 - Manchester")
    print("6 - Manchester Diferencial")

    choice = input("Elige el número del código de línea a usar: ").strip()

    bits_str = input("Ingresa la secuencia binaria separada por espacios (ej: 1 0 1 1 0): ")
    bits = [int(b) for b in bits_str.split()]

    if choice == '1':
        signal = rz_encode(bits)
        nombre = "RZ"
    elif choice == '2':
        signal = nrz_encode(bits)
        nombre = "NRZ"
    elif choice == '3':
        signal = ami_encode(bits)
        nombre = "AMI"
    elif choice == '4':
        signal = cmi_encode(bits)
        nombre = "CMI"
    elif choice == '5':
        signal = manchester_encode(bits)
        nombre = "Manchester"
    elif choice == '6':
        signal = manchester_differential(bits)
        nombre = "Manchester Diferencial"
    else:
        print("⚠️ Opción inválida.")
        return

    # Mostrar resultados
    print(f"\n🔢 Señal codificada ({nombre}):")
    print(signal)

    plot_signal(signal, nombre)

if __name__ == "__main__":
    main()
