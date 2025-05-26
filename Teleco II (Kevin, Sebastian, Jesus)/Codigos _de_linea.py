#Codigos de linea
# FUNCIONES DE CÓDIGOS DE LÍNEA
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display



def codigo_nrz(bits, fs):
    return np.repeat(bits, fs)

def codigo_rz(bits, fs):
    rz = []
    for b in bits:
        mitad = int(fs / 2)
        if b == 1:
            rz.extend([1]*mitad + [0]*mitad)
        else:
            rz.extend([-1]*mitad + [0]*mitad)
    return np.array(rz)

def codigo_ami(bits, fs):
    ami = []
    last = -1
    for b in bits:
        if b == 0:
            ami.extend([0]*fs)
        else:
            last *= -1
            ami.extend([last]*fs)
    return np.array(ami)

def codigo_cmi(bits, fs):
    cmi = []
    last = 1
    for b in bits:
        if b == 0:
            last *= -1
            cmi.extend([last]*fs)
        else:
            mitad = int(fs / 2)
            cmi.extend([1]*mitad + [-1]*mitad)
    return np.array(cmi)

def codigo_hdb3(bits, fs):
    hdb3 = []
    v_count = 0
    cero_count = 0
    bipolar = -1
    new_bits = []

    for b in bits:
        if b == 1:
            new_bits.append(1)
            cero_count = 0
            v_count += 1
        else:
            cero_count += 1
            if cero_count == 4:
                if v_count % 2 == 0:
                    new_bits[-3:] = [0, 0, 0]
                    new_bits.append(-1)  # Violación
                    v_count += 1
                else:
                    new_bits[-3:] = [0, 0, 0]
                    new_bits.append(1)
                    new_bits[-4] = -1
                    v_count = 0
                cero_count = 0
            else:
                new_bits.append(0)

    for b in new_bits:
        if b == 1:
            bipolar *= -1
            hdb3.extend([bipolar]*fs)
        elif b == -1:
            hdb3.extend([-bipolar]*fs)
        else:
            hdb3.extend([0]*fs)
    return np.array(hdb3)

def codigo_manchester(bits, fs):
    man = []
    for b in bits:
        mitad = int(fs / 2)
        if b == 1:
            man.extend([1]*mitad + [-1]*mitad)
        else:
            man.extend([-1]*mitad + [1]*mitad)
    return np.array(man)

def codigo_manchester_diferencial(bits, fs):
    man_diff = []
    last = -1
    for b in bits:
        mitad = int(fs / 2)
        if b == 1:
            last *= -1
        man_diff.extend([last]*mitad + [-last]*mitad)
    return np.array(man_diff)

def codigo_mlt3(bits, fs):
    mlt3 = []
    last = 0
    next_val = 1
    for b in bits:
        if b == 0:
            mlt3.extend([last]*fs)
        else:
            if last == 0:
                last = next_val
            elif last == next_val:
                last = 0
            elif last == -next_val:
                last = next_val
            mlt3.extend([last]*fs)
    return np.array(mlt3)

# ENTRADA DE DATOS

entrada = input("Ingrese la secuencia de bits (ej: 1011001): ")
bits = [int(b) for b in entrada.strip()]
fs = 100  # muestras por bit
t = np.linspace(0, len(bits), len(bits)*fs)

# GRAFICAR TODOS LOS CÓDIGOS
codigos = {
    "NRZ": codigo_nrz(bits, fs),
    "RZ": codigo_rz(bits, fs),
    "AMI": codigo_ami(bits, fs),
    "CMI": codigo_cmi(bits, fs),
    "HDB3": codigo_hdb3(bits, fs),
    "Manchester": codigo_manchester(bits, fs),
    "Manchester Dif.": codigo_manchester_diferencial(bits, fs),
    "MLT-3": codigo_mlt3(bits, fs),
}

plt.figure(figsize=(12, 18))

colores = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'teal', 'magenta']

for i, (nombre, señal) in enumerate(codigos.items(), start=1):
    plt.subplot(8, 1, i)
    plt.plot(t, señal, drawstyle='steps-pre', color=colores[i-1])
    plt.title(f"Código de Línea: {nombre}")
    plt.ylim(-2, 2)
    plt.title(f"Código de Línea: {nombre}")
    plt.ylim(-2, 2)
    plt.grid(True)
    plt.ylabel("Nivel")

plt.xlabel("Tiempo [bits]")
plt.tight_layout()
plt.show()
