import json
import os
import requests



FILE = r"C:\Users\Antony\Desktop\Trivia\preguntas\preguntas.json"

# =========================
# CONFIG OPENROUTER
# =========================
API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# =========================
# CARGAR JSON
# =========================
def cargar_preguntas():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except json.JSONDecodeError as e:
        print(f"Advertencia: el archivo JSON está vacío o tiene formato inválido: {e}")
        return []
    except Exception as e:
        print(f"Error al cargar preguntas: {e}")
        return []


# =========================
# GUARDAR JSON
# =========================
def guardar_preguntas(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================
# IA: GENERAR PROMPT
# =========================
def _prompt_fallback(pregunta):
    return (
        f"Imagen cinematográfica vertical 9:16, estilo realista y altamente detallada, "
        f"iluminación dramática, tono solemne y épico, inspirada en la pregunta: {pregunta}. "
        "La escena sugiere un momento bíblico o emocional importante sin revelar la respuesta, "
        "con enfoque en un elemento clave en primer plano o en el tercio inferior, "
        "composición con amplio espacio negativo en la parte superior para superposiciones de texto, "
        "sin texto, sin letras, sin subtítulos, sin logotipos."
    )


def _prompt_valido(prompt):
    if not prompt:
        return False

    texto = prompt.strip().lower()
    palabras_rechazo = [
        "user safety",
        "safety: safe",
        "content policy",
        "blocked",
        "policy violation",
        "no puedo",
        "no puedo ayudar",
    ]

    return not any(palabra in texto for palabra in palabras_rechazo)


def generar_prompt_ia(pregunta):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un experto en creación de prompts para generación de imágenes. "
                    "Devuelve SOLO un prompt visual. No expliques nada."
                )
            },
            {
                "role": "user",
                "content": (
                    "Convierte esta pregunta en un prompt para generar una imagen de fondo "
                    "para trivia biblica sin delatar la respuesta. "
                    "Debe ser cinematográfico, sin texto en la imagen, estilo épico, formato vertical 9:16.\n\n"
                    f"Pregunta: {pregunta}"
                )
            }
        ]
    }

    try:
        response = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()

        prompt = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        prompt = prompt.strip() if isinstance(prompt, str) else ""

        if _prompt_valido(prompt):
            return prompt

        print("La IA devolvió un contenido de seguridad o inválido. Usando fallback.")
        return _prompt_fallback(pregunta)

    except Exception as e:
        print("Error IA:", e)
        return _prompt_fallback(pregunta)


# =========================
# CREAR PREGUNTA
# =========================
def crear_pregunta():
    print("\n=== NUEVA PREGUNTA ===")

    pregunta = input("Pregunta: ")
    a = input("Opción A: ")
    b = input("Opción B: ")
    c = input("Opción C: ")
    correcta = input("Correcta (a/b/c): ").lower()

    print("\n⏳ Generando prompt con IA...")

    prompt = generar_prompt_ia(pregunta)

    print("\n✔ Prompt generado:")
    print(prompt)

    respuesta_correcta = {
        "a": a,
        "b": b,
        "c": c,
    }.get(correcta, "")

    return {
        "pregunta": pregunta,
        "a": a,
        "b": b,
        "c": c,
        "correcta": correcta,
        "respuesta_para_codigo": respuesta_correcta,
        "prompt_imagen": prompt
    }


# =========================
# MAIN
# =========================

def main():
    preguntas = cargar_preguntas()

    while True:
        print("\n========================")
        print(f"Preguntas guardadas: {len(preguntas)}")
        print("========================")

        opcion = input("\n1) Agregar pregunta\n2) Reiniciar archivo\n3) Salir\nOpción: ").strip()

        if opcion == "1":
            q = crear_pregunta()
            preguntas.append(q)
            guardar_preguntas(preguntas)

            print("\n✔ Pregunta guardada en JSON")

        elif opcion == "2":
            confirmar = input("¿Seguro que quieres borrar todas las preguntas? (s/n): ").strip().lower()
            if confirmar in {"s", "si", "sí", "y"}:
                preguntas = []
                guardar_preguntas(preguntas)
                print("\n✔ Archivo reiniciado. Sin preguntas guardadas.")
            else:
                print("Operación cancelada.")

        elif opcion == "3":
            break

        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
