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

def text_to_speech(text):
    import uuid
    result = str(uuid.uuid4())
    output_path = f"temp/{result}.mp3"
    tts = gTTS(text, lang="es")
    tts.save(output_path)
    return result, output_path

text = st.text_area("Ingrese el texto a escuchar.")

# Función para convertir texto a audio
def text_to_speech(text):
    import uuid
    # Crear el directorio "temp/" si no existe
    output_dir = "temp"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generar un nombre único para el archivo
    result = str(uuid.uuid4())
    output_path = os.path.join(output_dir, f"{result}.mp3")
    
    # Generar el archivo de audio en español
    tts = gTTS(text, lang="es")
    tts.save(output_path)
    return result, output_path



# Function to remove old files
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    n_days = n * 86400
    for f in mp3_files:
        if os.stat(f).st_mtime < now - n_days:
            os.remove(f)
