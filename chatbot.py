import os
from dotenv import load_dotenv
from google import genai

# 1. Cargar la API Key desde el archivo .env
load_dotenv()

# 2. Inicializar el cliente de la nueva librería
client = genai.Client()

# 3. Generar la respuesta con el modelo exacto de tu lista
try:
    print("⏳ Esperando respuesta de Gemini...")
    response = client.models.generate_content(
        model='gemini-flash-latest', 
        contents='Hola mundo, soy un estudiante de IA. ¿Quién eres tú?'
    )
    print("\n--- Respuesta del Chatbot ---") 
    print(response.text)
except Exception as e:
    print(f"\n❌ Ocurrió un error al conectar con la IA: {e}")