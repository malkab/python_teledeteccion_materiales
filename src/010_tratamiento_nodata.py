#!/usr/bin/env python
# coding=UTF8
# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import numpy as np
from skimage import io

"""

  Tratamiento de no-data en las bandas.

  La geometría de las imágenes de satélite no siempre es perfectamente
  cuadrangular. Esto se debe a la senda de vuelo de los satélites, que
  no siempre se alinea con los ejes de coordenadas de la Tierra. A medida
  que el punto fotografiado se aleja del nadir del satélite, esto es, del
  punto inmediatamente debajo del satélite, la imagen va acumulando
  deformaciones, por lo que llega un momento que los datos de los píxeles
  muy alejados del nadir ya no se consideran fiables. Por ello, los píxeles
  fuera de la zona de cobertura de la imagen se marcan con un valor especial,
  un valor nulo, que indica que no se han codificado datos en esas posiciones.
  Vamos a tratar estos valores NODATA para obtener una imagen limpia que
  tenga sólo datos radiométricos válidos.

"""
# Tamaño de las imágenes.
figsize = (20, 10)

# Esta variable apunta a la versión de las imágenes que vamos a utilizar, para
# más comodidad.
data_dir = ["..", "data", "000_in", "clipped-mask"]

# Esta lo hace al directorio de salida de resultados base y a uno específico
# para este script y crea éste último si no existe.
out_base_dir = ["..", "data", "900_out"]
out_dir = [*out_base_dir, "010"]

if not os.path.exists(os.path.join(*out_dir)):
    os.makedirs(os.path.join(*out_dir))

# Carga de imagen con Scikit-Image (skimage), que la convertirá en un array
# Numpy para poder operar con sus datos.
in_file = io.imread(os.path.join(*data_dir, "b_1-ultrablue.tif"))

# Este es el primer píxel de la imagen, en la esquina superior izquierda.
print(f"Píxel esquina superior izquierda: {in_file[0, 0]}")

# Visualizamos la imagen recién cargada con Matplotlib.
plt.figure(1, figsize=figsize)
plt.suptitle("Valores nulos no tratados")
plt.imshow(in_file, cmap="gray")
plt.savefig(os.path.join(*out_dir, "ultrablue_nulos_no_tratados.png"), dpi=300)
plt.close()

"""

  Exploramos y alteramos los valores nulos de la imagen.

"""
# Tamaño de imagen.
print(f"Tamaño de la imagen: {str(in_file.shape)}")

# Valor mínimo y máximo.
print(f"Rango de valores: {np.min(in_file)}, {np.max(in_file)}")

# Transformamos los valores -999.0 en el NaN de Numpy.
in_file[in_file == -999.0] = np.nan

# Valores máximos y mínimos sin propagación de NaN.
print(
    f"Rango de valores sin contar nulos (NaN): {np.nanmin(in_file)}, {np.nanmax(in_file)}"
)

# Nueva visualización, sin contar los nulos.
plt.figure(2, figsize=figsize)
plt.imshow(in_file, cmap="gray")
plt.suptitle("Valores nulos tratados")
plt.colorbar()
plt.savefig(os.path.join(*out_dir, "ultrablue_nulos_tratados.png"), dpi=300)
plt.close()

# Histograma, sin contar los nulos.
plt.figure(3, figsize=figsize)
plt.hist(in_file.ravel(), bins=500, histtype="step", range=(0.0, 1.0))
plt.suptitle("Histograma de reflectividad sin nulos")
plt.savefig(os.path.join(*out_dir, "ultrablue_histogram_no_nulos.png"), dpi=300)
plt.show()
plt.close()
