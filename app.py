import os
import streamlit as st
from PIL import Image
import base64
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import openai
import pytesseract
import io

# Configuración de pytesseract (especifica la ruta si es necesario)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Cambia esto según tu instalación

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400&family=Lexend:wght@600&display=swap');
    h1, h2, h3 { font-family: 'Lexend', sans-serif; }
    p, div, label, span, input, textarea { font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Título y subtítulo de la aplicación
st.title('LectorManga')

# Barra lateral con información
with st.sidebar:
   st.subheader("Aquí podrás escuchar descripciones detalladas del manga que estás leyendo")

# Entrada para la clave de API de OpenAI
api_key = st.text_input('Ingresa tu Clave de API de OpenAI', type='password')
if api_key:
    openai.api_key = api_key  # Configurar la clave de API directamente con openai

# Carga de archivo de imagen
uploaded_image = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_image:
    try:
        # Intentar abrir la imagen para verificar que es válida
        image = Image.open(uploaded_image)
        with st.expander("Imagen", expanded=True):
            st.image(image, caption=uploaded_image.name, use_column_width=True)
    except Exception as e:
        st.error("El archivo cargado no es una imagen válida.")

# Añadir toggle para detalles adicionales
show_details = st.checkbox("Añadir detalles sobre la imagen", value=False)

if show_details:
    # Campo de texto para detalles adicionales
    additional_details = st.text_area("Añadir contexto de la imagen aquí:")

# Botón para análisis de imagen
if st.button("Analizar la imagen") and uploaded_image and api_key:
    with st.spinner("Analizando imagen..."):
        try:
            # Extraer texto de la imagen usando OCR
            extracted_text = pytesseract.image_to_string(image, lang="spa")
            
            # Crear un prompt para enviar a la API de OpenAI
            prompt_text = (
                "Eres un lector de manga, que son una serie de viñetas con dibujos y burbujas de texto que se lee de derecha a izquierda. "
                "Proporciona una explicación precisa en español sobre lo que está ocurriendo en las viñetas, y transcribe textualmente lo "
                "que se encuentra en las burbujas de diálogo.\n\n"
                f"Texto extraído de la imagen:\n{extracted_text}"
            )

            if show_details and additional_details:
                prompt_text += f"\n\nContexto adicional proporcionado:\n{additional_details}"

            # Solicitud a la API de OpenAI para analizar el texto extraído
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_text,
                max_tokens=500,
                temperature=0.5
            )
            st.markdown(response['choices'][0]['text'])
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

# Cargar archivo PDF
uploaded_pdf = st.file_uploader("Carga el archivo PDF", type="pdf")

if uploaded_pdf:
    try:
        # Extraer y procesar el texto del PDF
        pdf_reader = PdfReader(uploaded_pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Dividir el texto en chunks
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=20, length_function=len)
        chunks = text_splitter.split_text(text)

        # Crear embeddings a partir de los fragmentos del texto
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # Mostrar el campo de entrada para las preguntas
        st.subheader("Escribe lo que quieres saber sobre el documento")
        user_question = st.text_area(" ")

        if user_question:
            # Realizar búsqueda en la base de conocimientos
            docs = knowledge_base.similarity_search(user_question)

            # Cargar el modelo de lenguaje y realizar la cadena de preguntas y respuestas
            llm = OpenAI(api_key=api_key, model_name="gpt-4")
            chain = load_qa_chain(llm, chain_type="stuff")

            # Mostrar la respuesta
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
                st.write(response)
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el PDF: {e}")
