import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image
from gtts import gTTS
import time
import glob

# Custom CSS for fonts
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400&family=Lexend:wght@600&display=swap');
    .title-font {
        font-family: 'Lexend', sans-serif;
        font-size: 36px;
    }
    .paragraph-font {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="LectorManga", layout="centered", initial_sidebar_state="collapsed")

# Title with custom font
st.markdown('<p class="title-font">LectorManga</p>', unsafe_allow_html=True)

# Sidebar setup
with st.sidebar:
    st.subheader("Este agente analiza imágenes y convierte texto a audio.")

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# API Key input
ke = st.text_input('Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']

# Initialize OpenAI client
if api_key:
    client = OpenAI(api_key=api_key)

# File uploader for image
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

# Optional details input
show_details = st.checkbox("Añadir detalles sobre la imagen")
if show_details:
    additional_details = st.text_area("Añade contexto aquí:")

# Analyze button
analyze_button = st.button("Analizar imagen")

if uploaded_file and api_key and analyze_button:
    with st.spinner("Analizando..."):
        try:
            base64_image = encode_image(uploaded_file)
            prompt_text = """Eres un lector ávido de manga. Analiza la imagen, describe los diálogos y personajes. Explica en español."""
            if show_details and additional_details:
                prompt_text += f"\n\nContexto adicional:\n{additional_details}"

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt_text,
                max_tokens=500
            )
            analysis = response["choices"][0]["text"]
            st.markdown("### Resultado del análisis:")
            st.write(analysis)

            # Text-to-speech functionality
            st.markdown("### Escucha el análisis:")
            if analysis:
                tts = gTTS(analysis, lang='es')
                audio_path = "temp/analysis_audio.mp3"
                tts.save(audio_path)
                audio_file = open(audio_path, "rb")
                st.audio(audio_file.read(), format="audio/mp3")

        except Exception as e:
            st.error(f"Error: {e}")

# Text-to-speech for custom text
st.markdown('<p class="title-font">Convierte tu texto a audio</p>', unsafe_allow_html=True)
text = st.text_area("Introduce el texto a convertir.")
languages = {
    "Español": 'es',
    "Inglés": 'en',
    "Ruso": 'ru',
    "Japonés": 'ja',
    "Italiano": 'it'
}
language_option = st.selectbox("Selecciona el idioma", list(languages.keys()))
lg = languages[language_option]

if st.button("Convertir texto a audio"):
    if text:
        try:
            tts = gTTS(text, lang=lg)
            audio_file_path = f"temp/{text[:20]}.mp3" if len(text) > 20 else "temp/audio.mp3"
            tts.save(audio_file_path)
            audio_file = open(audio_file_path, "rb")
            st.audio(audio_file.read(), format="audio/mp3")

            # Download link
            with open(audio_file_path, "rb") as f:
                data = f.read()
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(audio_file_path)}">Descargar audio</a>'
            st.markdown(href, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")
