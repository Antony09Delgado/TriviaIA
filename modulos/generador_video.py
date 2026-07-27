import random
import json
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip, ColorClip, AudioClip, VideoClip, vfx, afx

#========================IMAGENES DE INTRO========================

imagen_intro1 = r"C:\Users\Antony\Desktop\Trivia\imagenes\intro\1.png"
imagen_intro2 = r"C:\Users\Antony\Desktop\Trivia\imagenes\intro\2.jpg"
imagen_intro3 = r"C:\Users\Antony\Desktop\Trivia\imagenes\intro\3.jpg"

#=======================EFECTOS DE AUDIO========================

wosh_audio1 = r"C:\Users\Antony\Desktop\Trivia\audios\efectos\wosh1.mp3"
wosh_audio2 = r"C:\Users\Antony\Desktop\Trivia\audios\efectos\wosh2.mp3"
wosh_audio3 = r"C:\Users\Antony\Desktop\Trivia\audios\efectos\wosh3.mp3"
wosh_audio4 = r"C:\Users\Antony\Desktop\Trivia\audios\efectos\wosh4.mp3"


IMAGENES_INTRO = [imagen_intro1, imagen_intro2, imagen_intro3]
AUDIOS_WOSH = [wosh_audio1, wosh_audio2, wosh_audio3, wosh_audio4]


def obtener_imagen_intro_aleatoria():
    #Devuelve una imagen de intro elegida al azar.
    return random.choice(IMAGENES_INTRO)


def obtener_audio_wosh_aleatorio():
    #Devuelve un audio de efecto elegido al azar.
    return random.choice(AUDIOS_WOSH)


def obtener_ruta_audio_intro():
    #devuelve audio frase intro
    contador_path = r"C:\Users\Antony\Desktop\Trivia\audios\contador_intro.json"

    try:
        with open(contador_path, "r", encoding="utf-8") as f:
            datos = json.load(f)
            siguiente = int(datos.get("siguiente", 1))
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        siguiente = 1

    numero = max(1, siguiente - 1)
    path = fr"C:\Users\Antony\Desktop\Trivia\audios\intro_{numero}.mp3"
    return path


#____________________________________________________________________________________________________
#
#==================================HAREMOS EL VIDEO DE INTRO=========================================
#____________________________________________________________________________________________________


#--------------------------------------------------------------------cargamos cosas necesarias
imagen_intro = ImageClip(obtener_imagen_intro_aleatoria())
imagen_biblia = ImageClip(r"C:\Users\Antony\Desktop\Trivia\imagenes\intro\biblia.png")
frase_audio_intro = AudioFileClip(obtener_ruta_audio_intro())
duracion_total = frase_audio_intro.duration + 2  # Duración total del video de intro

#--------------------------------------------------------------------empezamos a darles valor de duracion
#                                                                      effectos o mas

imagen_intro = imagen_intro.with_duration(duracion_total)
imagen_biblia = imagen_biblia.with_duration(duracion_total).with_effects([vfx.Scroll(
    w=imagen_biblia.w,
    h=imagen_biblia.h,
    x_speed=0,
    y_speed=120,
    x_start=0,
    y_start=-300),  # Efecto de entrada desde la arriba
]).resized(height=200).with_fps(30).with_position(('center', 'center'))  # Redimensionar la imagen de la biblia
final = CompositeVideoClip([imagen_biblia])

final.write_videofile(r"C:\Users\Antony\Desktop\Trivia\marca\result.mp4")# Previsualizar la imagen de la biblia con efecto