# ✈️ AI Concierge - NM Viajes

Un asistente virtual inteligente desarrollado con Python y Streamlit para la agencia de turismo NM Viajes. Este proyecto utiliza la API de Google Gemini para ofrecer atención al cliente 24/7, recomendar destinos y perfilar usuarios de forma dinámica.

## 🚀 Características Principales
* **Interfaz Gráfica (UI):** Diseño inmersivo simulando la web real de NM Viajes, incluyendo un widget flotante de chat.
* **Memoria de Sesión (State Management):** El bot es capaz de recordar el contexto de la conversación actual utilizando `st.session_state`.
* **Personalidades Dinámicas:** Un panel lateral (Sidebar) permite alterar el *System Prompt* y la Temperatura de la IA en tiempo real (Modo Estándar, Guía Extremo, Agente VIP).
* **Ciberseguridad Integrada:** Implementación de *Input Guardrails* para interceptar y bloquear palabras prohibidas antes de que la IA procese la solicitud.

## 🛠️ Tecnologías Utilizadas
* Python 3.x
* Streamlit
* API de Google Gemini (SDK `google-genai`)
* `python-dotenv` para la gestión segura de credenciales.

## ⚙️ Instalación y Ejecución
1. Clona este repositorio.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Crea un archivo `.env` en la raíz del proyecto y añade tu API Key: `GEMINI_API_KEY=tu_llave_aqui`
4. Ejecuta la aplicación: `streamlit run app.py`

python -m streamlit run app.py