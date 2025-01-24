#!/usr/bin/env python
# coding=UTF8
# -*- coding: utf-8 -*-

import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from helpers.raster import load_geo_profile, save_geotiff_from_array
from matplotlib.lines import Line2D
from sklearn.ensemble import RandomForestClassifier
from training.random_forest_training import entrenamiento, sample_ms

"""

  Este script hace sucesivas clasificaciones con
  Random forest a medida que se le van añadiendo
  clases al set de entrenamiento.

"""
# Tamaño de las imágenes
figsize = (20, 10)

# Esta variable apunta a la versión de las imágenes que vamos a utilizar, para
# más comodidad.
data_dir = ["..", "data", "000_in", "clipped-mask"]

# Esta lo hace al directorio de salida de resultados base y a uno específico
# para este script y crea éste último si no existe.
out_base_dir = ["..", "data", "900_out"]
out_dir = [*out_base_dir, "090"]

if not os.path.exists(os.path.join(*out_dir)):
    os.makedirs(os.path.join(*out_dir))

# Leemos el perfil GeoTIFF de una de las imágenes originales para utilizarlo en
# las imágenes nuevas.
profile = load_geo_profile(os.path.join(*data_dir, "b_1-ultrablue.tif"))

# Carga del array multiespectral.
ms = np.load(os.path.join(*out_base_dir, "multiespectral.npy"))

# Creamos dos listas vacías para la función Random Forest, una para guardar los
# vectores de las muestras de entrenamiento y otra para guardar la clase a la
# que pertenece cada uno.
samples = []
classes = []

# Esta variable es para designar el número de clase para la clasificación.
class_n = 0

# Creamos una lista vacía para guardar los nombres de las categorías a medida
# que se leen del diccionario de entrenamiento y otra para el color de
# representación. El orden en los diccionarios en Python no está asegurado.
categorias = []
colores = []

# Iteramos por las clases de la estructura de datos de entrenamiento.
for k, v in entrenamiento.items():
    print(f"Procesando clase {k}")

    # Guardamos el nombre de la categoría.
    categorias.append(k)

    # Guardamos el color.
    colores.append(v["color"])

    # Iteramos las listas de entrenamiento en cada clase.
    for s in v["entrenamiento"]:
        # Añadimos los vectores de entrenamiento junto a la clase a la que
        # pertenecen.
        sample = [list(i) for i in sample_ms(ms, s)]
        class_s = [class_n for i in range(len(sample))]

        # Añadimos ambos elementos a las listas globales de entrenamiento.
        samples.extend(sample)
        classes.extend(class_s)

    # Aumentamos el identificador numérico de la clase.
    class_n += 1

# Los nombres de las bandas, para los gráficos.
bandas = ["U-Blue", "Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"]

# Hacemos el mismo estudio de la estructura de datos de entrenamiento.
for i in range(len(categorias)):
    # Para acumular los vectores de entrenamiento de la categoría.
    vectores_sample = []

    # Comparamos las listas de vectores y clases para quedarnos con los que nos
    # interesan.
    for j in range(len(samples)):
        if classes[j] == i:
            vectores_sample.append(samples[j])

    # La convertimos en un array de numpy.
    vectores_sample = np.array(vectores_sample)

    # Gráfico de reflectancia media en cada banda para el entrenamiento y la
    # clasificación.
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(
        f"Análisis del muestreo de entrenamiento para la categoría {categorias[i]}",
        fontsize=15,
    )

    # Calculamos la media, el máximo y el mínimo para cada banda.
    max = np.max(vectores_sample, axis=0)
    min = np.min(vectores_sample, axis=0)
    mean = np.mean(vectores_sample, axis=0)

    # Añadimos las líneas al gráfico.
    ax.plot(range(0, 7), mean, label="Media", color="black")
    ax.plot(range(0, 7), max, color="darkgrey")
    ax.plot(range(0, 7), min, color="darkgrey")

    # Create a margin zone between max and min
    ax.fill_between(range(0, 7), min, max, color="gray", alpha=0.2, label="Rango")

    # Obligamos al eje Y a ir a todo el rango de reflectancia, para poder ver
    # mejor la idoneidad de la zona de entrenamiento.
    ax.set_ylim(0, 1)
    ax.set_ylabel("Reflectancia")

    # El eje X son las bandas.
    ax.set_xlabel("Bandas")
    ax.set_xticks(range(len(bandas)))
    ax.set_xticklabels(bandas)

    # Mostramos leyenda.
    ax.legend()

    # Guardamos.
    plt.savefig(os.path.join(*out_dir, f"reflectancia_entrenamiento_{i}.png"))

# Creamos el clasificador con 50 árboles y entrenamos.
clf = RandomForestClassifier(n_estimators=50)
clf.fit(samples, classes)

# Al igual que hicimos en el caso del cluster, vamos a crear una "banda"
# adicional en el array multiespectral para recoger el resultado del
# clasificador.
n = np.zeros(shape=(ms.shape[0] * ms.shape[1], 1))
n[:] = np.nan

ms_vectores = np.resize(ms, (ms.shape[0] * ms.shape[1], 7))

ms_vectores = np.append(ms_vectores, n, axis=1)

# La máscara de los nan.
mascara_pixeles_no_nan = ~np.isnan(ms_vectores[:, :7]).all(axis=1)

# Aplicamos la máscara a los vectores espectrales y se los pasamos al modelo
# para que haga la predicción sobre las 7 bandas espectrales.
clasificacion = clf.predict(ms_vectores[mascara_pixeles_no_nan, :7])

# Utilizando la misma máscara booleana, metemos el resultado de la
# clasificación en la "banda" 8 de los vectores.
ms_vectores[mascara_pixeles_no_nan, 7] = clasificacion

# Volvemos a redimensionar a (x, y) de la imagen original.
random_forest = np.resize(ms_vectores, (ms.shape[0], ms.shape[1], 8))

# Preparamos una imagen para mostrar el resultado. Seleccionamos un número
# de colores igual al número de clusters para crear una leyenda de color.
cmap = mpl.colors.ListedColormap(colores)

# Mapeamos el cluster_reclass.
fig, ax = plt.subplots(figsize=figsize)
fig.suptitle("Random Forest", fontsize=20)
ax.imshow(random_forest[:, :, 7], aspect=1, cmap=cmap, interpolation="none")

# Añadimos una leyenda.
legend_elements = [
    Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor=colores[j],
        markersize=10,
        label=categorias[j],
    )
    for j in range(len(categorias))
]
ax.legend(handles=legend_elements, loc="upper right", title="Categorías")

plt.savefig(os.path.join(*out_dir, "random_forest.png"))

# Guardamos como GeoTIFF la clasificación.
save_geotiff_from_array(
    os.path.join(*out_dir, "random_forest.tif"), random_forest[:, :, 7:], profile
)

# Gráfico de reflectancia media en cada banda.
fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(
    "Reflectancia en bandas para clusters",
    fontsize=20,
)

for k in range(len(categorias)):
    group = ms_vectores[ms_vectores[:, 7] == k][:, :7]
    mean = np.mean(group, axis=0)

    ax.plot(range(0, 7), mean, label=f"{categorias[k]}", color=colores[k])

ax.set_xlabel("Bandas")
ax.set_ylabel("Reflectancia")
ax.set_xticks(range(len(bandas)))
ax.set_xticklabels(bandas)
ax.legend()

plt.savefig(os.path.join(*out_dir, "clusters_reflectancia.png"))
plt.show()

# Comparamos ahora la respuesta espectral media de las zonas de entrenamiento
# frente a la clasificación, para tener una idea de cómo de buena es la misma.

# Iteramos cada categoría.
for i in range(len(categorias)):
    # Para acumular los vectores de entrenamiento de la categoría.
    vectores_sample = []

    # Comparamos las listas de vectores y clases para quedarnos con los que nos
    # interesan.
    for j in range(len(samples)):
        if classes[j] == i:
            vectores_sample.append(samples[j])

    # La convertimos en un array de numpy.
    vectores_sample = np.array(vectores_sample)

    # Seleccionamos de los vectores clasificados los que pertenecen a la
    # categoría.
    vectores_clasificados = ms_vectores[ms_vectores[:, 7] == i, :7]

    # Gráfico de reflectancia media en cada banda para el entrenamiento y la
    # clasificación.
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(
        f"Comparativa muestreo de entrenamiento / clasificación para la categoría {categorias[i]}",
        fontsize=15,
    )

    # Calculamos las medias.
    mean_sample = np.mean(vectores_sample, axis=0)
    mean_clasificados = np.mean(vectores_clasificados, axis=0)

    # Añadimos las líneas al gráfico.
    ax.plot(range(0, 7), mean_sample, label="Entrenamiento", color="black")
    ax.plot(range(0, 7), mean_clasificados, label="Clasificación", color="red")

    ax.set_xlabel("Bandas")
    ax.set_ylabel("Reflectancia")
    ax.set_xticks(range(len(bandas)))
    ax.set_xticklabels(bandas)
    ax.legend()

    # Guardamos.
    plt.savefig(os.path.join(*out_dir, f"clusters_reflectancia_{i}.png"))

plt.close()
