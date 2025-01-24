#!/usr/bin/env python
# coding=UTF8
# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure, io

"""

  Mejora de contraste de las por medio
  de ecualización adaptativa del histograma

"""
# Tamaño de las imágenes.
figsize = (20, 10)

# Esta variable apunta a la versión de las imágenes que vamos a utilizar, para
# más comodidad.
data_dir = ["..", "data", "000_in", "clipped-mask"]

# Esta lo hace al directorio de salida de resultados base y a uno específico
# para este script y crea éste último si no existe.
out_base_dir = ["..", "data", "900_out"]
out_dir = [*out_base_dir, "030"]

if not os.path.exists(os.path.join(*out_dir)):
    os.makedirs(os.path.join(*out_dir))

# Carga de imagen con Scikit-Image (skimage), que convertirá en un array Numpy
# para poder operar con sus datos.
ublue = io.imread(os.path.join(*data_dir, "b_1-ultrablue.tif"))

"""

  Mejora del contraste en la imagen por medio de una equalización del histograma
  adaptativa.

"""
# Transformamos los valores -999.0 en NaN.
ublue[ublue == -999.0] = np.nan

# Equalizamos
ublue_eq = exposure.equalize_adapthist(ublue, clip_limit=0.025)

# Componemos las imágenes una al lado de la otra.
fig, (fig0, fig1) = plt.subplots(1, 2, figsize=(30, 10))

# Configuramos el espacio entre las imágenes, la composición un tanto relajada y
# el título.
fig.tight_layout(pad=5.0)
fig.suptitle("Comparativa de imágenes")

# Primera imagen.
img0 = fig0.imshow(ublue, cmap="gray")
fig0.set_title("Original")
fig.colorbar(img0, ax=fig0, cmap="gray", orientation="horizontal", fraction=0.05)

# Segunda imagen.
img1 = fig1.imshow(ublue_eq, cmap="gray")
fig1.set_title("Ecualizada")
fig.colorbar(img1, ax=fig1, cmap="gray", orientation="horizontal", fraction=0.05)

# Guardamos la imagen.
fig.savefig(os.path.join(*out_dir, "ultrablue_eq_comparativa.png"), dpi=300)

# Comparativa de histogramas.
fig, (fig0, fig1) = plt.subplots(2, figsize=(15, 15))

fig.tight_layout(pad=5.0)
fig.suptitle("Comparativa de histogramas")
fig.subplots_adjust(top=0.95)

# Histograma original.
fig0.hist(ublue.ravel(), bins=500, histtype="step")
fig0.set_title("Histograma original")

# Histograma ecualizado.
fig1.hist(ublue_eq.ravel(), bins=500, histtype="step")
fig1.set_title("Histograma ecualizado")

# Guardamos la imagen.
fig.savefig(os.path.join(*out_dir, "histogramas.png"), dpi=300)

# Visualización final.
fig.show()
