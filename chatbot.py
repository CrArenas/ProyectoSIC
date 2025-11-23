import json
import spacy



def get_response(message):
    user_doc = nlp(message)

    best_intent = None
    best_score = 0.0

    for intent in intents:
        for doc in intent["docs"]:
            score = user_doc.similarity(doc)
            if score > best_score:
                best_score = score
                best_intent = intent

    # Umbral mínimo para evitar respuestas incorrectas
    if best_score < 0.60:
        return "No te entiendo :(. ¿Podrías re escribir tu pregunta?"

    return best_intent["response"]

nlp = spacy.load("en_core_web_sm")

# Cargar intents
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

# Preprocesar doc de patterns
for intent in intents:
    intent["docs"] = [nlp(pattern) for pattern in intent["patterns"]]
