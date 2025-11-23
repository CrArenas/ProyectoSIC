# chatbot.py — Gemini versión completa
import os
import json
from typing import Dict, Any
import google.generativeai as genai


if os.path.exists("user_profile.json"):
        with open("user_profile.json", "w", encoding="utf-8") as f:
            f.write("{}")


# -----------------------------------
# CONFIGURACIÓN GEMINI
# -----------------------------------

API_KEY = "X"
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-flash-latest"
PROFILE_PATH = "user_profile.json"


# -----------------------------------
# Perfil del usuario
# -----------------------------------

def load_profile() -> Dict[str, Any]:
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_profile(profile: Dict[str, Any]):
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def update_profile(profile: Dict[str, Any], user_input: str):
    profile.setdefault("historial", [])

    # Guardamos mensajes cortos como intereses
    if len(user_input) < 200:
        profile["historial"].append(user_input)

    return profile


# -----------------------------------
# FUNCIÓN PRINCIPAL DEL CHATBOT
# -----------------------------------

def get_response(user_input: str):

    # Cargar y actualizar perfil en cada mensaje
    profile = load_profile()
    profile = update_profile(profile, user_input)
    save_profile(profile)

    # Construcción del prompt
    prompt = f"""
Eres Jerry, un orientador tecnológico, eres amable, cálido, cercano y realista.
Hablas como una persona normal, sin sonar robótico, y te gusta usar emojis simples :)

 Tu misión:
- ayudar al usuario a entender el mundo de la tecnología
- explicar conceptos técnicos con claridad
- recomendar rutas de aprendizaje
- motivar de manera honesta y realista
- dar consejos prácticos basados en el perfil del usuario

 Perfil del usuario:
{json.dumps(profile, ensure_ascii=False)}

No uses listas ni formato técnico rígido.

No te extiendas tanto en tus mensajes, es bueno que seas conciso y directo, con 2 frases es suficiente.

No hablas con jergas de ningún país, utilizas un español neutro.

Usuario: {user_input}
Jerry:
"""

    # Llamado a Gemini
    model = genai.GenerativeModel(MODEL_NAME)

    response = model.generate_content(prompt)

    # Convertir respuesta a texto plano
    return response.text.strip()
