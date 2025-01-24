#!/usr/bin/env python
# coding=UTF8
# -*- coding: utf-8 -*-

import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from helpers.raster import load_geo_profile, save_geotiff_from_array
from matplotlib.lines import Line2D
from sklearn.cluster import KMeans

"""

  Este script crea una clasificación automática de los píxeles con clusters K.

"""
# Tamaño de las imágenes.
figsize = (20, 10)

# Esta variable apunta a la versión de las imágenes que vamos a utilizar, para
# más comodidad.
data_dir = ["..", "data", "000_in", "clipped-mask"]

# Esta lo hace al directorio de salida de resultados base y a uno específico
# para este script y crea éste último si no existe.
out_base_dir = ["..", "data", "900_out"]
out_dir = [*out_base_dir, "070"]

if not os.path.exists(os.path.join(*out_dir)):
    os.makedirs(os.path.join(*out_dir))

# Leemos el perfil GeoTIFF de una de las imágenes originales para utilizarlo en
# las imágenes nuevas.
profile = load_geo_profile(os.path.join(*data_dir, "b_1-ultrablue.tif"))

# Carga del array multiespectral.
ms = np.load(os.path.join(*out_base_dir, "multiespectral.npy"))

# Ahora, para entrenar a KMeans, necesitamos pasar de una shape (1333, 2439, 7)
# a (vectores pixel, 7 bandas). Estamos pasando de una estructura de 3
# dimensiones (x, y, banda) a una de dos dimensiones (pixel, bandas)
vectores = np.resize(ms, (ms.shape[0] * ms.shape[1], 7))

print()
print(f"La nueva estructura de datos tiene la forma: {str(vectores.shape)}")

print()
print(f"El vector del pixel en posición 250000 es: {str(vectores[250000])}")

print()
print(f"El vector del pixel en posición 0 es: {str(vectores[0])}")

# KMeans no permite la existencia de datos nan, y tenemos bastantes. Eliminamos
# los vectores NaN creando una máscara que descarta todos los píxeles que tengan
# todas sus componentes vectoriales a nulo. Para ello, confeccionaremos una
# máscara booleana true / false que filtrará todos aquellos vectores que tengan
# todas las componentes NaN. Como primer paso, utilizamos la función Numpy
# isnan() que devuelve verdadero si el elemento considerado es NaN:
filtro_0 = np.isnan(vectores)

print()
print(f"Forma del filtro_0: {str(filtro_0.shape)}")
print(f"Elemento 0 y 250000 del filtro_0: {filtro_0[0]}, {filtro_0[250000]}")

# Con el filtro 0 obtenemos el valor de np.isnan aplicado indiscriminadamente a
# todos los valores de vectores, sin tener en cuenta la dimensionalidad. De
# esta forma, los valores nulos (como el 0) tienen todas sus componentes TRUE
# (todas son NaN) y los que tienen datos radiométricos los tienen todos a FALSE.
# No pueden existir (no deberían, en cualquier caso) píxeles con algunas
# componentes nulas.

# Ahora refinamos el filtro con la función all() de Numpy. all() devuelve
# verdadero si todos los elementos considerados son True:
filtro_1 = np.isnan(vectores).all()

print()
print(f"Forma del filtro_1: {str(filtro_1.shape)}")
print(f"Valor de filtro_1: {str(filtro_1)}")

# filtro_1 resulta ser un escalar False puesto que all() ha sido aplicada al
# array completo indiscriminadamente. Como lo que queremos en realidad es
# aplicarlo dentro de cada vector, podemos utilizar el usual argumento opcional
# "axis" que poseen muchas funciones Numpy para aplicar la función en un eje del
# array determinado. En nuestro caso, axis=0 sería una aplicación columnar, es
# decir, a todos los valores de todos los vectores para cada longitud de onda
# (todos los azules, todos los rojos, etc.). Lo que queremos sin embargo es
# aplicar all() en el contexto del axis=1, es decir, dentro de los vectores
# propiamente dichos, para ver si todas sus componentes son NaN:
filtro_2 = np.isnan(vectores).all(axis=1)

print()
print(f"Forma del filtro_2: {str(filtro_2.shape)}")
print(f"Elemento 0 y 250000 del filtro_2: {filtro_2[0]}, {filtro_2[250000]}")

# Si aplicamos este filtro, estaríamos filtrando los vectores nulos (los que
# tienen true en el array máscara o filtro). Como queremos los contrarios, sólo
# tenemos que negar el booleano:
filtro_3 = ~np.isnan(vectores).all(axis=1)

print()
print(f"Forma del filtro_3: {str(filtro_3.shape)}")
print(f"Elemento 0 y 250000 del filtro_3: {filtro_3[0]}, {filtro_3[250000]}")

# Ahora sólo tenemos que aplicar el filtro como máscara booleana al array
# original de vectores:
vectores_no_nan = vectores[filtro_3]

print()
print(f"La forma del array con la máscara aplicada es: {str(vectores_no_nan.shape)}")
print(
    f"Elemento 0 y 250000 del array filtrado: {vectores_no_nan[0]}, {vectores_no_nan[250000]}"
)

# Ahora ya tenemos un array de ~2700K vectores de siete componentes, todas no
# nulas, con los que operar.

# En la clusterización K, dado que el número óptimo de clústeres puede no estar
# claro a priori, es un buen ejercicio someter a los datos a clusterizaciones
# con un número creciente de clusters para ver el efecto de generalización u
# overfitting del proceso

# Primero, cogemos un set de entrenaminto de 500000 vectores. Con
# np.random.choice obtenemos los índices de 500000 vectores de vectores, es
# decir, se coge el número total de vectores (vectores.shape[0], el tamaño de la
# primera dimensión de los vectores) y de estos índices se cogen al azar 500000:
n = np.random.choice(vectores_no_nan.shape[0], size=500000)

# Ahora hacemos slicing del array de vectores en función de dichos índices
# aleatorios:
training_set = vectores_no_nan[n, :]

print()
print(f"Dimensión de la muestra: {str(training_set.shape)}")

# Unos colores para hacer los gráficos (habría que incluir más colores para
# hacer más de 7 clusters).
colores = ["royalblue", "cyan", "yellow", "orange", "red", "green", "gray"]

# Los nombres de las bandas.
bandas = ["U-Blue", "Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"]

# El máximo número de clústeres a probar.
max_clusters = 7

# El número de veces que se ejecutará el algoritmo con diferentes centroides. Se
# queda con el mejor resultado.
n_init = 20

# Para almacenar los errores medios cuadráticos de cada clusterización.
inercias = []

for i in range(2, max_clusters + 1):
    # Un índice de base 0, para diversos usos.
    idx = i - 2

    print()
    print(f"Clustering con {i} clusters...")

    # Creamos el modelo.
    kmeans = KMeans(n_clusters=i, n_init=n_init).fit(training_set)

    # Obtener la inercia del modelo (suma de las distancias al cuadrado de los
    # puntos a sus centros más cercanos).
    inertia = kmeans.inertia_
    print(f"EMC del modelo con {i} clusters: {inertia}")

    inercias.append(inertia)

    # Lo aplicamos sobre el total de los vectores.
    clusters = kmeans.predict(vectores_no_nan)

    # Ahora tenemos que asignar los clusters calculados a cada pixel. Para ello,
    # añadimos una nueva "banda" con las dimensiones del array multiespectral de
    # NaN para almacenar la información del cluster en el que cae cada pixel y
    # se lo añadimos a vectores.
    blank = np.zeros(shape=(ms.shape[0] * ms.shape[1]))
    blank[:] = np.nan

    blank[filtro_3] = clusters

    cluster_reclass = np.resize(blank, (ms.shape[0], ms.shape[1], 1))

    save_geotiff_from_array(
        os.path.join(*out_dir, f"clusters_{i}.tif"), cluster_reclass, profile
    )

    ms_cluster = np.append(ms, cluster_reclass, axis=2)

    ms_cluster = np.reshape(ms_cluster, (ms.shape[0] * ms.shape[1], 8))

    # Preparamos una imagen para mostrar el resultado. Seleccionamos un número
    # de colores igual al número de clusters para crear una leyenda de color.
    cmap = mpl.colors.ListedColormap(colores[:i])

    # Mapeamos el cluster_reclass.
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f"Clusterización K - {i} clusters", fontsize=20)
    ax.imshow(cluster_reclass, aspect=1, cmap=cmap, interpolation="none")

    # Añadimos una leyenda.
    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=colores[j],
            markersize=10,
            label=f"{j}",
        )
        for j in range(i)
    ]
    ax.legend(handles=legend_elements, loc="upper right", title="Clusters")

    plt.savefig(os.path.join(*out_dir, f"clusters_{i}.png"))

    # Gráfico de reflectancia media en cada banda.
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(
        f"Reflectancia en bandas para {i} clusters",
        fontsize=20,
    )

    for k in range(i):
        group = ms_cluster[ms_cluster[:, 7] == k][:, :7]
        mean = np.mean(group, axis=0)

        ax.plot(range(0, 7), mean, label=f"{k}", color=colores[k])

    ax.set_xlabel("Bandas")
    ax.set_ylabel("Reflectancia")
    ax.set_xticks(range(len(bandas)))
    ax.set_xticklabels(bandas)
    ax.legend()

    plt.savefig(os.path.join(*out_dir, f"clusters_{i}_reflectancia.png"))

# Creamos un gráfico de dos dimensiones con los valores de inercia en el eje Y y
# la posición de las inercias en el array inercias en el eje X.
plt.figure(figsize=figsize)
plt.plot(range(2, max_clusters + 1), inercias, marker="o")
plt.title("Inercia vs Número de Clusters")
plt.xlabel("Número de Clusters")
plt.ylabel("Inercia")
plt.grid(True)
plt.savefig(os.path.join(*out_dir, "inertia_vs_clusters.png"))

plt.close()
