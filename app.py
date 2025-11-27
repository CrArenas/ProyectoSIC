import streamlit as st
from chatbot import get_response
import base64
import time

# ================= IMÁGENES BASE64 =================
def load_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bot_pic64 = load_image_base64("Imagenes/Botsito.png")
user_pic64 = load_image_base64("Imagenes/Perfil.jpg")

st.set_page_config(page_title="Jerry", layout="centered")

# =============== FONDO DEGRADADO ===============
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg,#1e3c57,#335c81,#213d5a);
        background-attachment: fixed;
    }

    /* SCROLL */
    .chat-scroll{max-height:420px;overflow-y:auto;padding:10px;}
    .chat-scroll::-webkit-scrollbar{width:7px;}
    .chat-scroll::-webkit-scrollbar-thumb{background:#7792aa;border-radius:10px;}

    /* BURBUJAS */
    .bot-msg{background:#fff;padding:12px 16px;border-radius:15px 15px 15px 5px;
             border-left:4px solid #335c81;font-size:16px;max-width:60%;
             box-shadow:0 2px 6px rgba(0,0,0,.08)}
    .user-msg{background:#008069;padding:12px 16px;color:white;border-radius:15px 15px 5px 15px;
              border-right:4px solid #006b55;font-size:16px;max-width:60%;
              box-shadow:0 2px 6px rgba(0,0,0,.1)}

    .msg{display:flex;margin-bottom:12px;animation:fadeUp .3s ease;}
    @keyframes fadeUp{from{opacity:0;transform:translateY(6px);}to{opacity:1;}}

    .header{padding:15px;border-radius:18px;margin-bottom:12px;color:white;
            background:rgba(255,255,255,.06);backdrop-filter:blur(6px);text-align:center;}
    .header img{width:60px;height:60px;border-radius:50%;margin-bottom:6px;border:2px solid #ffffff80;}

    /* ---- TYPING BOX ---- */
    .typing-box{background:white;padding:10px 15px;border-radius:18px;display:flex;align-items:center;gap:7px;}
    .dot{width:7px;height:7px;background:#777;border-radius:50%;animation:blink 1.3s infinite;}
    .dot:nth-child(2){animation-delay:.2s;}
    .dot:nth-child(3){animation-delay:.4s;}
    @keyframes blink{0%,80%,100%{opacity:.3;}40%{opacity:1;}}
</style>
""", unsafe_allow_html=True)

# ================= ENCABEZADO =================
st.markdown(f"""
<div class="header">
    <img src="data:image/jpeg;base64,{bot_pic64}">
    <h2 style='margin:0;'>Jerry</h2>
    <span style="opacity:.7;">Tu asistente personal</span>
</div>
""", unsafe_allow_html=True)

# ================= CONTENEDOR FIJO PARA "JERRY ESTÁ ESCRIBIENDO" =================
typing_top = st.empty()

# ================= SISTEMA DEL CHAT =================
if "messages" not in st.session_state:
    st.session_state.messages = []

chat = st.container()
with chat:
    st.markdown("<div class='chat-scroll' id='chatbox'>", unsafe_allow_html=True)

    for m in st.session_state.messages:
        if m["role"]=="user":
            st.markdown(f"""
            <div class='msg' style='justify-content:right;'>
                <div class='user-msg'>{m['content']}</div>
                <img src="data:image/jpeg;base64,{user_pic64}" style="width:38px;height:38px;border-radius:50%;margin-left:7px;">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='msg'>
                <img src="data:image/jpeg;base64,{bot_pic64}" style="width:38px;height:38px;border-radius:50%;margin-right:7px;">
                <div class='bot-msg'>{m['content']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= INPUT + BOTÓN =================
col1,col2 = st.columns([8,2])
with col1:
    user = st.text_input("", placeholder="Escribe aquí...", key="input", label_visibility="collapsed")
with col2:
    send = st.button("Enviar", use_container_width=True)

# ================= PROCESAR MENSAJE + TYPING INDICATOR =================
def procesar():
    st.session_state.messages.append({"role":"user","content":user})

    # 🔥 ⬆ TYPING EN LA PARTE SUPERIOR DEL CHAT ⬆ 🔥
    typing_top.markdown(f"""
    <div style='margin-bottom:10px;display:flex;justify-content:center;'>
        <div class='typing-box'>
            <img src="data:image/jpeg;base64,{bot_pic64}" style="width:28px;height:28px;border-radius:50%;">
            Jerry está escribiendo <div class='dot'></div><div class='dot'></div><div class='dot'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(1)
    reply = get_response(user)
    typing_top.empty()

    st.session_state.messages.append({"role":"bot","content":reply})
    st.rerun()

if send and user.strip():
    procesar()
