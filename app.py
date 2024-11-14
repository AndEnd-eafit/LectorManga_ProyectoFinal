import os
import streamlit as st
from PIL import Image
import base64
import openai

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400&family=Lexend:wght@600&display=swap');

    h1, h2, h3 {
        font-family: 'Lexend', sans-serif;
    }

    p, div, label, span, input, textarea {
        font-family: 'Inter', sans-serif;
    }
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

# Función para codificar la imagen en base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

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
        base64_image = encode_image(uploaded_image)

        # Prompt para la descripción de la imagen
        prompt_text = (
            "Eres un lector de manga, que son una serie de viñetas con dibujos y burbujas de texto que se lee de derecha a izquierda, "
            "debes proporcionar una explicación precisa en español sobre lo que está ocurriendo en las viñetas, y decir textualmente lo"
            "que se encuentra en las burbujas de diálogo"
        )

        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional proporcionado:\n{additional_details}"

        # Solicitud a la API de OpenAI para analizar la imagen
        try:
            response = openai.Image.create(
                prompt=prompt_text,
                image=f"data:image/jpeg;base64,{base64_image}",
                model="gpt-4-vision"
            )
            st.markdown(response['data'][0]['text'])
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

# Eliminamos la sección del código relacionada con el archivo PDF:
# Cualquier bloque de código relacionado con uploaded_pdf, extracción de texto, creación de embeddings, 
# búsqueda en FAISS, y la cadena de preguntas y respuestas ha sido removido.

