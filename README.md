# ORG_MUSIC_MP3
# Organizador de archivos de música
Este script en Python está diseñado para organizar tus archivos de música en una estructura específica. Puede ser útil si tienes una colección de música desorganizada y quieres organizarla de manera ordenada para su uso en servidores de medios como Jellyfin y Navidrome.

## Características
1. Organiza archivos de música en carpetas por artista y álbum.
1. Limpia los nombres de archivos y carpetas de caracteres especiales y tildes.
1. Recoge el metadatos de los mp3 para poder crear la estructura necesaria dependiendo del servidor que hayas elegido.
1. En caso de utilizar los archivos de tener archivos temporales, como los que te crea MacOs, este no los copiará a la carpeta destino.
1. Puede manejar álbumes multidisco.
1. Copia las portadas de álbumes (archivos .jpg) y archivos PDF a la carpeta "Disc 1" en caso de álbumes multidisco y servidor Navidrome.

## Requisitos
### Para ejecutar este script, necesitarás:
- Python 3.11
- Las bibliotecas asyncio, unidecode, os, sys, re, shutil y eyed3.
- Puedes instalar las bibliotecas necesarias instalando el los requirements.txt

### ¿Qué debo de ingresar en la dirección de origen o ruta de origen?
**Deberás de ingresar una ruta que dentro de ella tenga la siguiente estructura dependiendo del caso:**

1. SI HAY DOS DISCOS

Carpeta base (normalmente tiene el nombre del album o artista)
 - Disc 1
   - ?PDF
   - Archivos MP3
   - COVER.JPG
 - Disc 2
   - Archivos MP3
 - Disc x...
   - Archivos MP3

2. SI HAY SOLO 1
- Carpeta base (normalmente tiene el nombre del album o artista)
   - ?PDF
   - Archivos MP3
   - COVER.JPG
   
### El directorio base que pasas puede tener varios albumes multidiscos y de disco único. El script recorrera todo el directorio para darte luego el orden que que necesites.

## Uso
1. Ejecuta el script y sigue las instrucciones.
1. Ingresa la ruta base (origen) donde se encuentran tus álbumes de música desorganizados.
1. Ingresa la ruta de destino donde deseas que se organicen los archivos.
1. Selecciona el tipo de servidor para el que deseas que se organice la estructura de archivos (Jellyfin o Navidrome).
1. El script recorrerá la ruta base, organizará tus archivos y copiará las portadas de álbumes y archivos PDF según la opción seleccionada.

# Notas adicionales
Asegúrate de que los archivos de música estén en formato MP3 para que el script los reconozca.

Si se encuentra un error al ejecutar el script, se mostrará un mensaje de error correspondiente.

¡Disfruta de tu música organizada!

Este script fue desarrollado por Diego Salinas.

[Enlace a la biblioteca eyed3](https://eyed3.readthedocs.io/en/latest/)

