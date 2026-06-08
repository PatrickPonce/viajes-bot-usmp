import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Configuración inicial
load_dotenv()
client = genai.Client()

# 2. Definimos las instrucciones del sistema
instrucciones = (
    "Eres un asesor de viajes experto, amable y persuasivo de la agencia NM Viajes. "
    "Tu objetivo es ayudar a planificar vacaciones. Responde de forma concisa y usa emojis."
)

configuracion = types.GenerateContentConfig(
    system_instruction=instrucciones
)

# 3. Iniciamos la sesión de chat
chat = client.chats.create(
    model='gemini-flash-latest', 
    config=configuracion
)

print("✈️ --- AI Concierge de NM Viajes Iniciado (Escribe 'salir' para terminar) ---")

# 4. El Bucle de Chat (Loop)
while True:
    # Entrada del usuario
    user_input = input("Tú: ")
    
    # Condición de salida
    if user_input.lower() in ["salir", "exit", "chau"]:
        print("Bot: ¡Buen viaje! Nos vemos pronto. 🌴")
        break
        
    # Envío del mensaje y recepción de respuesta
    try:
        response = chat.send_message(user_input)
        print(f"Bot: {response.text}")
        print("-" * 40)
        
        # --- AQUÍ EMPIEZA EL CÓDIGO DE DEBUG DE MEMORIA ---
        print("\n🧠 [MODO DEBUG] Historial actual enviado a Google:")
        for mensaje in chat.get_history():
            # Extraemos el texto de la estructura de la nueva librería
            texto = mensaje.parts[0].text if mensaje.parts else "Sin texto"
            # Imprimimos el rol y los primeros 50 caracteres para no saturar la consola
            print(f"   Rol: {mensaje.role} | Contenido: {texto[:50]}...") 
        print("----------------------------------------\n")
        # --- AQUÍ TERMINA EL CÓDIGO DE DEBUG ---

    except Exception as e:
        print(f"Error de conexión: {e}")