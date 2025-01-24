#!/usr/bin/env python
# coding=UTF8
# -*- coding: utf-8 -*-

import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from helpers.raster import load_geo_profile, save_geotiff_from_array

"""

  Este script calcula el Normalized Difference Vegetation Index (NDVI), un
  índice normalizado (de -1 a 1) que explota el contraste existente en la
  respuesta espectral de la vegetación entre el infrarrojo cercano (NIR) y el
  rojo.

  La definición del índice es la siguiente:

  NDVI = (NIR - RED) / (NIR + RED)

  Donde:

    NIR: banda del infrarrojo cercano (Near Infrared), en nuestro caso, la que
         está en la dimensión 4 del array multiespectral.

    RED: banda del rojo, en nuestro caso, la que está en la dimensión 3 del
         array multiespectral.

"""
# Tamaño de las imágenes.
figsize = (20, 10)

# Esta variable apunta a la versión de las imágenes que vamos a utilizar, para
# más comodidad.
data_dir = ["..", "data", "000_in", "clipped-mask"]

# Esta lo hace al directorio de salida de resultados base y a uno específico
# para este script y crea éste último si no existe.
out_base_dir = ["..", "data", "900_out"]
out_dir = [*out_base_dir, "060"]

if not os.path.exists(os.path.join(*out_dir)):
    os.makedirs(os.path.join(*out_dir))

# Leemos el perfil GeoTIFF de una de las imágenes originales para utilizarlo en
# las imágenes nuevas.
profile = load_geo_profile(os.path.join(*data_dir, "b_1-ultrablue.tif"))

# Carga del array multiespectral.
ms = np.load(os.path.join(*out_base_dir, "multiespectral.npy"))

# Calculamos el NDVI, aplicando la fórmula normalizada entre las bandas
# apropiadas. Recordemos que la banda NIR es la índice 4 y la RED la 3.
ndvi = (ms[:, :, 4] - ms[:, :, 3]) / (ms[:, :, 4] + ms[:, :, 3])

# Mostramos el NDVI total, positivos y negativos.
plt.figure(1, figsize=figsize)
plt.imshow(ndvi, cmap="bwr", vmin=-1, vmax=1)
plt.colorbar()
plt.suptitle("NDVI total")
plt.savefig(os.path.join(*out_dir, "ndvi.png"), dpi=300)
plt.close()

save_geotiff_from_array(os.path.join(*out_dir, "ndvi.tif"), ndvi, profile)

# Ahora el NDVI por encima de 0, que es el que corresponde a las coberturas no
# acuáticas.
ndvi_pos = np.copy(ndvi)
ndvi_pos[ndvi_pos < 0.0] = np.nan

plt.figure(2, figsize=figsize)
plt.imshow(ndvi_pos, cmap="Greens", vmin=0, vmax=1)
plt.colorbar()
plt.suptitle("NDVI positivo")
plt.savefig(os.path.join(*out_dir, "ndvi_pos.png"), dpi=300)
plt.close()

save_geotiff_from_array(os.path.join(*out_dir, "ndvi_pos.tif"), ndvi_pos, profile)

# --------------------------------------
#
# Ahora vamos a hacer una reclasificación temática del NDVI en algunas clases de
# interés. El NDVI positivo se corresponde con las coberturas no acuáticas, y se
# podrían definir algunas clases que se corresponderían a las siguientes:
#
#    - NDVI < 0.0: agua
#
#    - NDVI < 0.2: suelo desnudo o urbano
#
#    - NDVI < 0.5: vegetación rala
#
#    - NDVI < 0.7: vegetación vigorosa
#
#    - NDVI < 1.0: vegetación muy vigorosa
#
# --------------------------------------

# Utilizaremos para hacer la reclasificación una UFUNC de numpy, que nos
# permitirá aplicar una función a todos los elementos de un array
# (https://numpy.org/doc/stable/reference/ufuncs.html).

# Definimos las clases.
clases = [
    {"nombre": "Agua", "valor_max": 0},
    {"nombre": "Urbano / suelo desnudo", "valor_max": 0.2},
    {"nombre": "Vegetación rala", "valor_max": 0.5},
    {"nombre": "Vegetación vigorosa", "valor_max": 0.7},
    {"nombre": "Vegetación muy vigorosa", "valor_max": 1.0},
]


# Definimos la función que vamos a utilizar para la reclasificación.
def reclasificacion_ndvi_e(ndvi):
    # Chequear que no es nan.
    if ~np.isnan(ndvi):
        for i, v in enumerate(clases):
            if ndvi < v["valor_max"]:
                return i

    else:
        return np.nan


# Aplicamos la función a todos los elementos del array.
reclasificacion_ndvi = np.vectorize(reclasificacion_ndvi_e)

# Clasificamos.
clasificacion = reclasificacion_ndvi(ndvi)

# Lo mostramos.
plt.figure(3, figsize=figsize)
cmap = plt.get_cmap("Paired", len(clases))
plt.imshow(clasificacion, cmap=cmap)
plt.legend(
    [mpatches.Patch(color=cmap(b)) for b in range(len(clases))],
    [x["nombre"] for x in clases],
)
plt.suptitle("NDVI reclasificado")
plt.savefig(os.path.join(*out_dir, "ndvi_clasificado.png"), dpi=300)
plt.close()

save_geotiff_from_array(
    os.path.join(*out_dir, "ndvi_reclasificado.tif"), clasificacion, profile
)

# Hacemos un recuento de superficie en km2, sabiendo que el pixel mide 30x30
# metros.
unique, counts = np.unique(clasificacion, return_counts=True)
superficie = [round(i * 30 * 30 / 1000000.0) for i in counts]

print("Recuento de superficies", unique, superficie)

# Hacemos visualizaciones individuales por clases.
for i, v in enumerate(clases):
    clasificacion_i = np.copy(clasificacion)
    clasificacion_i[clasificacion_i != i] = np.nan

    plt.figure(4 + i, figsize=figsize)
    plt.imshow(clasificacion_i, cmap=cmap)
    plt.suptitle(f"Clase NDVI: {v["nombre"]} (superficie: {superficie[i]} km2)")
    plt.savefig(os.path.join(*out_dir, f"ndvi_clasificado_{i}.png"), dpi=300)
    plt.close()

    save_geotiff_from_array(
        os.path.join(*out_dir, f"ndvi_clasificado_{i}.tif"), clasificacion_i, profile
    )

# Mostrarlo todo.
plt.show()
plt.close()
