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
plt.axvline(x = 6, linestyle = '--', color='red', linewidth=2, label='Vreg = 6V')
plt.text(6.5, plt.ylim()[1]*0, '6V', ha='center', fontsize=9, color='red')

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
datos = np.loadtxt("Curva Foldback.txt", skiprows=1)
x = datos[:, 2]  # I(RL)
y = datos[:, 1:]  # Vo


plt.figure()
plt.plot(x, y[:, 0], color = 'black')

plt.xlabel(f'$I_{{RL}} [A]$')
plt.xlim(np.min(x), 1.5)

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
freq, modulo5, fase5 = leer_ganancia_lazo("Ganancia de Lazo(R5).txt")
freq, modulo10, fase10 = leer_ganancia_lazo("Ganancia de Lazo(R10).txt")
freq, modulo50, fase50 = leer_ganancia_lazo("Ganancia de Lazo(R50).txt")

fase5 = np.unwrap(fase5, period=360)
fase10 = np.unwrap(fase10, period=360)
fase50 = np.unwrap(fase50, period=360)

# Crear subplots
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# --- Magnitud ---
ax1.set_xscale('log')
ax1.plot(freq, modulo5, color = 'black', label = f'$R_L = 5$')
ax1.plot(freq, modulo10, color = 'blue', label = f'$R_L = 10$')
ax1.plot(freq, modulo50, color = 'green', label = f'$R_L = 50$')

ax1.set_xlabel("Frecuencia [Hz]")
ax1.set_xlim(np.min(freq), np.max(freq))

ax1.set_ylabel("Magnitud [dB]")
ax1.set_title("Diagrama de Bode")
ax1.grid(True, which="both")
ax1.legend()

# --- Fase ---
ax2.set_xscale('log')
ax2.plot(freq, fase5, color = 'black', label = f'$R_L = 5$')
ax2.plot(freq, fase10, color = 'blue', label = f'$R_L = 10$')
ax2.plot(freq, fase50, color = 'green', label = f'$R_L = 50$')

ax2.set_xlabel("Frecuencia [Hz]")
ax2.set_xlim(np.min(freq), np.max(freq))

ax2.set_ylabel("Fase [°]")
ax2.grid(True, which="both")
ax2.legend()

plt.tight_layout()
plt.savefig("Bode.png")

### Lazo de corriente 


freq, modulo, fase = leer_ganancia_lazo("Ganancia de Lazo de corriente.txt")

plt.figure()
plt.xscale('log')
plt.plot(freq, modulo, color = 'black')

plt.xlabel("Frecuencia [Hz]")
plt.xlim(np.min(freq), np.max(freq))

plt.ylabel("Magnitud [dB]")
plt.title("Bode del lazo de corriente")
plt.grid(True, which="both")

plt.tight_layout()
plt.savefig("Bode corriente.png")


plt.show()