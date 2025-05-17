import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import random

# Lista de tipos de codificación disponibles
TIPOS = [
    "CMI(code mark inversion)",
    "RZ(retorno a cero)",
    "NZR (Cero Sin Retorno)",
    "AMI(alternative mark inversion)",
    "Manchester Diferencial",
    "Manchester",
    "HDB3"
]

# Índice global de la gráfica actual
global current_idx
current_idx = 0
# Variable global para polaridad en HDB3; se inicializa en iniciar_aplicación
violation_polarity = None


def dibujar_grafica(numero, duty_cycle, tipo_grafica, frame):
    # Limpiar frame de dibujo
    for widget in frame.winfo_children():
        widget.destroy()

    # Color aleatorio para la señal
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    # Parámetros de la gráfica
    v = 1
    ylim_inf = -v - 0.2
    ylim_sup = v + 0.2

    # Convertir número a lista de bits
    binary_signal = list(map(int, str(numero)))

    # Generar la señal en función del tipo
    square_signal = []
    # Para HDB3, inicializamos el estado según la polaridad elegida
    if tipo_grafica == "HDB3":
        state = v if violation_polarity.get() == '+' else -v
    else:
        state = v

    for bit in binary_signal:
        if tipo_grafica == "HDB3":
            if bit == 1:
                square_signal.extend([state] * int(32 * duty_cycle / 100))
                square_signal.extend([0] * int(32 * (1 - duty_cycle / 100)))
                state = -state
            else:
                square_signal.extend([0] * 32)
        else:
            if bit == 1:
                square_signal.extend([state] * int(32 * duty_cycle / 100))
                square_signal.extend([0] * int(32 * (1 - duty_cycle / 100)))
                state = -state
            else:
                square_signal.extend([0] * 32)
        if tipo_grafica == "CMI(code mark inversion)":
            if bit == 1:
                square_signal.extend([state]*int(20*duty_cycle/100))
                square_signal.extend([0]*int(20*(1-duty_cycle/100)))
                state = -state  # Alternamos el estado
            else:
                square_signal.extend([-v]*int(10*duty_cycle/100))  # Primer segmento v-
                square_signal.extend([v]*int(10*duty_cycle/100))  # Segundo segmento v+
                square_signal.extend([0]*int(20*(1-duty_cycle/100)))
        elif tipo_grafica == "RZ(retorno a cero)":
            if bit == 1:
                square_signal.extend([v]*int(20*duty_cycle/100))  # Cuando el bit es 1, la señal es v+
                square_signal.extend([0]*int(20*(1-duty_cycle/100)))
            else:
                square_signal.extend([-v]*int(20*duty_cycle/100))  # Cuando el bit es 0, la señal es v-
                square_signal.extend([0]*int(20*(1-duty_cycle/100)))
        elif tipo_grafica == "NZR (Cero Sin Retorno)":
            if bit == 1:
                square_signal.extend([v]*int(20*duty_cycle/100))  # Cuando el bit es 1, la señal es v+
                square_signal.extend([0]*int(20*(1-duty_cycle/100)))
            else:
                square_signal.extend([0]*20)  # Cuando el bit es 0, la señal es 0 durante todo el ciclo
        elif tipo_grafica == "AMI(alternative mark inversion)":
            if bit==1:
                square_signal.extend([state]*int(20*duty_cycle/100))  # Cuando el bit es 1, la señal es state
                square_signal.extend([0]*int(20*(1-duty_cycle/100)))  # Luego vuelve a 0 durante el resto del ciclo
                state = -state  # Alternamos el estado
            else:
                square_signal.extend([0]*20)  # Cuando el bit es 0, la señal es 0 durante todo el ciclo
        elif tipo_grafica == "Manchester Diferencial":
            if bit==1:
                square_signal.extend([state]*int(10*duty_cycle/100))  # Primer segmento
                square_signal.extend([-state]*int(10*duty_cycle/100))  # Segundo segmento
                square_signal.extend([0]*int(20*(1-duty_cycle/100)))
            else:
                square_signal.extend([-state]*int(10*duty_cycle/100))  # Primer segmento
                square_signal.extend([state]*int(10*duty_cycle/100))  # Segundo segmento
                square_signal.extend([0]*int(20*(1-duty_cycle/100)))
            if square_signal[-1] != 0:  # Solo actualizamos el estado si la señal no es 0
               state = square_signal[-1]
        elif tipo_grafica == "Manchester":
            if bit==1:
                square_signal.extend([-state]*int(10*duty_cycle/100))  # Segundo segmento
                square_signal.extend([state]*int(10*duty_cycle/100))  # Primer segmento
                square_signal.extend([0]*int(20*(1-duty_cycle/100)))
            else:
                square_signal.extend([state]*int(10*duty_cycle/100))  # Primer segmento
                square_signal.extend([-state]*int(10*duty_cycle/100))  # Segundo segmento
                square_signal.extend([0]*int(20*(1-duty_cycle/100))) 

    signal = np.array(square_signal)
    x = np.linspace(0, len(signal) / 10, len(signal))

    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(0, len(signal) / 10)
    ax.set_ylim(ylim_inf, ylim_sup)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_xlabel('bits')
    ax.set_title(tipo_grafica)

    # Trazar señal
    ax.plot(x, signal, color=color)

    # Anotar bits
    for i, bit in enumerate(binary_signal):
        ax.text(i * (len(signal) / len(binary_signal)) + 0.5,
                ylim_sup - 0.1, str(bit), ha='center')

    # Renderizar en el frame de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)


def iniciar_aplicacion():
    global ventana, entry_numero, entry_duty_cycle, plot_frame, btn_prev, btn_next, label_tipo, current_idx, violation_polarity

    ventana = tk.Tk()
    ventana.title("Codificador de Señales Binarias")
    ventana.state('zoomed')

    # Inicializar variable de polaridad para HDB3
    violation_polarity = tk.StringVar(value='+')

    # Frame de entrada
    input_frame = ttk.Frame(ventana, padding=10)
    input_frame.pack(fill='x')

    ttk.Label(input_frame, text="Bits (0/1, máx 32):", font=('Arial', 12)).grid(row=0, column=0, sticky='w')
    entry_numero = ttk.Entry(input_frame, width=40, font=('Consolas', 14))
    entry_numero.grid(row=0, column=1, padx=5)
    vcmd = (ventana.register(lambda P: len(P) <= 32 and all(c in '01' for c in P)), '%P')
    entry_numero.config(validate='key', validatecommand=vcmd)

    ttk.Label(input_frame, text="Duty Cycle (% múltiplos de 10):", font=('Arial', 12)).grid(row=1, column=0, sticky='w')
    entry_duty_cycle = ttk.Entry(input_frame, width=10, font=('Consolas', 14))
    entry_duty_cycle.grid(row=1, column=1, sticky='w', padx=5)

    btn_start = ttk.Button(input_frame, text="Iniciar", command=mostrar_controles)
    btn_start.grid(row=0, column=2, rowspan=2, padx=10)

    # Frame para controles de navegación
    nav_frame = ttk.Frame(ventana, padding=10)
    nav_frame.pack(fill='x')

    btn_prev = ttk.Button(nav_frame, text="⟨ Atrás", command=lambda: navegar(-1), state='disabled')
    btn_prev.pack(side='left')
    label_tipo = ttk.Label(nav_frame, text="", width=30, anchor='center')
    label_tipo.pack(side='left', expand=True)
    btn_next = ttk.Button(nav_frame, text="Adelante ⟩", command=lambda: navegar(1), state='disabled')
    btn_next.pack(side='left')

    # Radiobuttons para polaridad de violación (sólo HDB3)
    ttk.Label(nav_frame, text="Polaridad Violación:").pack(side='left', padx=(20,5))
    ttk.Radiobutton(nav_frame, text='+', variable=violation_polarity, value='+').pack(side='left')
    ttk.Radiobutton(nav_frame, text='-', variable=violation_polarity, value='-').pack(side='left', padx=(0,20))

    # Frame para dibujar la gráfica
    plot_frame = ttk.Frame(ventana)
    plot_frame.pack(fill='both', expand=True)

    ventana.mainloop()


def mostrar_controles():
    global current_idx
    numero = entry_numero.get()
    duty = entry_duty_cycle.get()
    if len(numero) == 32 and duty.isdigit():
        dc = int(duty)
        if 0 <= dc <= 100 and dc % 10 == 0:
            current_idx = 0
            label_tipo.config(text=TIPOS[current_idx])
            btn_prev.config(state='disabled')
            btn_next.config(state='normal')
            dibujar_grafica(numero, dc, TIPOS[current_idx], plot_frame)
        else:
            messagebox.showerror("Error", "Duty cycle debe ser múltiplo de 10 entre 0 y 100.")
    else:
        messagebox.showerror("Error", "Número debe tener 32 bits (0/1) y Duty Cycle válido.")


def navegar(delta):
    global current_idx
    numero = entry_numero.get()
    dc = int(entry_duty_cycle.get())
    current_idx = (current_idx + delta) % len(TIPOS)
    dibujar_grafica(numero, dc, TIPOS[current_idx], plot_frame)
    label_tipo.config(text=TIPOS[current_idx])
    btn_prev.config(state='normal' if current_idx > 0 else 'disabled')
    btn_next.config(state='normal' if current_idx < len(TIPOS)-1 else 'disabled')


if __name__ == '__main__':
    iniciar_aplicacion()