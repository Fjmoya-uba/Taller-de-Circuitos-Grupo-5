import numpy as np
import matplotlib.pyplot as plt

# -------- FUNCION GENERAL PARA LEER ARCHIVOS DE LTSPICE --------
def leer_txt_ltspice(nombre_archivo):
    data = np.loadtxt(nombre_archivo, skiprows=1)
    x = data[:, 0]
    y = data[:, 1:]
    return x, y


# ============================================================
# 1) REGULACIÓN DE LÍNEA: Vo vs Vreg
# ============================================================
x, y = leer_txt_ltspice("Regulacion de Linea.txt")

plt.figure()

plt.plot(x, y[:, 0], color = 'black')

plt.xlabel(f'$V_{{reg}} [V]$')
plt.xlim(np.min(x), np.max(x))

plt.ylabel(f'$V_{{o}} [V]$')

plt.title("Regulación de Línea")
plt.grid()
plt.savefig("Regulacion_de_Linea.png")

# ============================================================
# 2) REGULACIÓN DE CARGA: Vo vs RL
# ============================================================
x, y = leer_txt_ltspice("Regulacion de Carga.txt")

plt.figure()
plt.plot(x, y[:, 0], color = 'black')

plt.xlabel(f'$R_{{L}} [\\Omega]$')
plt.xlim(np.min(x), np.max(x))

plt.ylabel(f'$V_{{o}} [V]$')

plt.title("Regulación de Carga")
plt.grid()
plt.savefig("Regulacion_de_Carga.png")

# ============================================================
# 3) CURVA FOLDBACK: Vo vs I(RL)
# ============================================================
x, y = leer_txt_ltspice("Curva Foldback.txt")

plt.figure()
plt.plot(x, y[:, 0], color = 'black')

plt.xlabel(f'$I_{{RL}} [A]$')
plt.xlim(np.min(x), np.max(x))

plt.ylabel(f'$V_{{o}} [V]$')
plt.title("Curva Foldback")
plt.grid()
plt.savefig("Curva_Foldback.png")

# ============================================================
# 4) GANANCIA DE LAZO: módulo y fase vs frecuencia
# ============================================================
def leer_ganancia_lazo(nombre_archivo):
    freq = []
    modulo = []
    fase = []

    with open(nombre_archivo, 'r') as f:
        next(f)  # saltear encabezado

        for linea in f:
            partes = linea.strip().split()

            # Columna 0: frecuencia
            f_val = float(partes[0])

            # Columna 1: "(XdB,Y°)"
            complejo = partes[1]

            # Limpiar string
            complejo = complejo.strip("()")
            mag_str, fase_str = complejo.split(',')

            # Sacar unidades
            mag = float(mag_str.replace('dB', ''))
            ph = float(fase_str.replace('°', ''))

            freq.append(f_val)
            modulo.append(mag)
            fase.append(ph)

    return np.array(freq), np.array(modulo), np.array(fase)


# =========================
# USO
# =========================
freq, modulo, fase = leer_ganancia_lazo("Ganancia de Lazo.txt")

# Crear subplots
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# --- Magnitud ---
ax1.set_xscale('log')
ax1.plot(freq, modulo, color = 'black')

ax1.set_xlabel("Frecuencia [Hz]")
ax1.set_xlim(np.min(freq), np.max(freq))

ax1.set_ylabel("Magnitud [dB]")
ax1.set_title("Diagrama de Bode")
ax1.grid(True, which="both")

# --- Fase ---
ax2.set_xscale('log')
ax2.plot(freq, fase, color = 'black')

ax2.set_xlabel("Frecuencia [Hz]")
ax2.set_xlim(np.min(freq), np.max(freq))

ax2.set_ylabel("Fase [°]")
ax2.grid(True, which="both")

plt.tight_layout()
plt.savefig("Bode.png")
plt.show()