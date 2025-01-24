#!/usr/bin/env python
# coding=UTF8
# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import numpy as np
from helpers.raster import load_geo_profile, save_geotiff_from_array
from skimage import exposure, io

"""

  Este script crea una composición diversas composiciones de color, tanto
  verdadero como falso.

"""
# Composiciones de falso color.
#
# Lo interesante es generar imágenes en color con longitudes de onda ("colores")
# a las que el ojo humano no es sensible.
#
# Recordemos la relación bandas - índices en el array multiespectral en su
# tercer eje:
#
# Banda                      Índice de la tercera dimensión Numpy
#
# Band 1 - Ultra Blue        0
#
# Band 2 - Blue              1
#
# Band 3 - Green             2
#
# Band 4 - Red               3
#
# Band 5 - NIR               4
#
# Band 6 - SWIR 1            5
#
# Band 7 - SWIR 2            6
#
# Vamos a generar primero la composición llamada "Color verdadero". Recibe este
# nombre porque se le asigna a los canales de color del ordenador (ROJO, VERDE,
# AZUL) las longitudes de onda correspondientes a esos colores, tal y como los
# interpreta nuestro ojo. Por lo tanto, esta composición de color estará cercana
# a lo que vería el ojo humano:
#
# Canal cromático   Banda
#
# rojo              Red
#
# verde             Green
#
# azul              Blue
#
# Tras ello generaremos dos composiciones de color destinadas a destacar la la
# vegetación. Son:
#
# Canal cromático   Banda
#
# rojo              NIR
#
# verde             Red
#
# azul              Green
#
# y
#
# Canal cromático   Banda
#
# rojo              SWIR 1
#
# verde             Red
#
# azul              Blue

# Tamaño de las imágenes.
figsize = (30, 5)

# Esta variable apunta a la versión de las imágenes que vamos a utilizar, para
# más comodidad.
data_dir = ["..", "data", "000_in", "clipped-mask"]

# Esta lo hace al directorio de salida de resultados base y a uno específico
# para este script y crea éste último si no existe.
out_base_dir = ["..", "data", "900_out"]
out_dir = [*out_base_dir, "050"]

if not os.path.exists(os.path.join(*out_dir)):
    os.makedirs(os.path.join(*out_dir))

# Leemos el perfil GeoTIFF de una de las imágenes originales para utilizarlo en
# las imágenes nuevas.
profile = load_geo_profile(os.path.join(*data_dir, "b_1-ultrablue.tif"))

# Carga del array multiespectral.
ms = np.load(os.path.join(*out_base_dir, "multiespectral.npy"))

# Definimos un array de diccionarios para realizar varias composiciones de color
# de golpe.
composiciones_color = [
    {
        "nombre": "Color verdadero",
        "nombre_fichero": "color_verdadero",
        "bandas": (3, 2, 1),
    },
    {
        "nombre": "Realce vegetación 1",
        "nombre_fichero": "realce_vegetacion_1",
        "bandas": (4, 3, 2),
    },
    {
        "nombre": "Realce vegetación 2",
        "nombre_fichero": "realce_vegetacion_2",
        "bandas": (5, 4, 1),
    },
]

# Preparamos una imagen para mostrar las composiciones de color.
fig, subplots = plt.subplots(1, 3, figsize=figsize)
fig.suptitle("Composiciones de color", fontsize=20)

# Un contador para controlar los subplots a la hora de ciclar las composiciones
# definidas anteriormente.
n = 0

# Creamos las composiciones de color.
for c in composiciones_color:
    print(f"Generando composición: {c["nombre"]}")

    # Hacemos slicing sobre el multiespectral con las bandas seleccionadas.
    composicion = ms[:, :, c["bandas"]]

    # Vemos la forma del array.
    print(f"Forma del array de color seleccionado: {str(composicion.shape)}")

    # Como la imagen es un poco oscura, vamos a hacerle algunos ajustes.
    composicion_eq = exposure.adjust_gamma(
        exposure.equalize_adapthist(composicion), gamma=0.75
    )

    subplots[n].set_title(c["nombre"])
    subplots[n].imshow(composicion_eq)

    # Guardamos la imagen a PNG, con un cambio de tipo de dato a entero de 8
    # bits sin signo.
    io.imsave(
        os.path.join(*out_dir, f"{c['nombre_fichero']}.png"),
        (composicion * 256).astype(np.uint8),
    )
    io.imsave(
        os.path.join(*out_dir, f"{c['nombre_fichero']}_eq.png"),
        (composicion_eq * 256).astype(np.uint8),
    )

    # Guardamos como GeoTIFF la clasificación.
    save_geotiff_from_array(
        os.path.join(*out_dir, f"{c['nombre_fichero']}.tif"), composicion, profile
    )

    n += 1

plt.show()
fig.savefig(os.path.join(*out_dir, "composiciones_color.png"), dpi=300)
fig.savefig(os.path.join(*out_dir, "composiciones_color.pdf"), dpi=300)
plt.close()
