# chatbot.py (versión rápida con 8-bit)
import os
import json
from typing import Dict, Any

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
PROFILE_PATH = "user_profile.json"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Cargando modelo {MODEL_NAME} en {DEVICE} en 8-bit...")

# --- CONFIGURACIÓN PARA 8-BIT ---
bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0,
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto"
)

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
    profile.setdefault("historial_temas", [])

    if len(user_input) < 200:
        profile["historial_temas"].append(user_input)

    return profile


# -----------------------------------
# Generación rápida
# -----------------------------------
def generate(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    output = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.05
    )

    return tokenizer.decode(output[0], skip_special_tokens=True)


# -----------------------------------
# Función principal del chatbot
# -----------------------------------
def get_response(user_input: str):

    profile = load_profile()
    profile = update_profile(profile, user_input)

    prompt = f"""
Eres Jerry, un orientador tecnológico amable, cercano y realista.
Tu estilo es cálido, directo y humano.
Evita sonar como robot o como manual.

Usuario: {user_input}
Jerry:
"""

    raw = generate(prompt)

    if "Jerry:" in raw:
        raw = raw.split("Jerry:")[-1].strip()

    save_profile(profile)
    return raw
