import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1. Mapa de símbolos 8-PSK
symbol_map = {
    '000': np.exp(1j * 0),
    '001': np.exp(1j * np.pi/4),
    '010': np.exp(1j * np.pi/2),
    '011': np.exp(1j * 3*np.pi/4),
    '100': np.exp(1j * np.pi),
    '101': np.exp(1j * 5*np.pi/4),
    '110': np.exp(1j * 3*np.pi/2),
    '111': np.exp(1j * 7*np.pi/4)
}

# 2. Conversión bits → símbolos
def bits_to_symbols(bits):
    symbols = []
    for i in range(0, len(bits), 3):
        triplet = ''.join(map(str, bits[i:i+3]))
        if len(triplet) == 3:
            symbols.append(symbol_map[triplet])
    return np.array(symbols)

# 3. Conversión símbolo → bits
def symbol_to_bits(symbol):
    distances = {bits: abs(symbol - sym) for bits, sym in symbol_map.items()}
    return min(distances, key=distances.get)

# 4. Canal AWGN
def awgn_channel(symbols, snr_db):
    snr_linear = 10 ** (snr_db / 10)
    symbol_energy = np.mean(np.abs(symbols)**2)
    noise_variance = symbol_energy / snr_linear
    noise = np.sqrt(noise_variance / 2) * (np.random.randn(*symbols.shape) + 1j * np.random.randn(*symbols.shape))
    return symbols + noise

# 5. Simulación completa
def simulate_8psk_awgn(num_bits=399, snr_db=10):
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
    df = pd.DataFrame([(b, np.round(sym.real, 2), np.round(sym.imag, 2)) for b, sym in zip(bit_strings, coordinates)], columns=["Bits", "I", "Q"])

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    table.scale(1, 1.5)
    plt.title("Tabla de bits y símbolos 8-PSK")
    plt.show()

# 7. Diagrama de constelación ideal
def plot_constellation():
    plt.figure(figsize=(7, 7))
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')
    plt.grid(True)
    for bits, sym in symbol_map.items():
        plt.plot(sym.real, sym.imag, 'bo')
        plt.text(sym.real + 0.05, sym.imag + 0.05, bits, fontsize=10)
    plt.title("8-PSK - Diagrama de Constelación")
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
    for bits, sym in symbol_map.items():
        plt.arrow(0, 0, sym.real, sym.imag, head_width=0.05, head_length=0.1, fc='green', ec='green')
        plt.text(sym.real + 0.05, sym.imag + 0.05, bits, fontsize=10)
    plt.title("8-PSK - Diagrama Fasorial")
    plt.xlabel("In-phase (I)")
    plt.ylabel("Quadrature (Q)")
    plt.axis('equal')
    plt.show()

# 9. Señal senoidal modulada (con amplitud configurable)
def plot_modulated_signal(symbols, carrier_freq=1000, sample_rate=100000, symbol_duration=0.001, amplitude=1):
    samples_per_symbol = int(sample_rate * symbol_duration)
    t = np.arange(0, samples_per_symbol * len(symbols)) / sample_rate
    signal = np.zeros_like(t)

    for i, s in enumerate(symbols):
        i_comp = s.real
        q_comp = s.imag
        t_symbol = t[i * samples_per_symbol : (i + 1) * samples_per_symbol]
        modulated = amplitude * (i_comp * np.cos(2 * np.pi * carrier_freq * t_symbol) -
                                 q_comp * np.sin(2 * np.pi * carrier_freq * t_symbol))
        signal[i * samples_per_symbol : (i + 1) * samples_per_symbol] = modulated

    plt.figure(figsize=(12, 4))
    plt.plot(t[:5 * samples_per_symbol], signal[:5 * samples_per_symbol])
    plt.title("Señal modulada en 8-PSK (senoidal)")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 10. Codificaciones de línea
def plot_line_coding(bits):
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
    def hdb3(bits):
        result, count, polarity = [], 0, 1
        for b in bits:
            if b == 1:
                result.append(polarity)
                polarity *= -1
                count = 0
            else:
                count += 1
                if count == 4:
                    result[-3] = polarity
                    result.extend([0, 0, 0, -polarity])
                    polarity *= -1
                    count = 0
                else:
                    result.append(0)
        return np.array(result)

    codings = {
        "RZ": rz(bits), "NRZ": nrz(bits), "AMI": ami(bits),
        "Manchester": manchester(bits), "Manchester Diferencial": diff_manchester(bits),
        "CMI": cmi(bits), "HDB3": hdb3(bits)
    }

    plt.figure(figsize=(12, 10))
    for i, (name, signal) in enumerate(codings.items()):
        plt.subplot(len(codings), 1, i + 1)
        plt.step(range(len(signal)), signal, where='post')
        plt.title(name)
        plt.ylim(-4, 4)
        plt.grid(True)
    plt.tight_layout()
    plt.show()

# 11. Ejecutar todo
if __name__ == "__main__":
    plot_bit_table()
    plot_constellation()
    plot_vector_diagram()

    bits_tx, bits_rx, ber, symbols_tx, symbols_rx = simulate_8psk_awgn(num_bits=399, snr_db=10)
    print(f"Bit Error Rate (BER): {ber:.4f}")

    plot_modulated_signal(symbols_tx, amplitude=0.5)
    plot_line_coding(bits_tx[:32])
