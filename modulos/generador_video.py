import random
import json
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip, ColorClip, AudioClip, VideoClip, vfx, afx, TextClip, CompositeAudioClip

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
#==================================font=============================
fuente = r"C:\Users\Antony\Desktop\Trivia\fuentes\ConcertOne.ttf"


#____________________________________________________________________________________________________
#
#=================================animcion de entrada funcion=========================================
#____________________________________________________________________________________________________

def animacion(x_final, y_final, ancho, duracion_entrada=0.5):
    x_inicial = -ancho

    def posicion(t):
        if t < duracion_entrada:
            progreso = t / duracion_entrada
            x = x_inicial + (x_final - x_inicial) * progreso
            return (int(x), int(y_final))
        else:
            x = x_final
            return (int(x), int(y_final))

    return posicion


#____________________________________________________________________________________________________
#
#==================================HAREMOS EL VIDEO DE INTRO=========================================
#____________________________________________________________________________________________________


#--------------------------------------------------------------------cargamos cosas necesarias
imagen_intro = ImageClip(obtener_imagen_intro_aleatoria())
imagen_biblia = ImageClip(r"C:\Users\Antony\Desktop\Trivia\imagenes\intro\biblia.png")
frase_audio_intro = AudioFileClip(obtener_ruta_audio_intro())
duracion_total_intro = frase_audio_intro.duration + 1  # Duración total del video de intro

ANCHO, ALTO = 1080, 1920
canva = ColorClip(size=(ANCHO, ALTO), color=(255, 255, 255))


#--------------------------------------------------------------------empezamos a darles valor de duracion
#                                                                            effectos o mas               
# 
#                                                    
#--- canva fondo de intro negro
canva = canva.with_duration(duracion_total_intro)
#

#---------- imagen intro
intro_w, intro_h = imagen_intro.size
imagen_intro = imagen_intro.with_duration(duracion_total_intro)
imagen_intro = imagen_intro.with_fps(30).resized(height=ALTO, width=ANCHO).with_position(("center", "center"))

#--------------- imagen de la biblia
imagen_biblia = imagen_biblia.resized(height=555)  # Ajusta la altura de la imagen de la biblia
biblia_w,bibliah  = imagen_biblia.size

animacion_biblia_intro = animacion(
    x_final = 153,
    y_final = 1122,
    ancho = biblia_w,
    duracion_entrada = 0.2,
)

imagen_biblia = (
    imagen_biblia
    .with_duration(duracion_total_intro)
    .with_fps(30)
)

imagen_biblia = imagen_biblia.with_position(animacion_biblia_intro)

#--- texto..
texto_intro = TextClip(
    font=fuente,
    text="''Cuánto sabes de la Biblia?''",
    font_size=120,
    color="white",
    stroke_color="black",
    stroke_width=5,
    method="caption",
    size=(1013, 332),
    text_align="center",
)

texto_intro = texto_intro.with_duration(duracion_total_intro).with_fps(30)
w_texto_intro, _ = texto_intro.size
animacion_texto_intro = animacion(
    x_final = 34,
    y_final = 707,
    ancho = -w_texto_intro,
    duracion_entrada = 0.2,
)

texto_intro = texto_intro.with_position(animacion_texto_intro)

#---------------------audios de intro
frase_audio_intro = frase_audio_intro
wosh_intro_1 = AudioFileClip(obtener_audio_wosh_aleatorio())
wosh_intro_1 = wosh_intro_1.with_start(0.10)

audio_intro = CompositeAudioClip(
    [
    frase_audio_intro,
    wosh_intro_1
    ]
)

#----------------final de intro
final_intro = CompositeVideoClip(
    [
    canva,
    imagen_intro,
    imagen_biblia,
    texto_intro
    ]
    )
final_intro = final_intro.with_audio(audio_intro)
#final_intro.save_frame("preview_intro.png", t=3)  # Guardar un fotograma de vista previa
#final.preview(fps=15)
#final_intro.write_videofile(r"C:\Users\Antony\Desktop\Trivia\marca\result.mp4")# Previsualizar la imagen de la biblia con efecto


# =========================================================================================================
#                                         tercera parte 
#                                            final
#==========================================================================================================


#-------------------importamos  clip de video y audios necesarios

end_video = VideoFileClip(r"C:\Users\Antony\Desktop\Trivia\imagenes\end\fondo_final.gif")
audio_voz_chao = AudioFileClip(r"C:\Users\Antony\Desktop\Trivia\audios\final\final_voz.mp3")

duracion_end = audio_voz_chao.duration + 1  # Duración total del video 
end_video = end_video.with_fps(30).resized(height=ALTO, width=ANCHO)
end_video = end_video.with_effects([vfx.Loop(duration=duracion_end)])
end_video = end_video.with_position(("center", "center"))

#____________________________________________texto final
texto_end = TextClip(
    font=fuente,
    text="''Comenta tu Puntuación''",
    font_size=120,
    color="white",
    stroke_color="black",
    stroke_width=5,
    method="caption",
    size=(1013, 332),
    text_align="center",
)

texto_end = texto_end.with_duration(duracion_end).with_fps(30)
w_texto_end, _ = texto_end.size

animacion_texto_end = animacion(
    x_final = 34,
    y_final = 725,
    ancho = w_texto_end,
    duracion_entrada = 0.2,
)

texto_end = texto_end.with_position(animacion_texto_end)
#_________________________________________________________________audio
 
efecto_wosh_final = AudioFileClip(obtener_audio_wosh_aleatorio())
efecto_wosh_final = efecto_wosh_final.with_start(0.10)

audio_end = CompositeAudioClip([audio_voz_chao, efecto_wosh_final ])
end_video = end_video.with_effects([vfx.Resize(new_size=(1080, 1920))])
#_____________ ecportar
end = CompositeVideoClip(
    [
    end_video,
    texto_end
    ])

#end.preview(fps=15)
end = end.with_audio(audio_end)
end.write_videofile(
    "resultado_final.mp4",
    fps=24,
    codec="libx264",                      # Códec compatible
    preset="medium",                      # Asegura una codificación estándar
    audio_codec="aac", 
    ffmpeg_params=["-pix_fmt", "yuv420p"] # Formato de color compatible con Windows
)
#end.save_frame("preview_end.png", t=3)
#mañaa arreglo directorios para funcionar en cualquier pc