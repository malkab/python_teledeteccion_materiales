import rasterio


# Lee el perfil de una imagen GeoTIFF. El perfil incluye muchos datos
# importantes para la georreferenciación de la imagen, es decir, para ubicarla
# con precisión sobre la superficie terrestre, como por ejemplo el sistema de
# coordenadas y la proyección, así como la resolución de la imagen y las
# coordenadas de anclaje en el territorio. Este perfil nos va a permitir
# enclavar las imágenes que producimos en el mismo lugar que las imágenes
# originales.
def load_geo_profile(geotiff_path):

    # Abre el fichero GeoTIFF pasado y lee su perfil
    with rasterio.open(geotiff_path) as dataset:
        profile = dataset.profile
        return profile


# Esta función guarda un array de shape (x, y, n) o (x, y) en un archivo
# GeoTIFF.
def save_geotiff_from_array(output_path, array, profile):

    # Actualizamos el perfil GeoTIFF para indicarle el número de bandas que va a
    # tener el GeoTIFF.

    # Unibanda
    if len(array.shape) == 2:
        profile.update(count=1)

    # Multibanda
    else:
        profile.update(count=array.shape[2])

    # Apertura de un GeoTIFF para escritura, asignándole el perfil de otro para
    # que tengan el mismo posicionamiento terrestre.
    with rasterio.open(output_path, "w", **profile) as dst:

        # Unibanda
        if len(array.shape) == 2:

            # Creación de la única banda del GeoTIFF.
            dst.write(array.astype(rasterio.float32), 1)

        # Multibanda
        else:

            # Creación de cada una de las bandas del GeoTIFF, que se corresponde
            # con los componentes de la dimensión n.
            for i in range(array.shape[2]):
                dst.write(array[:, :, i].astype(rasterio.float32), i + 1)
