import os
import streamlit as st
import base64
import openai
from PIL import Image

# Función para codificar la imagen en base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

st.set_page_config(page_title="LectorManga", layout="centered", initial_sidebar_state="collapsed")

# Configuración de la página
st.title("LectorManga")
with st.sidebar:
    st.subheader("Este Agente analiza el contenido de la imagen y responde tus preguntas.")

# Input para la clave API
api_key = st.text_input('Ingresa tu clave API')
os.environ['OPENAI_API_KEY'] = api_key

# Subida de archivo
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

# Mostrar la imagen si se sube
if uploaded_file:
    st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

# Toggle para mostrar detalles adicionales
show_details = st.checkbox("Añadir contexto adicional sobre la imagen")

if show_details:
    additional_details = st.text_area("Añade contexto adicional aquí:")

# Botón para analizar la imagen
analyze_button = st.button("Analizar la imagen")

# Analizar la imagen si se sube un archivo y hay una clave API
if analyze_button:
    if uploaded_file and api_key:
        with st.spinner("Analizando..."):
            try:
                # Codificar la imagen a base64
                base64_image = encode_image(uploaded_file)

                # Crear el prompt
                prompt_text = (
                    "Eres un lector ávido de manga. Tu tarea es examinar la siguiente imagen "
                    "en detalle y leerla de derecha a izquierda. Proporciona una explicación "
                    "detallada y precisa de lo que muestra la imagen. Incluye texto de los "
                    "globos de diálogo, identifica a los personajes y explica su contexto. "
                    "Usa español para tu respuesta."
                )

                if show_details and additional_details:
                    prompt_text += f"\n\nContexto adicional proporcionado por el usuario:\n{additional_details}"

                # Llamada a la API de OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un asistente que analiza imágenes de manga."},
                        {"role": "user", "content": prompt_text},
                    ],
                    max_tokens=500,
                )

                # Mostrar la respuesta
                st.markdown("### Respuesta:")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
    else:
        if not uploaded_file:
            st.warning("Por favor, sube una imagen.")
        if not api_key:
            st.warning("Por favor, ingresa tu clave API.")
