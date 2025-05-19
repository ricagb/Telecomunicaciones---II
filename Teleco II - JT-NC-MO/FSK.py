import numpy as np
import matplotlib.pyplot as plt

# 1. Generar bits aleatorios
def generate_bits(num_bits):
    return np.random.randint(0, 2, num_bits)

# 2. Modulación 2-FSK
def fsk_modulation(bits, f1=1000, f2=2000, sample_rate=100000, symbol_duration=0.001):
    t = np.arange(0, symbol_duration * len(bits), 1 / sample_rate)
    signal = np.zeros_like(t)
    samples_per_symbol = int(sample_rate * symbol_duration)

    for i, bit in enumerate(bits):
        freq = f1 if bit == 0 else f2
        t_symbol = t[i * samples_per_symbol : (i + 1) * samples_per_symbol]
        signal[i * samples_per_symbol : (i + 1) * samples_per_symbol] = np.cos(2 * np.pi * freq * t_symbol)

    return signal, t

# 3. Canal AWGN
def awgn_channel(signal, snr_db):
    snr_linear = 10 ** (snr_db / 10)
    power_signal = np.mean(signal ** 2)
    noise_variance = power_signal / snr_linear
    noise = np.sqrt(noise_variance) * np.random.randn(len(signal))
    return signal + noise

# 4. Demodulación 2-FSK (detección por correlación)
def fsk_demodulation(received_signal, f1=1000, f2=2000, sample_rate=100000, symbol_duration=0.001):
    samples_per_symbol = int(sample_rate * symbol_duration)
    num_symbols = len(received_signal) // samples_per_symbol
    bits_rx = []
    t_symbol = np.arange(0, symbol_duration, 1 / sample_rate)

    ref_wave_0 = np.cos(2 * np.pi * f1 * t_symbol)
    ref_wave_1 = np.cos(2 * np.pi * f2 * t_symbol)

    for i in range(num_symbols):
        segment = received_signal[i * samples_per_symbol : (i + 1) * samples_per_symbol]
        corr_0 = np.sum(segment * ref_wave_0)
        corr_1 = np.sum(segment * ref_wave_1)
        bit = 0 if corr_0 > corr_1 else 1
        bits_rx.append(bit)

    return np.array(bits_rx)

# 5. Simulación completa
def simulate_2fsk_awgn(num_bits=300, snr_db=10):
    bits_tx = generate_bits(num_bits)
    signal_tx, t = fsk_modulation(bits_tx)
    signal_rx = awgn_channel(signal_tx, snr_db)
    bits_rx = fsk_demodulation(signal_rx)
    ber = np.mean(bits_tx != bits_rx)
    return bits_tx, bits_rx, ber, signal_tx, signal_rx, t

# 6. Graficar señales
def plot_fsk_signal(t, signal, title="Señal modulada 2-FSK"):
    plt.figure(figsize=(12, 4))
    plt.plot(t, signal)
    plt.title(title)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 7. Ejecutar simulación
if __name__ == "__main__":
    bits_tx, bits_rx, ber, signal_tx, signal_rx, t = simulate_2fsk_awgn(num_bits=300, snr_db=10)
    print(f"Bit Error Rate (BER): {ber:.4f}")
    plot_fsk_signal(t, signal_tx, title="Señal 2-FSK modulada (transmitida)")
    plot_fsk_signal(t, signal_rx, title="Señal 2-FSK recibida con ruido AWGN")
S