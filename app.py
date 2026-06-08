import streamlit as st
import time
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- 1. CONFIGURACIÓN DE IA ---
load_dotenv()
client = genai.Client()

# --- 2. CONFIGURACIÓN DE PÁGINA Y CSS ---
st.set_page_config(page_title="NM Viajes - Home", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .fake-header { color: #E3001B; font-weight: bold; font-size: 24px; margin-bottom: 20px; }
    .fake-search { background-color: #f4f6f9; padding: 40px; border-radius: 10px; text-align: center; margin-bottom: 40px; border: 1px solid #e0e0e0; }
    .card { background: white; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee; }
    
    /* Botón flotante */
    [data-testid="stPopover"] { position: fixed !important; bottom: 30px !important; right: 30px !important; z-index: 9999 !important; }
    [data-testid="stPopover"] > button { border-radius: 50px !important; width: 65px !important; height: 65px !important; background-color: #E3001B !important; color: white !important; border: none !important; box-shadow: 0px 6px 20px rgba(0,0,0,0.3) !important; font-size: 28px !important; transition: transform 0.2s ease; }
    [data-testid="stPopover"] > button:hover { transform: scale(1.1); background-color: #cc0018 !important; }
    [data-testid="stPopoverBody"] { width: 380px !important; height: 550px !important; border-radius: 15px !important; box-shadow: 0px 10px 40px rgba(0,0,0,0.2) !important; padding: 1rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. FONDO: WEB EXISTENTE ---
st.markdown("<div class='fake-header'>🔴 nmviajes</div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div class='fake-search'>
    <h2 style='color: #111827;'>Descubre tu próximo destino</h2>
    <div style='background: white; padding: 15px; border-radius: 50px; display: inline-block; width: 60%; box-shadow: 0 2px 10px rgba(0,0,0,0.05);'>
        📍 Ida y vuelta &nbsp;&nbsp;|&nbsp;&nbsp; 🛫 Lima &nbsp;&nbsp;|&nbsp;&nbsp; 🛬 Destino &nbsp;&nbsp;|&nbsp;&nbsp; 📅 Fechas
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown("<div class='card'><h3>Cusco</h3><p>Paquete 4D/3N<br><b>Desde US$ 259</b></p></div>", unsafe_allow_html=True)
with c2: st.markdown("<div class='card'><h3>Madrid</h3><p>Vuelo Directo<br><b>Desde US$ 1,040</b></p></div>", unsafe_allow_html=True)
with c3: st.markdown("<div class='card'><h3>Tampa</h3><p>Vuelo + Auto<br><b>Desde US$ 523</b></p></div>", unsafe_allow_html=True)

# --- 4. CHATBOT FLOTANTE CON MEMORIA Y CLIENTE PERSISTENTE ---
with st.popover("💬"):
    st.markdown("#### ✈️ AI Concierge")
    st.divider()
    
    # Verificamos si la sesión ya existe, si no, creamos todo desde cero
    if "chat_session" not in st.session_state:
        # Re-inicializamos el cliente aquí para asegurar que esté abierto
        st.session_state.client = genai.Client()
        
        # 1. Creamos la personalidad con LIMITACIÓN DE DOMINIO AFINADA
        configuracion = types.GenerateContentConfig(
            system_instruction=(
                "Eres un asesor de viajes experto, amable y persuasivo de la agencia peruana NM Viajes. "
                "Tu misión exclusiva es ayudar a planificar vacaciones, vender vuelos y paquetes turísticos. "
                "REGLA ESTRICTA: Si el usuario te pregunta sobre temas ajenos (como matemáticas, programación, cocina, deportes, etc.), "
                "debes negarte educadamente diciendo: 'Lo siento, como asesor de NM Viajes solo puedo ayudarte a planear tu próxima gran aventura. ✈️'. "
                "EXCEPCIÓN: Sí tienes permitido saludar, mantener los modales y responder preguntas sobre el historial o el contexto de esta misma conversación."
            )
        )
        
        st.session_state.chat_session = st.session_state.client.chats.create(
            model='gemini-2.5-flash', 
            config=configuracion
        )
        st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy tu asesor virtual de NM Viajes 🌴. ¿A dónde quieres viajar hoy?"}]
        
    chat_box = st.container(height=320, border=False)
    
    # Dibujar historial
    for msg in st.session_state.messages:
        with chat_box:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    # Capturar nueva interacción
    if prompt := st.chat_input("Escribe tu duda aquí..."):
        
        # Guardar en memoria y mostrar pregunta
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_box:
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Procesar con la IA
            with st.chat_message("assistant"):
                try:
                    # Usamos el chat_session que ya definimos arriba
                    response = st.session_state.chat_session.send_message(prompt)
                    texto_ia = response.text
                except Exception as e:
                    texto_ia = f"Error: {e}. Intenta recargar la página."

                st.markdown(texto_ia)
        
        # Guardar respuesta en la memoria de la sesión
        st.session_state.messages.append({"role": "assistant", "content": texto_ia})