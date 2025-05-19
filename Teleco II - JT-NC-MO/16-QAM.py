import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1. Mapa de símbolos 16-QAM
symbol_map = {
    '0000': (-3, -3), '0001': (-3, -1), '0010': (-3, 3), '0011': (-3, 1),
    '0100': (-1, -3), '0101': (-1, -1), '0110': (-1, 3), '0111': (-1, 1),
    '1000': (3, -3),  '1001': (3, -1),  '1010': (3, 3),  '1011': (3, 1),
    '1100': (1, -3),  '1101': (1, -1),  '1110': (1, 3),  '1111': (1, 1)
}

# 2. Conversión bits → símbolos
def bits_to_symbols(bits):
    symbols = []
    for i in range(0, len(bits), 4):
        quad = ''.join(map(str, bits[i:i+4]))
        if len(quad) == 4:
            i_val, q_val = symbol_map[quad]
            symbols.append(complex(i_val, q_val))
    return np.array(symbols)

# 3. Conversión símbolo → bits
def symbol_to_bits(symbol):
    distances = {bits: abs(symbol - complex(i, q)) for bits, (i, q) in symbol_map.items()}
    return min(distances, key=distances.get)

# 4. Canal AWGN
def awgn_channel(symbols, snr_db):
    snr_linear = 10 ** (snr_db / 10)
    symbol_energy = np.mean(np.abs(symbols)**2)
    noise_variance = symbol_energy / snr_linear
    noise = np.sqrt(noise_variance / 2) * (np.random.randn(*symbols.shape) + 1j * np.random.randn(*symbols.shape))
    return symbols + noise

# 5. Simulación completa
def simulate_16qam_awgn(num_bits=400, snr_db=10):
    bits_tx = np.random.randint(0, 2, num_bits)
    symbols_tx = bits_to_symbols(bits_tx)
    symbols_rx = awgn_channel(symbols_tx, snr_db)

    bits_rx = []
    for sym in symbols_rx:
        bits = symbol_to_bits(sym)
        bits_rx.extend([int(b) for b in bits])

    bits_rx = np.array(bits_rx[:len(bits_tx)])
    ber = np.mean(bits_tx != bits_rx)
    return bits_tx, bits_rx, ber, symbols_tx, symbols_rx

# 6. Tabla de bits

def plot_bit_table():
    bit_strings = list(symbol_map.keys())
    coordinates = [symbol_map[b] for b in bit_strings]
    df = pd.DataFrame(coordinates, columns=["I", "Q"])
    df["Bits"] = bit_strings
    df = df[["Bits", "I", "Q"]]

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    table.scale(1, 1.5)
    plt.title("Tabla de bits y símbolos 16-QAM")
    plt.show()

# 7. Diagrama de constelación ideal
def plot_constellation():
    plt.figure(figsize=(7, 7))
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')
    plt.grid(True)
    for bits, (i, q) in symbol_map.items():
        plt.plot(i, q, 'bo')
        plt.text(i + 0.1, q + 0.1, bits, fontsize=10)
    plt.title("16-QAM - Diagrama de Constelación")
    plt.xlabel("In-phase (I)")
    plt.ylabel("Quadrature (Q)")
    plt.axis('equal')
    plt.show()

# 8. Diagrama fasorial
def plot_vector_diagram():
    plt.figure(figsize=(8, 7))
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')
    plt.grid(True)
    for bits, (i, q) in symbol_map.items():
        plt.arrow(0, 0, i, q, head_width=0.2, head_length=0.2, fc='green', ec='green')
        plt.text(i + 0.1, q + 0.1, bits, fontsize=10)
    plt.title("16-QAM - Diagrama Fasorial")
    plt.xlabel("In-phase (I)")
    plt.ylabel("Quadrature (Q)")
    plt.axis('equal')
    plt.show()

# 9. Señal senoidal modulada (con amplitud configurable)
def plot_modulated_signal(symbols, carrier_freq=1000, sample_rate=100000, symbol_duration=0.001, amplitude=0.5):
    t = np.arange(0, symbol_duration * len(symbols), 1 / sample_rate)
    signal = np.zeros_like(t)
    samples_per_symbol = int(sample_rate * symbol_duration)

    for i, s in enumerate(symbols):
        i_comp = s.real
        q_comp = s.imag
        t_symbol = t[i * samples_per_symbol : (i + 1) * samples_per_symbol]
        modulated = amplitude * (i_comp * np.cos(2 * np.pi * carrier_freq * t_symbol) -
                                 q_comp * np.sin(2 * np.pi * carrier_freq * t_symbol))
        signal[i * samples_per_symbol : (i + 1) * samples_per_symbol] = modulated

    plt.figure(figsize=(12, 4))
    plt.plot(t[:5 * samples_per_symbol], signal[:5 * samples_per_symbol])
    plt.title("Señal modulada en 16-QAM (senoidal)")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 10. Codificaciones de línea
def hdb3(bits):
    result = []
    fill_info = []
    last_polarity = -1
    pulse_count = 0
    zero_count = 0
    i = 0
    while i < len(bits):
        bit = bits[i]
        if bit == 1:
            last_polarity *= -1
            result.append(last_polarity)
            pulse_count += 1
            zero_count = 0
            i += 1
        else:
            zero_count += 1
            if zero_count == 4:
                if pulse_count % 2 == 0:
                    b = last_polarity
                    v = -last_polarity
                    result.append(b)
                    fill_info.append((len(result)-1, 'B'))
                    result.extend([0, 0])
                    result.append(v)
                    fill_info.append((len(result)-1, 'V'))
                    last_polarity = v
                else:
                    result.extend([0, 0, 0])
                    v = -last_polarity
                    result.append(v)
                    fill_info.append((len(result)-1, 'V'))
                    last_polarity = v
                pulse_count = 0
                zero_count = 0
                i += 1
            else:
                result.append(0)
                i += 1
    return np.array(result), fill_info

def plot_line_coding(bits, invertir_hdb3=False):
    def rz(bits): return np.array([[b, 0] for b in bits]).flatten()
    def nrz(bits): return np.array(bits)
    def ami(bits):
        signal, polarity = [], 1
        for b in bits:
            signal.append(polarity if b else 0)
            if b: polarity *= -1
        return np.array(signal)
    def manchester(bits): return np.array([1 if b == 0 else -1 for b in bits for _ in (0, 1)]) * np.tile([1, -1], len(bits))
    def diff_manchester(bits):
        signal, last = [], -1
        for b in bits:
            if b == 0: last *= -1
            signal.extend([last, -last])
        return np.array(signal)
    def cmi(bits):
        signal, last = [], 1
        for b in bits:
            if b == 0: signal.extend([0, 1])
            else: last *= -1; signal.extend([last, 1])
        return np.array(signal)

    hdb3_signal, rellenos = hdb3(bits)
    if invertir_hdb3:
        hdb3_signal *= -1

    codings = {
        "RZ": rz(bits),
        "NRZ": nrz(bits),
        "AMI": ami(bits),
        "Manchester": manchester(bits),
        "Manchester Diferencial": diff_manchester(bits),
        "CMI": cmi(bits),
        "HDB3": hdb3_signal
    }

    plt.figure(figsize=(12, 10))
    for i, (name, signal) in enumerate(codings.items()):
        plt.subplot(len(codings), 1, i + 1)
        plt.step(range(len(signal)), signal, where='post')
        plt.title(name + (" (invertido)" if name == "HDB3" and invertir_hdb3 else ""))
        plt.ylim(-4, 4)
        plt.grid(True)
        if name == "HDB3":
            for pos, tipo in rellenos:
                plt.text(pos + 0.1, signal[pos] + 0.5, tipo, fontsize=10, color='red')
    plt.tight_layout()
    plt.show()

    if rellenos:
        print("\n>>> Pulsos de Relleno Detectados en HDB3:")
        for pos, tipo in rellenos:
            print(f"  Pulso '{tipo}' en la posición {pos}")

# 11. Ejecutar todo
if __name__ == "__main__":
    plot_bit_table()
    plot_constellation()
    plot_vector_diagram()

    while True:
        entrada = input("\nIngresa una secuencia de bits (solo 0 y 1) o 'salir' para terminar: ").strip()
        if entrada.lower() == 'salir':
            print("Saliendo...")
            break

        if any(c not in '01' for c in entrada) or len(entrada) == 0:
            print("Error: La secuencia debe contener solo 0 y 1 y no estar vacía.")
            continue

        bits_manual = [int(b) for b in entrada]
        print(f"Secuencia bits ingresada (longitud {len(bits_manual)}): {bits_manual}")

        invertir = input("\u00bfInvertir señal HDB3? '+' para normal, '-' para invertir: ").strip() == '-'
        plot_line_coding(bits_manual, invertir_hdb3=invertir)

    bits_tx, bits_rx, ber, symbols_tx, symbols_rx = simulate_16qam_awgn(num_bits=400, snr_db=10)
    print(f"Bit Error Rate (BER) con bits aleatorios: {ber:.4f}")
    plot_modulated_signal(symbols_tx, amplitude=0.3)
