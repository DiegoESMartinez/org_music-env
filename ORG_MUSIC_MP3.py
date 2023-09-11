#CODIGO EN ESPAÑOL OLEEEEEEEEEEEEEEEEEE
#IMPORTACIONES
from asyncio import sleep
from unidecode import unidecode
import os
import sys
import re
import shutil
import eyed3


##################################FUNCIONES###############################################
# FUNCION PARA RECORRER LOS DIRECTORIOS
def recorrer_directorios(directorio_base,multidisco:bool):
  if os.path.isdir(directorio_base):
        for item in os.listdir(directorio_base):
            item_path = os.path.join(directorio_base, item)
            if os.path.isdir(item_path):
                    if fuente_canciones == directorio_base:
                        recorrer_directorios(item_path,False)
                    else:
                        multi_disco(directorio_base,item_path)
                        break                    
            else:
                if esMP3(item_path):
                   if multidisco:
                       return item_path
                   else:
                        disco_unico(directorio_base,item_path)
                        break
                    


# FUNCION PARA COMPROBAR SI HAY UN ARCHIVO MP3
def esMP3(path):
    return path.endswith('.mp3') and not os.path.basename(path).startswith("._")

# FUNCION PARA COMPROBAR SI UNA RUTA EXISTE
def existeRuta(path):
	return os.path.exists(path)

#FUNCION PARA DETERMINAR EL SISTEMA OPEATIVO
def sistemaOperativo():
     # Obtiene la plataforma del sistema
    return sys.platform

    
# FUNCION PARA ELIMINAR LOS CARACTERES ESPECIALES Y TILDES
def eliminar_caracteres_especiales(texto):
    # Quitar tildes y dieresis
    texto_sin_acentos = unidecode(texto)
    # Expresion regular para eliminar todos los caracteres que no sean letras, numeros o espacios en blanco
    texto_limpio = re.sub(r'[^a-zA-Z0-9\s]', '', texto_sin_acentos)
    
    return texto_limpio

#FUNCION PARA CREAR CARPETAS
def crear_directorios(diccionario:dict):
    ruta_carpeta_completa = os.path.join(destino_canciones, f'{diccionario["artista_de_album"]}')
    ruta_carpeta_completa = os.path.join(ruta_carpeta_completa, f'{diccionario["album"]} {diccionario["lanzamiento"]}')
# Intenta crear la carpeta completa junto con todas las subcarpetas necesarias
    try:
        os.makedirs(ruta_carpeta_completa)
        print(f"Carpeta completa '{ruta_carpeta_completa}' creada exitosamente.")
        return ruta_carpeta_completa
    except OSError as error:
        print(f"No se pudieron crear las carpetas: {error}")
        return "ERROR"

#FUNCION PARA MOVER DE UNA CARPETA A OTRA EL CONTENIDO
def mudar_contenido(ruta_origen,ruta_destino,multidisco:bool):



    #COPIAMOS LA CARPETA COMPLETA CON SU ESTRUCTURA
    contenido = os.listdir(ruta_origen)
    contenido = ignorar_archivos_temporales(ruta_origen, contenido)
    
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
    
    for elemento in contenido:
        origen_elemento = os.path.join(ruta_origen, elemento)
        destino_elemento = os.path.join(ruta_destino, elemento)
        
        if os.path.isdir(origen_elemento):
            mudar_contenido(origen_elemento, destino_elemento,multidisco)
        else:
            if  not origen_elemento.endswith((".pdf", ".jpg")) if servidor == "2" and multidisco else True :
                shutil.copy2(origen_elemento, destino_elemento)



#FUNCION PARA FILTRAR LOS TEMPORALES 
def ignorar_archivos_temporales(ruta, nombres):
    return [nombre for nombre in nombres if not nombre.startswith(".")]

#def filtrar_temporales(ruta_origen):
#    return [os.path.join(root, filename) for root, _, files in os.walk(ruta_origen) for filename in files if filename.startswith(".")] 

#FUNCION PARA MOVER TODOS LOS COVER Y LOS PDF A DISC 1
def mudar_media_multidisc(carpeta_origen,destinacion,multidisco:bool):
    
    carpeta_destino = os.path.join(destinacion,"Disc 1") if multidisco else destinacion

    contenido_origen=os.listdir(carpeta_origen)

    # Recorre el directorio de origen
# Recorre el directorio de origen y sus subdirectorios de forma recursiva
    for filename in contenido_origen:
            if filename.endswith((".pdf", ".jpg")) and not filename.startswith("."):
                origen = os.path.join(carpeta_origen,filename)
                destino = os.path.join(carpeta_destino,filename)
                shutil.copy2(origen, destino)
                print(f"Moviendo {filename} a {carpeta_destino}")

#FUNCION PARA SACAR METADATOS DE MP3
def extraer_datos(path):
    if existeRuta(path):
        datosAudio = eyed3.load(path)
        datosAudio.tag.save()
        return {
                'artista_de_album' : eliminar_caracteres_especiales(datosAudio.tag.album_artist.split(",")[0]),
                'album' : eliminar_caracteres_especiales(datosAudio.tag.album[0:50]),
                'lanzamiento':f"({str(datosAudio.tag.recording_date)})"
        }
    else:
         return {'ERROR':f"HUBO UN ERROR EN LA RECOGIDA DE LA RUTA DEL ARCHIVO MP3 '{path}', vuelva a intentarlo"} 

          

#FUNCION DE UN DISCO
def disco_unico(path,item_path):
    datos_album=extraer_datos(item_path)

    if "ERROR" in datos_album.keys():
         print(datos_album["ERROR"])
         return
    else:
        ruta_destino = crear_directorios(datos_album) 
        mudar_contenido(path,ruta_destino,False)
        


#FUNCION DE DOS DISCOS O MAS
def multi_disco(path,item_path):
    datos_album=extraer_datos(recorrer_directorios(item_path,True))

    if "ERROR" in datos_album.keys():
            print(datos_album["ERROR"])
            return
    else:
        ruta_destino = crear_directorios(datos_album) 
        mudar_contenido(path,ruta_destino,True)
        if servidor == "2":
            mudar_media_multidisc(path,ruta_destino,True)


##################################################################################################################



sisOpe=sistemaOperativo()        


#PEDIR RUTA DE ORIGEN DE LOS ALBUMES
print(f"SISTEMA OPERATIVO: {sisOpe}")
fuente_canciones=""
while(True):
    fuente_canciones =input("RUTA BASE (ORIGEN) DE LOS ALBUMES: ")
    if existeRuta(fuente_canciones):
        break
    else:
        print("La ruta de base que has introducido no existe.")
        if input("¿DESEA VOLVER A INTRODUCIR LA RUTA BASE? SI/NO : ").upper()!="SI":            
            print("Como ha introducido no o cualquier otra para palabra diferente a 'SI' se cierra automaticamente el programa")
            sys.exit()

#PEDIR RUTA DE GUARDACION
destino_canciones=""
while(True):
    destino_canciones = input("DESTINO DE LAS CANCIONES: ")
    if existeRuta(destino_canciones):
        break
    else:
        print("La ruta de destino que has introducido no existe.")
        if input("¿DESEA VOLVER A INTRODUCIR LA RUTA DESTINO? SI/NO : ").upper()!="SI":
            print("Como ha introducido no o cualquier otra para palabra diferente a 'SI' se cierra automaticamente el programa")
            sys.exit()

#PREGUNTAR PARA QUE SERVIDOR ESTA DIRIGIDO
servidor=input("SELECCIONE PARA QUE TIPO DE SERVIDOR QUIERE LA ESTRUCTURA DE ARCHIVOS\n1- Jellyfin\n2. Navidrome\nCualquier otro numero o caracter producirá que se cierre el programa\nINTRODUZCA SU SERVIDOR (1\\2): ")
if servidor not in ["1","2"]:
        print("Como ha introducido un numero o cualquier otro caracter diferente a '1' o '2' se cierra automaticamente el programa")






#Comprobar si la ruta existe
if existeRuta(fuente_canciones) and existeRuta(destino_canciones):
#RECORRER RUTA DE CARPETA RAIZ SI EXISTE CARPETA
    recorrer_directorios(fuente_canciones,False)

    mensaje_despedida="""
PROCESO FINALIZADO

                                    /T /I                     
                                   / |/ | .-~/                
                               T\ Y  I  |/  /  _              
              /T               | \I  |  I  Y.-~/              
             I l   /I       T\ |  |  l  |  T  /               
          T\ |  \ Y l  /T   | \I  l   \ `  l Y                
      __  | \l   \l  \I l __l  l   \   `  _. |                
      \ ~-l  `\   `\  \  \\ ~\  \   `. .-~   |                
       \   ~-. "-.  `  \  ^._ ^. "-.  /  \   |                
     .--~-._  ~-  `  _  ~-_.-"-." ._ /._ ." ./                
      >--.  ~-.   ._  ~>-"    "\\   7   7   ]                 
     ^.___~"--._    ~-{  .-~ .  `\ Y . /    |                 
      <__ ~"-.  ~       /_/   \   \I  Y   : |                 
        ^-.__           ~(_/   \   >._:   | l______           
            ^--.,___.-~"  /_/   !  `-.~"--l_ /     ~"-.                      
                   (_/ .  ~(   /'     "~"--,Y   -=b-. _)      
                    (_/ .  \  :           / l      c"~o \     
                     \ /    `.    .     .^   \_.-~"~--.  )    
                      (_/ .   `  /     /       !       )/     
                       / / _.   '.   .':      /        '      
                       ~(_/ .   /    _  `  .-<_               
                         /_/ . ' .-~" `.  / \  \          ,z=.
                         ~( /   '  :   | K   "-.~-.______//   
                           "-,.    l   I/ \_    __{--->._(==. 
                            //(     \  <    ~"~"     //       
                           /' /\     \  \     ,v=.  ((        
                         .^. / /\     "  }__ //===-  `       GRACIAS POR UTILIZAR NUESTRO SCRIPT :) 
                        / / ' '  "-.,__ {---(==-              
                      .^ '       :  T  ~"   ll         
                     / .  .  . : | :!        \\               
                    (_/  /   | | j-"          ~^              
                      ~-<_(_.^-~"                         
    
"""

    print(mensaje_despedida)

