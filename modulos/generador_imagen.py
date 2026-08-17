import os
import json
import time
import requests
from urllib.parse import quote
from dotenv import load_sheet, load_dotenv
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from rutas import audios, imagenes, preguntas

# Esto busca el archivo .env y carga las claves en la memoria
load_dotenv()

TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

ARCHIVO_JSON = preguntas / "preguntas.json"
CARPETA_IMAGENES = imagenes


def cargar_preguntas():
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_preguntas(datos):
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )


def crear_carpeta():
    if not os.path.exists(CARPETA_IMAGENES):
        os.makedirs(CARPETA_IMAGENES)


def generar_imagen(prompt, nombre_archivo):
    hf_model = "runwayml/stable-diffusion-v1-5"
    url = f"https://api-inference.huggingface.co/models/{hf_model}"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "image/png",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True},
    }

    try:
        respuesta = requests.post(url, headers=headers, json=payload, timeout=120)
    except Exception as e:
        print("Error al solicitar imagen desde Hugging Face:", e)
        return None

    if respuesta.status_code == 200:
        ruta = os.path.join(CARPETA_IMAGENES, nombre_archivo)
        with open(ruta, "wb") as archivo:
            archivo.write(respuesta.content)
        print(f"Imagen guardada: {ruta}")
        return ruta

    print(f"Error al generar imagen en Hugging Face: status={respuesta.status_code}")
    try:
        print("Respuesta Hugging Face:", respuesta.text)
    except Exception:
        pass
    return None


def main():

    crear_carpeta()

    preguntas = cargar_preguntas()

    for i, pregunta in enumerate(preguntas):

        print(
            f"Generando imagen {i+1}/{len(preguntas)}"
        )

        ruta = generar_imagen(
            pregunta["prompt_imagen"],
            f"pregunta_{i+1}.png"
        )

        if ruta is not None:
            pregunta["imagen"] = ruta

    # Guardar nuevamente el JSON actualizado
    guardar_preguntas(preguntas)

    print("\nJSON actualizado correctamente")


if __name__ == "__main__":
    main()