#!/usr/bin/env python
# coding=UTF8
# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure, io

"""

  Ecualización adaptativa con scikit-image. La ecualización es un proceso
  mediante el cual se ajusta la distribución de los valores de intensidad de la
  imagen para mejorar su contraste y su visualización.

  ¡OJO! El resultado de la ecualización modifica los valores originales
  radiométricos de la imagen, por lo que quedan invalidados para cualquier otro
  proceso analítico posterior. La ecualización es un proceso de visualización
  destinado a hacer más agradable la imagen para su exploración visual, pero sus
  resultados desvirtuan la información científica real.

  La ecualización adaptativa es una variante de la ecualización que se aplica a
  regiones pequeñas de la imagen, en lugar de a toda la imagen. Esto permite que
  la imagen quede realzada por zonas, haciendo más luminosas las partes oscuras
  a la par que las partes contrastadas quedan inalteradas.

"""
# Tamaño de las imágenes.
figsize = (20, 10)

# Esta variable apunta a la versión de las imágenes que vamos a utilizar, para
# más comodidad.
data_dir = ["..", "data", "000_in"]

# Esta lo hace al directorio de salida de resultados base y a uno específico
# para este script y crea éste último si no existe.
out_base_dir = ["..", "data", "900_out"]
out_dir = [*out_base_dir, "020"]

if not os.path.exists(os.path.join(*out_dir)):
    os.makedirs(os.path.join(*out_dir))

# Nombre de la imagen a contrastar.
file_name = "mountains.jpg"

# Carga de imagen con Scikit-Image (skimage), que convertirá en un array Numpy
# para poder operar con sus datos.
in_file = io.imread(os.path.join(*data_dir, "imagenes", file_name))

# Mostramos la imagen original y sus tres canales cromáticos.
plt.figure(1, figsize=figsize)
plt.subplot(2, 1, 1)
plt.imshow(in_file)

plt.subplot(2, 1, 2)
rgb = np.hstack([in_file[:, :, 0], in_file[:, :, 1], in_file[:, :, 2]])
plt.imshow(rgb, cmap="gray")
plt.suptitle("Original / RGBA")
plt.savefig(os.path.join(*out_dir, "ecualizacion-imagen_original-rgba.png"), dpi=300)
plt.close()

# Construimos el histograma de las tres bandas.
plt.figure(2, figsize=figsize)
plt.hist(in_file[:, :, 0].ravel() / 256, bins=500, histtype="step", label="Rojo")
plt.hist(in_file[:, :, 1].ravel() / 256, bins=500, histtype="step", label="Verde")
plt.hist(in_file[:, :, 2].ravel() / 256, bins=500, histtype="step", label="Azul")
plt.legend()
plt.suptitle("Histograma original")
plt.savefig(os.path.join(*out_dir, "histograma_bandas_original.png"), dpi=300)
plt.close()

# Ecualización adaptativa muy leve, con su histograma.
eq_0 = exposure.equalize_adapthist(in_file, clip_limit=0.005)

plt.figure(3, figsize=figsize)
plt.hist(eq_0[:, :, 0].ravel(), bins=500, histtype="step", label="Rojo")
plt.hist(eq_0[:, :, 1].ravel(), bins=500, histtype="step", label="Verde")
plt.hist(eq_0[:, :, 2].ravel(), bins=500, histtype="step", label="Azul")
plt.legend()
plt.suptitle("Histograma EQ 0")
plt.savefig(os.path.join(*out_dir, "histograma_eq_0.png"), dpi=300)
plt.close()

# Ecualización adaptativa un poco más forzada, con su histograma.
eq_1 = exposure.equalize_adapthist(in_file, clip_limit=0.01)
plt.figure(4, figsize=figsize)
plt.hist(eq_1[:, :, 0].ravel(), bins=500, histtype="step", label="Rojo")
plt.hist(eq_1[:, :, 1].ravel(), bins=500, histtype="step", label="Verde")
plt.hist(eq_1[:, :, 2].ravel(), bins=500, histtype="step", label="Azul")
plt.legend()
plt.suptitle("Histograma EQ 1")
plt.savefig(os.path.join(*out_dir, "histograma_eq_1.png"), dpi=300)
plt.close()

# Ecualización adaptativa extremadamente forzada, con su histograma.
eq_2 = exposure.equalize_adapthist(in_file, clip_limit=0.7)
plt.figure(5, figsize=figsize)
plt.hist(eq_2[:, :, 0].ravel(), bins=500, histtype="step", label="Rojo")
plt.hist(eq_2[:, :, 1].ravel(), bins=500, histtype="step", label="Verde")
plt.hist(eq_2[:, :, 2].ravel(), bins=500, histtype="step", label="Azul")
plt.legend()
plt.suptitle("Histograma EQ 2")
plt.savefig(os.path.join(*out_dir, "histograma_eq_2.png"), dpi=300)
plt.close()

plt.figure(6, figsize=figsize)
eq = np.hstack([in_file / 256, eq_0, eq_1, eq_2])
plt.imshow(eq)
plt.suptitle("Ecualización")
plt.savefig(os.path.join(*out_dir, "comparativa_eq.png"), dpi=300)
plt.show()
plt.close()
