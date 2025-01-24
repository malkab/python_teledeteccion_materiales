#!/usr/bin/env python
# coding=UTF8
# -*- coding: utf-8 -*-

import os

import numpy as np
from skimage import io

"""

    Este script guarda un array multiespectral Numpy para usarlo en scripts
    posteriores con más comodidad.

    Compone un único array Numpy con todas las bandas de la imagen, lo que se
    suele llamar un cubo multiespectral de dos dimensiones espaciales (ancho y
    alto) y para cada posición x/y un array (un vector) con la información de la
    radiometría de las bandas.

"""
# Esta variable apunta a la versión de las imágenes que vamos a utilizar, para
# más comodidad.
data_dir = ["..", "data", "000_in", "clipped-mask"]

# Esta lo hace al directorio de salida de resultados base y a uno específico
# para este script y crea éste último si no existe.
out_base_dir = ["..", "data", "900_out"]

# Creamos un array con el nombre de las capas a incluir en el array
# multiespectral.
bandas = [
    "b_1-ultrablue.tif",  # 0
    "b_2-blue.tif",  # 1
    "b_3-green.tif",  # 2
    "b_4-red.tif",  # 3
    "b_5-nir.tif",  # 4
    "b_6-swir1.tif",  # 5
    "b_7-swir2.tif",  # 6
]

# Creamos array para guardar cada banda individualmente para posteriormente
# acoplarlas a un único array Numpy.
np_bandas = []

# Carga de imagen con Scikit-Image (skimage), que convertirá en un array Numpy
# para poder operar con sus datos.
for b in bandas:
    print(f"Procesando banda {b}")

    # Carga de la banda.
    band = io.imread(os.path.join(*data_dir, b))

    # Transformamos los valores -999.0 en NaN.
    band[band == -999.0] = np.nan

    # Añadimos la banda al array de bandas.
    np_bandas.append(band)

# Veamos la forma que tiene una banda individual.
print()
print(f"La banda UltraBlue tiene la forma: {str(np_bandas[0].shape)}")

# Ahora acoplamos las bandas individuales contenidas en np_bandas, de forma que
# las bandas queden acopladas sobre el eje 2, ya que para guardar imágenes
# Scikit-Image requiere esta estructura de datos:
#
#   eje 0: coordenada de pixel X
#   eje 1: coordenada de pixel Y
#   eje 2: información de bandas o canales
mspect = np.stack(np_bandas, axis=2)

# Chequeamos su forma.
print(f"El array multiespectral tiene la forma: {str(mspect.shape)}")

# Ahora, la información multiespectral está organizada en una pila de bandas,
# por lo que cada pixel de la imagen está representado por un vector
# multiespectral con las reflectancias en cada banda del espectro recogido por
# el sensor. Estos vectores son los que nos permitirán aplicar técnicas de ML.
print(f"La signatura espectral del pixel (500, 500) es: {str(mspect[500, 500, :])}")

# Por último, guardamos el array multiespectral en un formato binario propio de
# Numpy para su uso posterior.
np.save(os.path.join(*out_base_dir, "multiespectral"), mspect)
