#!/usr/bin/env python
# coding=UTF8
# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import numpy as np
from skimage import io

"""

  Carga de imágenes directamente a un array de dos dimensiones Numpy.

  Scikit-Image es una librería basada en Scikit-Learn orientada a
  CV (Computer Vision) y manipulación y análisis de imágenes en
  general. En el contexto de esta práctica la utilizaremos para
  cargar los datos de las bandas multiespectrales y manipular ciertos
  aspectos de la imagen.

"""
# Establecemos el tamaño de las figuras de Matplotlib
figsize = (20, 10)

# Esta variable apunta a la versión de las imágenes que vamos a utilizar, para
# más comodidad.
data_dir = ["..", "data", "000_in", "clipped-mask"]

# Esta lo hace al directorio de salida de resultados base y a uno específico
# para este script y crea éste último si no existe.
out_base_dir = ["..", "data", "900_out"]
out_dir = [*out_base_dir, "000"]

if not os.path.exists(os.path.join(*out_dir)):
    os.makedirs(os.path.join(*out_dir))

# Carga de imagen con Scikit-Image (skimage), que la convertirá en un array
# Numpy para poder operar con sus datos.
in_file = io.imread(os.path.join(*data_dir, "b_1-ultrablue.tif"))

# Esta es la estructura del array.
print(f"Número de dimensiones del array imagen: {in_file.ndim}")
print(f"Forma del array imagen: {str(in_file.shape)}")
print(
    f"El pixel (500, 500) tiene una reflectividad en el UltraBlue de: {in_file[500][500]}"
)
print(f"La reflectividad media de la banda es de: {np.nanmean(in_file)}")
print(f"Con una distribución típica de: {np.nanstd(in_file)}")
print(f"Rangos de reflectividad: {np.nanmin(in_file)} / {np.nanmax(in_file)}")

# Visualizamos la imagen recién cargada con Matplotlib.
plt.figure(1, figsize=figsize)
plt.imshow(in_file, cmap="hot")
plt.savefig(os.path.join(*out_dir, "ultrablue.png"), dpi=300)
plt.show()
plt.close()

# Construimos el histograma de frecuencias de valores de la imagen.
plt.figure(2, figsize=figsize)
plt.hist(in_file.ravel(), bins=500, histtype="step", label="UltraBlue")
plt.legend()
plt.suptitle("Histograma de reflectividad")
plt.savefig(os.path.join(*out_dir, "ultrablue_histogram.png"), dpi=300)
plt.show()
plt.close()
