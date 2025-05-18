import matplotlib.pyplot as plt
import numpy as np

def get_binary_data():
    while True:
        try:
            input_str = input("Ingrese la secuencia de bits binarios (ej: 10110): ").strip()
            data = [int(bit) for bit in input_str if bit in ('0', '1')]
            if len(data) == len(input_str):
                return data
            else:
                print("Solo puede ingresar 0s y 1s. Inténtelo de nuevo.")
        except:
            print("Entrada inválida. Inténtelo de nuevo.")

def ask_hdb3_violation():
    while True:
        viol = input("Para HDB3, ingrese el tipo de violación (n para negativa, p para positiva): ").strip().lower()
        if viol == 'n':
            return -1  # Violacion negativa
        elif viol == 'p':
            return 1    # Violacion positiva
        else:
            print("Entrada inválida. Ingrese 'n' o 'p'.")

def plot_signal(time, signal, title, ylim=(-3,3), v_points=None, b_points=None):
    plt.figure(figsize=(12, 3))
    plt.step(time, signal, where='post', linewidth=2)
    plt.title(title)
    plt.ylim(ylim)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.axhline(0, color='black', linewidth=0.8)

    # If violation points are supplied for HDB3, plot "V" marks
    if v_points:
        for t, y, polarity in v_points:
            plt.text(t, y, 'V', fontsize=18, fontweight='bold', color='red',
                     verticalalignment='bottom' if polarity>0 else 'top', horizontalalignment='center')

    # If balancing pulse points are supplied for HDB3, plot "B" marks
    if b_points:
        for t, y, polarity in b_points:
            plt.text(t, y, 'B', fontsize=18, fontweight='bold', color='blue',
                     verticalalignment='bottom' if polarity>0 else 'top', horizontalalignment='center')

    plt.show()

def nrz(data):
    signal = [1 if bit == 1 else 0 for bit in data for _ in range(2)]
    time = np.arange(len(signal))
    return time, signal

def rz(data):
    signal = []
    for bit in data:
        signal.extend([1, 0] if bit == 1 else [0, 0])
    time = np.arange(len(signal))
    return time, signal

def ami(data):
    signal = []
    last_level = -1
    for bit in data:
        if bit == 0:
            signal.extend([0, 0])
        else:
            last_level = -last_level
            signal.extend([last_level, last_level])
    time = np.arange(len(signal))
    return time, signal

def cmi(data):
    signal = []
    last_level = -1
    for bit in data:
        if bit == 0:
            signal.extend([0, 1])
        else:
            last_level = -last_level
            signal.extend([last_level, last_level])
    time = np.arange(len(signal))
    return time, signal

def manchester(data):
    signal = []
    for bit in data:
        signal.extend([0, 1] if bit == 1 else [1, 0])
    time = np.arange(len(signal))
    return time, signal

def differential_manchester(data):
    signal = []
    current_level = 1
    for bit in data:
        if bit == 0:
            current_level = 1 - current_level
            signal.extend([current_level, 1 - current_level])
        else:
            signal.extend([current_level, 1 - current_level])
        current_level = signal[-1]
    time = np.arange(len(signal))
    return time, signal

def hdb3(data, violation_polarity):
    encoded = []
    last_pulse = -violation_polarity
    zero_count = 0
    pulse_count = 0
    v_points = []
    b_points = []
    time_index = 0

    for i, bit in enumerate(data):
        if bit == 1:
            zero_count = 0
            last_pulse = -last_pulse
            encoded.append(last_pulse)
            pulse_count += 1
            time_index += 1
        else:
            zero_count += 1
            if zero_count < 4:
                encoded.append(0)
                time_index += 1
            else:
                for _ in range(3):
                    encoded.pop()

                if pulse_count % 2 == 0:
                    encoded.extend([0, 0, 0, violation_polarity])
                    v_points.append((time_index + 3, violation_polarity * 1.2, violation_polarity))
                else:
                    b_polarity = last_pulse
                    encoded.extend([b_polarity, 0, 0, violation_polarity])
                    v_points.append((time_index + 3, violation_polarity * 1.2, violation_polarity))
                    b_points.append((time_index, b_polarity * 1.2, b_polarity)) # Mark the B pulse
                last_pulse = violation_polarity
                zero_count = 0
                pulse_count = 0
                time_index += 1

    signal = [level for level in encoded for _ in range(2)]
    time = np.arange(len(signal))

    v_points_scaled = [(t_raw * 2 + 1, y, pol) for t_raw, y, pol in v_points]
    b_points_scaled = [(t_raw * 2 + 1, y, pol) for t_raw, y, pol in b_points]

    return time, signal, v_points_scaled, b_points_scaled

def main():
    data = get_binary_data()
    violation_polarity = ask_hdb3_violation()

    time_nrz, signal_nrz = nrz(data)
    time_rz, signal_rz = rz(data)
    time_ami, signal_ami = ami(data)
    time_cmi, signal_cmi = cmi(data)
    time_man, signal_man = manchester(data)
    time_dman, signal_dman = differential_manchester(data)
    time_hdb3, signal_hdb3, v_points, b_points = hdb3(data, violation_polarity)

    plot_signal(time_nrz, signal_nrz, "NRZ")
    plot_signal(time_rz, signal_rz, "RZ")
    plot_signal(time_ami, signal_ami, "AMI")
    plot_signal(time_cmi, signal_cmi, "CMI")
    plot_signal(time_man, signal_man, "Manchester")
    plot_signal(time_dman, signal_dman, "Differential Manchester")
    plot_signal(time_hdb3, signal_hdb3, "HDB3", ylim=(-2,2), v_points=v_points, b_points=b_points)

if __name__ == "__main__":
    main()