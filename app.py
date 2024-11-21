import os
import streamlit as st
import base64
import openai
from PIL import Image
from gtts import gTTS
import time
import glob

# Configuración de la página
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
additional_details = ""
if show_details:
    additional_details = st.text_area("Añade contexto adicional aquí:")

# Botón para analizar la imagen
if st.button("Analizar imagen"):
    if not uploaded_file:
        st.warning("Por favor, sube una imagen para analizar.")
    elif not api_key:
        st.warning("Por favor, ingresa tu clave de API.")
    else:
        with st.spinner("Analizando la imagen..."):
            # Simular análisis con OpenAI
            try:
                # Aquí se puede integrar la API de OpenAI para el análisis real
                analysis_text = (
                    "Esta es una descripción simulada de la imagen analizada. "
                    "El personaje parece estar sorprendido y dice: '¡No puedo creerlo!'."
                )
                
                # Agregar contexto adicional si existe
                if additional_details:
                    analysis_text += f" Contexto adicional proporcionado: {additional_details}"
                
                st.success("Análisis completado:")
                st.markdown(f"<p class='paragraph-font'>{analysis_text}</p>", unsafe_allow_html=True)

                # Convertir el análisis a audio automáticamente
                tts = gTTS(analysis_text, lang="es")
                audio_file = "temp/analysis_audio.mp3"
                tts.save(audio_file)

                # Reproducir el audio
                st.audio(audio_file, format="audio/mp3")
                st.success("Texto leído en voz alta automáticamente.")

            except Exception as e:
                st.error(f"Ocurrió un error al analizar la imagen: {e}")

# Eliminar archivos temporales antiguos
if not os.path.exists("temp"):
    os.mkdir("temp")
else:
    now = time.time()
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < now - 7 * 86400:  # Más de 7 días
            os.remove(f)
