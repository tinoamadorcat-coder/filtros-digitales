
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from scipy.signal import (
    butter, sosfiltfilt, sosfreqz,
    firwin, filtfilt, freqz
)

# ==================================================
# 1. CONFIGURACION Y CARPETA DE RESULTADOS
# ==================================================

fs = 500
duracion = 2

t = np.arange(0, duracion, 1/fs)

# Crear carpeta para guardar las graficas
CARPETA = Path(__file__).resolve().parent
CARPETA_RESULTADOS = CARPETA / "resultados"
CARPETA_RESULTADOS.mkdir(exist_ok=True)

print("Iniciando procesamiento de señales...")
print("Las graficas se guardaran en:", CARPETA_RESULTADOS)


# ==================================================
# 2. GENERAR SEÑAL ORIGINAL Y AGREGAR RUIDO
# ==================================================

senal_original = (
    np.sin(2 * np.pi * 5 * t) +
    0.7 * np.sin(2 * np.pi * 25 * t) +
    0.5 * np.sin(2 * np.pi * 80 * t)
)

np.random.seed(10)

ruido = 0.5 * np.random.randn(len(t))
senal_ruidosa = senal_original + ruido


# ==================================================
# 3. DISEÑO DE FILTROS IIR BUTTERWORTH
# ==================================================

# Pasa bajos: conserva frecuencias menores a 10 Hz
iir_bajos = butter(
    4, 10, btype="lowpass",
    fs=fs, output="sos"
)

# Pasa altos: conserva frecuencias mayores a 40 Hz
iir_altos = butter(
    4, 40, btype="highpass",
    fs=fs, output="sos"
)

# Pasa bandas: conserva frecuencias entre 20 y 30 Hz
iir_bandas = butter(
    4, [20, 30], btype="bandpass",
    fs=fs, output="sos"
)


# ==================================================
# 4. DISEÑO DE FILTROS FIR CON VENTANA HAMMING
# ==================================================

num_taps = 101

fir_bajos = firwin(
    num_taps, 10, fs=fs,
    pass_zero="lowpass", window="hamming"
)

fir_altos = firwin(
    num_taps, 40, fs=fs,
    pass_zero="highpass", window="hamming"
)

fir_bandas = firwin(
    num_taps, [20, 30], fs=fs,
    pass_zero="bandpass", window="hamming"
)


# ==================================================
# 5. APLICAR LOS SEIS FILTROS
# ==================================================

resultados = {
    "Pasa bajos IIR": sosfiltfilt(iir_bajos, senal_ruidosa),
    "Pasa altos IIR": sosfiltfilt(iir_altos, senal_ruidosa),
    "Pasa bandas IIR": sosfiltfilt(iir_bandas, senal_ruidosa),

    "Pasa bajos FIR": filtfilt(fir_bajos, [1.0], senal_ruidosa),
    "Pasa altos FIR": filtfilt(fir_altos, [1.0], senal_ruidosa),
    "Pasa bandas FIR": filtfilt(fir_bandas, [1.0], senal_ruidosa)
}


# ==================================================
# 6. GRAFICAR SEÑAL ORIGINAL Y SEÑAL CON RUIDO
# ==================================================

fig1, ejes1 = plt.subplots(2, 1, figsize=(12, 7))

ejes1[0].plot(t, senal_original)
ejes1[0].set_title("Señal original compuesta")
ejes1[0].set_xlabel("Tiempo (segundos)")
ejes1[0].set_ylabel("Amplitud")
ejes1[0].grid()

ejes1[1].plot(t, senal_ruidosa)
ejes1[1].set_title("Señal original con ruido blanco")
ejes1[1].set_xlabel("Tiempo (segundos)")
ejes1[1].set_ylabel("Amplitud")
ejes1[1].grid()

fig1.tight_layout()

fig1.savefig(
    CARPETA_RESULTADOS / "01_senales_originales.png",
    dpi=300, bbox_inches="tight"
)


# ==================================================
# 7. GRAFICAR RESULTADOS DE LOS SEIS FILTROS
# ==================================================

fig2, ejes2 = plt.subplots(3, 2, figsize=(14, 10))

for ax, (nombre, senal_filtrada) in zip(
    ejes2.flat, resultados.items()
):
    ax.plot(
        t, senal_ruidosa,
        alpha=0.4, label="Con ruido"
    )

    ax.plot(
        t, senal_filtrada,
        label="Filtrada"
    )

    ax.set_title(nombre)
    ax.set_xlabel("Tiempo (segundos)")
    ax.set_ylabel("Amplitud")
    ax.grid()
    ax.legend()

fig2.tight_layout()

fig2.savefig(
    CARPETA_RESULTADOS / "02_comparacion_filtros.png",
    dpi=300, bbox_inches="tight"
)


# ==================================================
# 8. RESPUESTA EN FRECUENCIA DE LOS FILTROS
# ==================================================

filtros_iir = [
    ("Pasa bajos IIR", iir_bajos),
    ("Pasa altos IIR", iir_altos),
    ("Pasa bandas IIR", iir_bandas)
]

filtros_fir = [
    ("Pasa bajos FIR", fir_bajos),
    ("Pasa altos FIR", fir_altos),
    ("Pasa bandas FIR", fir_bandas)
]

fig3, ejes3 = plt.subplots(3, 2, figsize=(14, 10))

# Respuesta en frecuencia de los filtros IIR
for ax, (nombre, filtro) in zip(ejes3[:, 0], filtros_iir):

    frecuencias, respuesta = sosfreqz(
        filtro, worN=2048, fs=fs
    )

    magnitud_db = 20 * np.log10(
        np.maximum(np.abs(respuesta), 1e-8)
    )

    ax.plot(frecuencias, magnitud_db)
    ax.set_title("Respuesta en frecuencia: " + nombre)
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Magnitud (dB)")
    ax.set_ylim(-100, 5)
    ax.grid()

# Respuesta en frecuencia de los filtros FIR
for ax, (nombre, filtro) in zip(ejes3[:, 1], filtros_fir):

    frecuencias, respuesta = freqz(
        filtro, worN=2048, fs=fs
    )

    magnitud_db = 20 * np.log10(
        np.maximum(np.abs(respuesta), 1e-8)
    )

    ax.plot(frecuencias, magnitud_db)
    ax.set_title("Respuesta en frecuencia: " + nombre)
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Magnitud (dB)")
    ax.set_ylim(-100, 5)
    ax.grid()

fig3.tight_layout()

fig3.savefig(
    CARPETA_RESULTADOS / "03_respuesta_frecuencia.png",
    dpi=300, bbox_inches="tight"
)


# ==================================================
# 9. MOSTRAR RESULTADOS NUMERICOS
# ==================================================

print("\n========================================")
print("RESULTADOS DEL PROCESAMIENTO DIGITAL")
print("========================================")

for nombre, senal_filtrada in resultados.items():

    amplitud_rms = np.sqrt(
        np.mean(senal_filtrada ** 2)
    )

    print("\n" + nombre)
    print("Amplitud RMS:", round(amplitud_rms, 4))

print("\n========================================")
print("PROCESAMIENTO TERMINADO CORRECTAMENTE")
print("========================================")

print("\nSe guardaron las siguientes graficas:")
print("1. 01_senales_originales.png")
print("2. 02_comparacion_filtros.png")
print("3. 03_respuesta_frecuencia.png")

print("\nUbicacion:", CARPETA_RESULTADOS)

# Mostrar las tres figuras
plt.show()

