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

def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    my_file_name = text[:20] if len(text) > 20 else "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

# Convert text to audio
if st.button("Convertir a Audio"):
    if text:
        result, output_text = text_to_speech(text, lg)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Download link for the audio file
        with open(f"temp/{result}.mp3", "rb") as f:
            data = f.read()
        def get_binary_file_downloader_html(bin_file, file_label='File'):
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
            return href
        st.markdown(get_binary_file_downloader_html(f"temp/{result}.mp3", file_label="Audio File"), unsafe_allow_html=True)

# Function to remove old files
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    n_days = n * 86400
    for f in mp3_files:
        if os.stat(f).st_mtime < now - n_days:
            os.remove(f)
