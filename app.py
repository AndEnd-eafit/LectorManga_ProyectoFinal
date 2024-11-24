import os
import streamlit as st
import base64
from PIL import Image
from gtts import gTTS
import openai

# Función para codificar la imagen a base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Función para convertir texto a audio
def text_to_speech(text, lang="es"):
    import uuid
    result = str(uuid.uuid4())
    output_path = f"temp/{result}.mp3"
    tts = gTTS(text, lang=lang)
    tts.save(output_path)
    return result, output_path

# Configuración de Streamlit
st.set_page_config(page_title="Análisis de imagen", layout="centered", initial_sidebar_state="collapsed")
st.title("Lector de Manga")
st.sidebar.subheader("¡Obtén descripciones detalladas de tu manga!")

# Ingresar API Key
ke = st.text_input('Ingresa tu Clave API')
if ke:
    openai.api_key = ke

# Subir archivo de imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

# Ingresar detalles adicionales
show_details = st.checkbox("Adicionar detalles sobre la imagen", value=False)
if show_details:
    additional_details = st.text_area("Añade contexto adicional:")

# Botón para analizar la imagen
if st.button("Analizar la imagen"):
    if not ke:
        st.error("Por favor ingresa tu API Key.")
    elif not uploaded_file:
        st.error("Por favor sube una imagen.")
    else:
        with st.spinner("Analizando la imagen..."):
            # Crear el prompt de la solicitud
            prompt = (
                "Eres un lector experto de manga. Describe en español lo que ves en la imagen de forma detallada. "
                "Incluye los diálogos en un formato de guion y analiza cada panel como si fueras un narrador de manga."
            )
            if show_details and additional_details:
                prompt += f"\n\nDetalles adicionales proporcionados: {additional_details}"

            # Solicitar la descripción a la API de OpenAI
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un asistente experto en descripciones de imágenes y análisis de paneles de manga."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                description = response.choices[0].message['content']
                st.subheader("Descripción Generada:")
                st.markdown(description)
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

# Botón para convertir la descripción a audio
if st.button("Convertir a Audio"):
    if 'description' in locals() and description:
        result, output_path = text_to_speech(description, lang="es")
        audio_file = open(output_path, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.download_button(
            label="Descargar el audio",
            data=audio_bytes,
            file_name="descripcion.mp3",
            mime="audio/mp3"
        )
    else:
        st.error("No hay descripción generada para convertir.")
