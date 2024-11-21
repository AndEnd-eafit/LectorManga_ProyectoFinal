import os
import streamlit as st
import base64
import openai
from PIL import Image
from gtts import gTTS
import time
import glob

# Configuración de la página (debe ir primero)
st.set_page_config(page_title="LectorManga", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS para fuentes
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

# Título principal
st.markdown('<p class="title-font">LectorManga</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.subheader("Este agente analiza el contenido de la imagen y responde tus preguntas.")
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

# Entrada de API Key
ke = st.text_input('Ingresa tu Clave de API')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ.get('OPENAI_API_KEY')

# Subir archivo de imagen
uploaded_file = st.file_uploader("Sube una imagen de manga", type=["jpg", "png", "jpeg"])

# Mostrar imagen subida
if uploaded_file:
    st.image(uploaded_file, caption="Imagen subida", use_column_width=True)

# Área para texto adicional
show_details = st.checkbox("Agregar detalles sobre la imagen")
if show_details:
    additional_details = st.text_area("Añade contexto adicional aquí:")

# Botón para analizar la imagen
if st.button("Analizar imagen"):
    if not uploaded_file:
        st.warning("Por favor, sube una imagen para analizar.")
    elif not api_key:
        st.warning("Por favor, ingresa tu clave de API.")
    else:
        st.success("Análisis completado (simulado).")

# Conversión de texto a audio
st.markdown('<p class="title-font">Conversión de Texto a Audio</p>', unsafe_allow_html=True)

# Entrada de texto
text = st.text_area("Escribe el texto que deseas convertir a audio:")

# Selección de idioma
languages = {
    "Español": 'es',
    "Inglés": 'en',
    "Ruso": 'ru',
    "Japonés": 'ja',
    "Italiano": 'it'
}
option_lang = st.selectbox("Selecciona el idioma", list(languages.keys()))
lg = languages[option_lang]

# Botón para convertir a audio
if st.button("Convertir a audio"):
    if text:
        tts = gTTS(text, lang=lg)
        audio_file = "temp/audio.mp3"
        tts.save(audio_file)
        with open(audio_file, "rb") as file:
            st.audio(file.read(), format="audio/mp3")
        st.success("Conversión a audio completada.")
    else:
        st.warning("Por favor, escribe algún texto para convertir.")

# Eliminar archivos temporales antiguos
if not os.path.exists("temp"):
    os.mkdir("temp")
else:
    now = time.time()
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < now - 7 * 86400:  # Más de 7 días
            os.remove(f)
