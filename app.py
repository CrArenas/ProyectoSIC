import streamlit as st
from chatbot import get_response
import base64

# --------------------------
# Función para convertir imágenes locales a base64
# --------------------------
def load_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Cargar imágenes en base64
bot_pic64 = load_image_base64("Imagenes/Botsito.jpg")
user_pic64 = load_image_base64("Imagenes/Perfil.jpg")

st.set_page_config(page_title="Orientador Vocacional", page_icon="🧭", layout="centered")

st.markdown("""
    <style>

        /* Fondo global del sitio (más claro) */
        body {
            background-color: #eceff1 !important;
        }

        .main {
            background-color: #eceff1 !important;
        }

        /* 📦 Caja principal del chat */
        .chat-wrapper {
            background-color: #1f2b38;
            padding: 20px;
            border-radius: 15px;
            max-width: 700px;
            margin: auto;
            box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
            margin-top: 20px;
            margin-bottom: 20px;
        }

        /* Contenedor general del contenido del chat */
        .chat-container {
            max-width: 600px;
            margin: auto;
            padding: 10px;
        }

        /* Cabecera */
        .chat-header {
            display: flex;
            align-items: center;
            background-color: #2b3a4a;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.08);
        }

        .chat-header img {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            margin-right: 12px;
            object-fit: cover;
        }

        .chat-header .name {
            font-size: 22px;
            font-weight: bold;
            color: white;
        }

        /* Fila del mensaje */
        .message-row {
            display: flex;
            align-items: flex-end;
            margin-bottom: 12px;
        }

        /* Fotos */
        .bot-pic, .user-pic {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            object-fit: cover;
        }

        .bot-pic { margin-right: 8px; }
        .user-pic { margin-left: 8px; }

        /* Burbujas */
        .bot-msg {
            background-color: #E5E5EA;
            padding: 10px 14px;
            border-radius: 15px 15px 15px 5px;
            max-width: 55%;
            color: black;
            font-size: 16px;
        }

        .user-msg {
            background-color: #008069;
            padding: 10px 14px;
            border-radius: 15px 15px 5px 15px;
            max-width: 55%;
            color: white;
            font-size: 16px;
        }

        /* Hover → verde */
        button[kind="secondary"]:hover {
            background-color: #008069 !important;
            color: white !important;
        }

    </style>
""", unsafe_allow_html=True)

# --------------------------
# Cabecera superior del chat
# --------------------------
st.markdown(
    f"""
    <div class='chat-header'>
        <img src="data:image/jpeg;base64,{bot_pic64}">
        <div class='name'>Jerry</div>
    </div>
    <div style="margin-bottom: 10px;">¿En qué puedo ayudarte hoy? </div>
    """,
    unsafe_allow_html=True
)


# --------------------------
# Crear historial de mensajes
# --------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# --------------------------
# Mostrar los mensajes con foto de perfil
# --------------------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="message-row" style="justify-content: flex-end;">
                <div class="user-msg">{msg['content']}</div>
                <img class="user-pic" src="data:image/jpeg;base64,{user_pic64}">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="message-row" style="justify-content: flex-start;">
                <img class="bot-pic" src="data:image/jpeg;base64,{bot_pic64}">
                <div class="bot-msg">{msg['content']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)

# Input
col1, col2 = st.columns([8, 2])

with col1:
    user_input = st.text_input(
        "",
        key="input",
        placeholder="Escribe aquí...",
        label_visibility="collapsed"
    )

with col2:
    send = st.button("Enviar", use_container_width=True)


# Función para enviar el mensaje
def procesar_mensaje():
    if user_input.strip():
        st.session_state["messages"].append({"role": "user", "content": user_input})
        bot_reply = get_response(user_input)
        st.session_state["messages"].append({"role": "bot", "content": bot_reply})
        st.rerun()


# Enviar con botón
if send:
    procesar_mensaje()
