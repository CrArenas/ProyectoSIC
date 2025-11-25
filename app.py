import streamlit as st
from chatbot import get_response
import base64


def load_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bot_pic64 = load_image_base64("Imagenes/Botsito.png")
user_pic64 = load_image_base64("Imagenes/Perfil.jpg")

st.set_page_config(page_title="Jerry", page_icon="", layout="centered")

# -------------------------------------------------
#  ESTILOS CSS MEJORADOS
# -------------------------------------------------
st.markdown("""
    <style>

        body {
            background-color: #eef2f3;
        }

        /* Contenedor principal */
        .chat-container {
            max-width: 650px;
            margin: auto;
            padding: 15px;
            background: white;
            border-radius: 18px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.08);
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
            background: linear-gradient(135deg, #1e3c57, #335c81);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 15px;
            color: white;
        }

        .chat-header img {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            margin-right: 12px;
            object-fit: cover;
            border: 2px solid #ffffff55;
        }

        .chat-header .name {
            font-size: 22px;
            font-weight: bold;
        }

        /* Filas */
        .message-row {
            display: flex;
            align-items: flex-end;
            margin-bottom: 12px;
        }

        /* Fotos */
        .bot-pic, .user-pic {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            object-fit: cover;
        }

        .bot-pic { margin-right: 8px; }
        .user-pic { margin-left: 8px; }

        /* Burbujas bot */
        .bot-msg {
            background: #ffffff;
            padding: 12px 16px;
            border-radius: 15px 15px 15px 5px;
            max-width: 60%;
            color: #1e1e1e;
            font-size: 16px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            border-left: 4px solid #335c81;
        }

        /* Burbujas usuario */
        .user-msg {
            background: #008069;
            padding: 12px 16px;
            border-radius: 15px 15px 5px 15px;
            max-width: 60%;
            color: white;
            font-size: 16px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            border-right: 4px solid #006b55;
        }

        /* Input */
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 1px solid #cccccc;
            font-size: 17px;
            padding: 10px;
        }

        .stTextInput > div > div > input:focus {
            border: 1px solid #335c81;
        }

        /* Botón */
        .stButton > button {
            background-color: #335c81;
            border-radius: 12px;
            padding: 10px;
            color: white;
            border: none;
            font-size: 15px;
        }

        .stButton > button:hover {
            background-color: #1e3c57;
        }

    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# CABECERA
# -------------------------------------------------
st.markdown(
    f"""
    <div class="chat-container">
        <div class='chat-header'>
            <img src="data:image/jpeg;base64,{bot_pic64}">
            <div>
                <div class='name'>Jerry</div>
                <div style="font-size:13px; opacity:0.8;">Tu asistente personal</div>
            </div>
        </div>
        <div style="margin-bottom: 10px;">¿En qué puedo ayudarte hoy?</div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# MANEJO DE MENSAJES
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown("<div class='chat-scroll' id='chat-box'>", unsafe_allow_html=True)

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="message-row" style="justify-content:flex-end;">
                <div class="user-msg">{msg['content']}</div>
                <img class="user-pic" src="data:image/jpeg;base64,{user_pic64}">
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            f"""
            <div class="message-row" style="justify-content:flex-start;">
                <img class="bot-pic" src="data:image/jpeg;base64,{bot_pic64}">
                <div class="bot-msg">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# -------------------------------------------------
# SCROLL AUTOMÁTICO
# -------------------------------------------------
st.markdown("""
<script>
    const chatBox = window.parent.document.getElementById("chat-box");
    if (chatBox) {
        setTimeout(() => {
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 50);
    }
</script>
""", unsafe_allow_html=True)

# -------------------------------------------------
# INPUT Y BOTÓN
# -------------------------------------------------
col1, col2 = st.columns([8, 2])

with col1:
    user_input = st.text_input("", placeholder="Escribe aquí...", key="input", label_visibility="collapsed")

with col2:
    send = st.button("Enviar", use_container_width=True)

# -------------------------------------------------
# FUNCIÓN DE ENVÍO
# -------------------------------------------------
def procesar_mensaje():
    if user_input.strip():
        st.session_state["messages"].append({"role": "user", "content": user_input})
        bot_reply = get_response(user_input)
        st.session_state["messages"].append({"role": "bot", "content": bot_reply})
        st.rerun()

if send:
    procesar_mensaje()
