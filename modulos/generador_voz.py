import json
import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError

import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from rutas import audios, imagenes, preguntas

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "").strip()
MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2").strip()
OUTPUT_FORMAT = os.getenv("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128").strip()

FILE = preguntas / "preguntas.json"
CARPETA_AUDIOS = audios
CONTADOR_INTRO = audios / "contador_intro.json"
CLIENTE = None


def cargar_preguntas():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except Exception as e:
        print(f"Error al cargar preguntas: {e}")
        return []


def frases_intro():
    return [
        "Cuánto sabes de la Biblia?",
        "Demuestra que sabes de la Biblia.",
        "Prueba tus conocimientos bíblicos.",
        "Vamos a poner a prueba tu fe y tu conocimiento.",
        "¿Estás listo para responder preguntas bíblicas?",
    ]


def frase_intro_aleatoria():
    return random.choice(frases_intro())


def obtener_siguiente_numero_intro():
    os.makedirs(CARPETA_AUDIOS, exist_ok=True)

    if os.path.exists(CONTADOR_INTRO):
        with open(CONTADOR_INTRO, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
                numero = int(datos.get("siguiente", 1))
            except Exception:
                numero = 1
    else:
        numero = 1

    siguiente = numero + 1
    with open(CONTADOR_INTRO, "w", encoding="utf-8") as f:
        json.dump({"siguiente": siguiente}, f, indent=4, ensure_ascii=False)

    return numero


def obtener_cliente():
    global CLIENTE

    if CLIENTE is None:
        if not API_KEY:
            raise RuntimeError("No se encontró una API key de ElevenLabs. Define ELEVENLABS_API_KEY.")
        CLIENTE = ElevenLabs(api_key=API_KEY)

    return CLIENTE


def generar_audio(texto, ruta_archivo):
    os.makedirs(CARPETA_AUDIOS, exist_ok=True)

    cliente = obtener_cliente()

    try:
        audio = cliente.text_to_speech.convert(
            text=texto,
            voice_id=VOICE_ID,
            model_id=MODEL_ID,
            output_format=OUTPUT_FORMAT,
        )
    except ApiError as error:
        detalle = getattr(error, "body", None)
        mensaje = detalle.get("detail", {}).get("message", str(error)) if isinstance(detalle, dict) else str(error)
        raise RuntimeError(f"No se pudo generar el audio: {mensaje}") from error

    if isinstance(audio, (bytes, bytearray)):
        audio_bytes = bytes(audio)
    else:
        audio_bytes = b"".join(list(audio))

    with open(ruta_archivo, "wb") as archivo:
        archivo.write(audio_bytes)


def construir_texto_pregunta(pregunta):
    return (
        f"Pregunta {pregunta['numero']}: {pregunta['pregunta']} "
        f"Opción A: {pregunta['a']}. Opción B: {pregunta['b']}. Opción C: {pregunta['c']}."
    )


def construir_texto_respuesta(pregunta):
    valor_correcto = pregunta.get("respuesta_para_codigo") or pregunta.get("respuesta")

    if not valor_correcto:
        correcta = pregunta.get("correcta", "")
        if correcta == "a":
            valor_correcto = pregunta.get("a", "")
        elif correcta == "b":
            valor_correcto = pregunta.get("b", "")
        elif correcta == "c":
            valor_correcto = pregunta.get("c", "")
        else:
            valor_correcto = ""

    return f"Excelente. La respuesta correcta es {valor_correcto}."


def generar_audios(preguntas, esperar_segundos=10):
    os.makedirs(CARPETA_AUDIOS, exist_ok=True)

    intro_numero = obtener_siguiente_numero_intro()
    intro_ruta = os.path.join(CARPETA_AUDIOS, f"intro_{intro_numero}.mp3")
    intro_texto = frase_intro_aleatoria()
    generar_audio(intro_texto, intro_ruta)
    print(f"Audio intro guardado: {intro_ruta}")
    time.sleep(esperar_segundos)

    resultados = []

    for index, pregunta in enumerate(preguntas, start=1):
        pregunta_dict = dict(pregunta)
        pregunta_dict["numero"] = index

        pregunta_ruta = os.path.join(CARPETA_AUDIOS, f"pregunta_{index}.mp3")
        respuesta_ruta = os.path.join(CARPETA_AUDIOS, f"respuesta_{index}.mp3")

        if os.path.exists(pregunta_ruta):
            os.remove(pregunta_ruta)
        if os.path.exists(respuesta_ruta):
            os.remove(respuesta_ruta)

        texto_pregunta = construir_texto_pregunta(pregunta_dict)
        texto_respuesta = construir_texto_respuesta(pregunta_dict)

        generar_audio(texto_pregunta, pregunta_ruta)
        print(f"Audio pregunta guardado: {pregunta_ruta}")

        time.sleep(esperar_segundos)

        generar_audio(texto_respuesta, respuesta_ruta)
        print(f"Audio respuesta guardado: {respuesta_ruta}")

        resultados.append({
            "pregunta": pregunta_ruta,
            "respuesta": respuesta_ruta,
        })

        if index < len(preguntas):
            time.sleep(esperar_segundos)

    return resultados


def main():
    preguntas = cargar_preguntas()
    if not preguntas:
        print("No hay preguntas para convertir a audio.")
        return

    print("Generando audios...")
    generar_audios(preguntas)
    print("Audios terminados.")


if __name__ == "__main__":
    main()
