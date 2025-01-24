entrenamiento = {
    "Pantano": {"entrenamiento": [[967, 983, 2095, 2183]], "color": "#5977cc"},
    "Océano": {"entrenamiento": [[1051, 1196, 301, 654]], "color": "#2c49a0"},
    "Suelo / urbano": {
        "entrenamiento": [
            [480, 495, 554, 603],
            [686, 689, 2116, 2120],
            [262, 269, 1297, 1304],
            [177, 188, 1025, 1026],
            [631, 632, 1887, 1899],
            [412, 413, 785, 794],
            [483, 484, 514, 517],
            [491, 492, 484, 486],
        ],
        "color": "#ababab",
    },
    "Aguas litorales": {"entrenamiento": [[806, 833, 558, 605]], "color": "#c0dfff"},
    "Vegetación vigorosa": {
        "entrenamiento": [
            [1106, 1120, 2162, 2180],
            [556, 573, 1093, 1106],
            [472, 475, 930, 942],
            [1071, 1081, 2017, 2029],
        ],
        "color": "#627b4c",
    },
    "Arena": {
        "entrenamiento": [[962, 966, 657, 667], [131, 134, 218, 222]],
        "color": "#ffcc00",
    },
    "Marisma": {"entrenamiento": [[729, 771, 713, 749]], "color": "#005b3f"},
    "Vegetación rala": {
        "entrenamiento": [
            [484, 493, 1085, 1102],
            [521, 523, 1531, 1534],
            [899, 905, 1595, 1600],
            [979, 1002, 993, 1017],
        ],
        "color": "#a7d22d",
    },
}


# Esta función extrae los vectores espectrales contenidos en un rectángulo
# de coordenadas dentro de la imagen definido por las siguientes coordenadas
# de imagen:
#
#   [ y_min, y_max, x_min, x_max ]
def sample_ms(ms, rect):

    samples = []

    for x in range(rect[0], rect[1]):
        for y in range(rect[2], rect[3]):

            samples.append(ms[x, y, :7])

    return samples
