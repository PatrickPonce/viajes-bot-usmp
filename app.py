import streamlit as st

# --- 1. CONFIGURACIÓN DE PÁGINA ---
# Configuramos el título y el ancho de la página
st.set_page_config(page_title="ViajesBot - Nuevo Mundo", page_icon="✈️", layout="wide")

# --- 2. BARRA LATERAL (SIDEBAR) ---
# Implementamos el menú de navegación y avisos de transparencia
with st.sidebar:
    st.title("MENÚ")
    st.button("💬 Asistente (Actual)", use_container_width=True, disabled=True)
    st.write("---")
    st.caption("Bot IA - Solo fines informativos")

# --- 3. GESTIÓN DE MEMORIA (SESSION STATE) ---
# Streamlit se recarga en cada interacción, usamos st.session_state para no perder el historial
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Saludo inicial del bot propuesto en el mockup
    saludo_inicial = "¡Hola! Soy el asistente virtual de Nuevo Mundo Viajes. Estoy aquí para ayudarte a encontrar el paquete turístico ideal. ¿A dónde te gustaría viajar?"
    st.session_state.messages.append({"role": "assistant", "content": saludo_inicial})

# --- 4. ÁREA CENTRAL DEL CHAT ---
st.header("Asistente Virtual 🟢 En línea")

# Mostrar los mensajes previos del historial en pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. ENTRADA DEL USUARIO Y RESPUESTA DE PRUEBA ---
# Barra inferior para escribir
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    
    # 5.1 Mostrar el mensaje del usuario en la app y guardarlo en memoria
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 5.2 Generar una respuesta falsa (Dummy) para probar la UI
    respuesta_falsa = "Hola, soy el bot de prueba. Tu interfaz funciona perfectamente, pero mi cerebro (Gemini) aún no está conectado. ¡Pásale el turno a Patrick!"
    
    # Mostrar la respuesta del bot en la app y guardarla en memoria
    with st.chat_message("assistant"):
        st.markdown(respuesta_falsa)
    st.session_state.messages.append({"role": "assistant", "content": respuesta_falsa})