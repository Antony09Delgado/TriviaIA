import json
import os


def mostrar_prompts_y_confirmar(archivo_json=None):
    if archivo_json is None:
        archivo_json = os.path.join(
            os.path.dirname(__file__),
            "..",
            "preguntas",
            "preguntas.json",
        )

    with open(archivo_json, "r", encoding="utf-8") as archivo:
        preguntas = json.load(archivo)

    if not isinstance(preguntas, list):
        raise ValueError("El archivo JSON no contiene una lista de preguntas.")

    total = len(preguntas)
    print(f"Se encontraron {total} prompts en el archivo.")
    print("=" * 60)

    variables = {}

    for i, pregunta in enumerate(preguntas, start=1):
        prompt = pregunta.get("prompt_imagen", "")
        nombre_variable = f"prompt_{i}"
        valor_variable = f"{i}.png"
        variables[nombre_variable] = valor_variable
        globals()[nombre_variable] = valor_variable

        print(f"Prompt {i}/{total}")
        print(prompt)
        print("-" * 60)

    while True:
        confirmacion = input("Escribe 'y' o 's' para cerrar: ").strip().lower()
        if confirmacion in {"y", "s"}:
            print("Confirmado. Cerrando función...")
            break
        print("esperando confirmacion. esperando de nuevo la y o la s")

    return variables


if __name__ == "__main__":
    resultado = mostrar_prompts_y_confirmar()
    print("\nVariables generadas:")
    for nombre, valor in resultado.items():
        print(f"{nombre} = {valor}")
    print(resultado)
