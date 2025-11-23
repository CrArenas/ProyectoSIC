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

st.set_page_config(page_title="Jerry", page_icon="", layout="centered")

st.markdown("""
    <style>
        /* Contenedor interno del chat */
        .chat-container {
            max-width: 600px;
            margin: auto;
            padding: 10px;
        }

        /* Scroll interno */
        .chat-scroll {
            max-height: 450px;
            overflow-y: auto;
            padding-right: 10px;
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

        /* Filas */
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

        /* Hover botón */
        button[kind="secondary"]:hover {
            background-color: #008069 !important;
            color: white !important;
        }

    </style>
""", unsafe_allow_html=True)

# --------------------------
# Cabecera superior
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
# Historial
# --------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --------------------------
# Contenedor con scroll
# --------------------------
st.markdown("<div class='chat-container chat-scroll' id='chat-box'>", unsafe_allow_html=True)

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

# --------------------------
# Auto-scroll al final
# --------------------------
st.markdown(
    """
    <script>
        const chatBox = window.parent.document.getElementById("chat-box");
        if (chatBox) {
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Input
# --------------------------
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

# --------------------------
# Enviar mensaje
# --------------------------
def procesar_mensaje():
    if user_input.strip():
        st.session_state["messages"].append({"role": "user", "content": user_input})
        bot_reply = get_response(user_input)
        st.session_state["messages"].append({"role": "bot", "content": bot_reply})
        st.rerun()

if send:
    procesar_mensaje()
