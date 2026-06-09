import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Cargar tu llave de Google (la que ya usas en tu app)
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# 2. Tu Base de Conocimiento (La "Materia Prima")
# Imagina que estos textos vienen de un PDF de catálogos de viaje
documentos = [
    Document(page_content="El paquete a Cusco cuesta $259 e incluye 4 días y 3 noches, visita a Machu Picchu y tren panorámico."),
    Document(page_content="El vuelo a Madrid directo cuesta $1,040 y sale todos los viernes a las 8:00 PM."),
    Document(page_content="Para viajar a Tampa desde Lima necesitas visa americana vigente. El paquete cuesta $523 e incluye auto alquilado."),
    Document(page_content="El paquete a Iquitos cuesta $300, incluye 3 días en un lodge en la selva, paseos en canoa y no requiere visa.")
]

# 3. El Traductor: Modelo de Embeddings
# Esto convierte el texto en números (vectores) para que ChromaDB los entienda
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

print("⏳ Vectorizando documentos y guardando en ChromaDB...")

# 4. Crear la Base de Datos Vectorial (ChromaDB)
# Aquí Langchain orquesta todo: toma los textos, los pasa por el modelo de embeddings y los guarda en Chroma
vectorstore = Chroma.from_documents(
    documents=documentos,
    embedding=embeddings,
    collection_name="catologo_viajes"
)

print("✅ ¡Base de datos lista!\n")

# 5. ¡Hacer una pregunta a la base de datos!
pregunta_usuario = "¿Qué destinos tengo que no superen los 600 dólares y qué incluyen?"

print(f"Buscando respuesta para: '{pregunta_usuario}'\n")

# Hacemos una búsqueda de similitud (Similarity Search)
resultados = vectorstore.similarity_search(pregunta_usuario, k=2) # k=2 trae los dos mejores resultados

print("--- RESULTADOS ENCONTRADOS EN LA BASE DE DATOS ---")
for i, res in enumerate(resultados):
    print(f"Resultado {i+1}: {res.page_content}")