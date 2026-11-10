
# Implementación y evaluación de filtros digitales

## Descripción
Este proyecto implementa y evalúa filtros digitales utilizando Python, NumPy, SciPy y Matplotlib.

Se genera una señal compuesta por tres frecuencias (5 Hz, 25 Hz y 80 Hz), a la cual se agrega ruido blanco para analizar el comportamiento de diferentes filtros digitales.

## Objetivo
Diseñar y comparar filtros pasa bajas, pasa altas y pasa banda mediante técnicas FIR e IIR, observando sus resultados en los dominios del tiempo y de la frecuencia.

## Filtros implementados

- IIR Butterworth de orden 4.
- FIR con ventana Hamming de 101 coeficientes.
- Filtro pasa bajas de 10 Hz.
- Filtro pasa altas de 40 Hz.
- Filtro pasa banda de 20 a 30 Hz.

## Herramientas utilizadas

- Python 3
- NumPy
- SciPy
- Matplotlib

## Instalación de librerías

Ejecutar en la terminal:

```bash
pip install numpy scipy matplotlib
```

## Ejecución

Ejecutar el programa con:

```bash
python filtros_digitales.py
```

## Resultados

El programa genera tres gráficas:

1. Señales originales y señal con ruido blanco.
2. Comparación de los seis filtros implementados.
3. Respuesta en frecuencia de los filtros FIR e IIR.

Las imágenes se guardan automáticamente en la carpeta `resultados`.

## Autor
Florentino Amador Martinez

## Actividad
Implementación y evaluación de filtros digitales.
