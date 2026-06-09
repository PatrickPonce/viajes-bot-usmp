import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- IMPORTACIONES PARA RAG (LANGCHAIN + CHROMA) ---
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# --- 1. CONFIGURACIÓN INICIAL Y CREDENCIALES ---
load_dotenv()
# Langchain necesita la variable GOOGLE_API_KEY, así que la igualamos a tu llave
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY") 
client = genai.Client()

# --- 2. INICIALIZAR BASE DE DATOS RAG (En Caché) ---
# Usamos @st.cache_resource para que ChromaDB se cree solo una vez y no vuelva 
# a vectorizar los textos cada vez que recargas la página (ahorra tiempo y dinero)
@st.cache_resource
def iniciar_base_conocimiento():
    documentos = [
        Document(page_content="El paquete a Cusco cuesta $259 e incluye 4 días y 3 noches, visita a Machu Picchu y tren panorámico."),
        Document(page_content="El vuelo a Madrid directo cuesta $1,040 y sale todos los viernes a las 8:00 PM."),
        Document(page_content="Para viajar a Tampa desde Lima necesitas visa americana vigente. El paquete cuesta $523 e incluye auto alquilado."),
        Document(page_content="El paquete a Iquitos cuesta $300, incluye 3 días en un lodge en la selva, paseos en canoa y no requiere visa.")
    ]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return Chroma.from_documents(documents=documentos, embedding=embeddings, collection_name="catalogo_viajes_nm")

vectorstore = iniciar_base_conocimiento()

# --- 3. CONFIGURACIÓN DE PÁGINA Y CSS ---
st.set_page_config(page_title="NM Viajes - Home", layout="wide", initial_sidebar_state="expanded")

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

# --- 4. PANEL LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Panel de Control IA")
    temperatura = st.slider("Creatividad (Temperatura)", 0.0, 1.0, 0.2) # Bajamos la temperatura para que RAG sea más exacto
    modo = st.selectbox("Personalidad del Agente", ["Asesor Estándar", "Guía Extremo", "Agente VIP Lujo"])
    st.divider()
    if st.button("🗑️ Limpiar Historial"):
        if "chat_session" in st.session_state:
            del st.session_state.chat_session

if "current_modo" not in st.session_state:
    st.session_state.current_modo = modo
    st.session_state.current_temp = temperatura

if st.session_state.current_modo != modo or st.session_state.current_temp != temperatura:
    st.session_state.current_modo = modo
    st.session_state.current_temp = temperatura
    if "chat_session" in st.session_state:
        del st.session_state.chat_session

# --- 5. FONDO: WEB EXISTENTE ---
st.markdown("<div class='fake-header'>🔴 nmviajes</div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div class='fake-search'>
    <h2 style='color: #111827;'>Descubre tu próximo destino</h2>
</div>
""", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown("<div class='card'><h3>Cusco</h3><p>Paquete 4D/3N<br><b>Desde US$ 259</b></p></div>", unsafe_allow_html=True)
with c2: st.markdown("<div class='card'><h3>Madrid</h3><p>Vuelo Directo<br><b>Desde US$ 1,040</b></p></div>", unsafe_allow_html=True)
with c3: st.markdown("<div class='card'><h3>Tampa</h3><p>Vuelo + Auto<br><b>Desde US$ 523</b></p></div>", unsafe_allow_html=True)

# --- 6. CHATBOT FLOTANTE CON RAG ---
with st.popover("💬"):
    st.markdown(f"#### ✈️ {modo}")
    st.divider()
    
    if "chat_session" not in st.session_state:
        st.session_state.client = genai.Client()
        
        # INSTRUCCIÓN RAG: Le decimos explícitamente que use la información proporcionada
        regla_base = (
            " REGLA ESTRICTA: Eres un asesor de NM Viajes. Basa tus respuestas ÚNICAMENTE en la 'Información Interna' "
            "que se te proporcione. Si te preguntan el precio de un paquete que no está en la información interna, "
            "di que no tienes el precio exacto en este momento."
        )
        
        if modo == "Asesor Estándar": sys_prompt = "Eres amable y paciente. " + regla_base
        elif modo == "Guía Extremo": sys_prompt = "Usa jerga de mochileros, tutéalo y ten mucha energía. " + regla_base
        else: sys_prompt = "Eres muy formal y elegante. Trata de 'Usted'. " + regla_base
        
        configuracion = types.GenerateContentConfig(system_instruction=sys_prompt, temperature=temperatura)
        st.session_state.chat_session = st.session_state.client.chats.create(model='gemini-2.5-flash', config=configuracion)
        st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy tu asesor virtual de NM Viajes 🌴. ¿A dónde quieres viajar hoy?"}]
        
    chat_box = st.container(height=320, border=False)
    
    for msg in st.session_state.messages:
        with chat_box:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    if prompt := st.chat_input("Escribe tu duda aquí..."):
        
        # Guardar mensaje original del usuario en la UI
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_box:
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                # --- FILTRO DE SEGURIDAD (INPUT GUARDRAIL) ---
                palabras_prohibidas = ["contraseña", "hackear", "estafa", "ilegal", "robo"]
                if any(palabra in prompt.lower() for palabra in palabras_prohibidas):
                    st.warning("⚠️ Mensaje bloqueado por políticas de seguridad.")
                    texto_ia = "Lo siento, mi filtro de seguridad interno me impide procesar esa solicitud."
                    st.markdown(texto_ia)
                else:
                    try:
                        # --- MAGIA RAG: RECUPERACIÓN DE DATOS ---
                        # 1. Buscar en ChromaDB los documentos relevantes
                        resultados = vectorstore.similarity_search(prompt, k=2)
                        
                        # 2. Unir los resultados en un solo bloque de texto
                        contexto_encontrado = "\n".join([res.page_content for res in resultados])
                        
                        # 3. Construir un "Prompt Enriquecido" (Esto va a la IA, pero el usuario no lo ve)
                        prompt_enriquecido = f"""
                        INFORMACIÓN INTERNA DE NM VIAJES:
                        {contexto_encontrado}
                        
                        PREGUNTA DEL CLIENTE:
                        {prompt}
                        """
                        
                        # Enviamos el prompt enriquecido a Gemini
                        response = st.session_state.chat_session.send_message(prompt_enriquecido)
                        texto_ia = response.text
                        st.markdown(texto_ia)
                        
                    except Exception as e:
                        texto_ia = f"Error: {e}. Intenta recargar la página."
                        st.markdown(texto_ia)
        
        # Guardar respuesta de la IA en el historial visual
        st.session_state.messages.append({"role": "assistant", "content": texto_ia})