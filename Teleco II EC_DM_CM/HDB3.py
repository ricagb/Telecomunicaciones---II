import matplotlib.pyplot as plt
import numpy as np

def hdb3_encode(data_bits):
    output = []
    last_polarity = -1
    zero_count = 0
    pulse_count = 0
    
    for bit in data_bits:
        if bit == 1:
            zero_count = 0
            last_polarity *= -1
            output.append(last_polarity)
            pulse_count += 1
        else:
            zero_count += 1
            if zero_count == 4:
                if pulse_count % 2 == 0:
                    # Regla 1: B00V (número de 1's desde última violación es par)
                    output[-3:] = [0, 0, 0]  # eliminamos 3 ceros anteriores
                    output.append(last_polarity)  # B con misma polaridad
                else:
                    # Regla 2: 000V (número impar de 1's)
                    output[-3:] = [0, 0, 0]  # eliminamos 3 ceros anteriores
                    last_polarity *= -1
                    output.append(last_polarity)  # V rompe alternancia
                zero_count = 0
                pulse_count = 0
            else:
                output.append(0)
    return output

def main():
    print("=== CODIFICACIÓN HDB3 ===")
    print("Regla 1: Reemplaza 0000 por B00V (si el número de 1's desde la última violación es PAR)")
    print("Regla 2: Reemplaza 0000 por 000V (si el número de 1's desde la última violación es IMPAR)")
    regla = input("¿Quieres aplicar ambas reglas automáticamente? (s/n): ").strip().lower()

    bits_str = input("Ingresa la secuencia binaria separada por espacios (ej: 1 0 0 0 0 1 0 1): ")
    data_bits = [int(b) for b in bits_str.split()]
    
    encoded = hdb3_encode(data_bits)

    print("\nSecuencia codificada (HDB3):")
    print(encoded)

    # Gráfica
    t = np.arange(0, len(encoded) + 1)
    signal = np.repeat(encoded, 2)
    t = np.repeat(t, 2)[1:-1]

    plt.figure(figsize=(12, 3))
    plt.plot(t, signal, drawstyle='steps-pre')
    plt.title("Señal codificada HDB3")
    plt.ylim([-2, 2])
    plt.grid(True)
    plt.yticks([-1, 0, 1])
    plt.xlabel("Tiempo")
    plt.ylabel("Nivel")
    plt.xticks(np.arange(len(data_bits)+1), labels=np.arange(len(data_bits)+1))
    plt.show()

if __name__ == "__main__":
    main()
