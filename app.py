import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Function to handle text-to-speech conversion
def text_to_speech(text, lg="es"):
    from gtts import gTTS
    import uuid
    
    result = str(uuid.uuid4())
    output_path = f"temp/{result}.mp3"
    tts = gTTS(text, lang=lg)
    tts.save(output_path)
    return result, text

# Streamlit page setup
st.set_page_config(page_title="Análisis de imagen", layout="centered", initial_sidebar_state="collapsed")
st.title("LectorManga")
with st.sidebar:
    st.subheader("¡Hola! En esta app podrás obtener descripciones detalladas de la página manga que requieras.")

# API Key input
ke = st.text_input('Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']

# Initialize OpenAI client with the API key
if api_key:
    client = OpenAI(api_key=api_key)

# File uploader allows user to add their own image
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the uploaded image
    with st.expander("Imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

# Toggle for showing additional details input
show_details = st.checkbox("Adicionar detalles sobre la imagen", value=False)

if show_details:
    # Text input for additional details about the image
    additional_details = st.text_area(
        "Adiciona contexto de la imagen aquí:",
        disabled=not show_details
    )

# Button to trigger the analysis
analyze_button = st.button("Analizar la imagen")

# Analyze image
if uploaded_file is not None and api_key and analyze_button:

    with st.spinner("Analizando..."):
        # Encode the image
        base64_image = encode_image(uploaded_file)
    
        # Optimized prompt for additional clarity and detail
        prompt_text = ('Eres un lector de manga, un estilo de cómic que se lee de derecha a izquierda. '
                       'Estás para asistir a los usuarios que tengan dificultades para interpretar imágenes '
                       'o cómics. Analizarás cada panel y le darás una descripción detallada al usuario. '
                       'Separa sus diálogos en líneas organizadas como si fuera un guion.')

        prompt_text += "\n\nDescribe lo que ves en la imagen en español."

        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional proporcionado por el usuario:\n{additional_details}"
    
        # Make the request to the OpenAI API
        try:
            response = openai.Completion.create(
                model="gpt-4",
                prompt=prompt_text,
                max_tokens=300,
                n=1,
                stop=None,
                temperature=0.7,
            )

            text = response.choices[0].text.strip()
            st.write("Descripción de la imagen:")
            st.markdown(text)
            
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

# Add text-to-speech conversion
if st.button("Convertir a Audio"):
    if 'text' in locals() and text:
        result, output_text = text_to_speech(text)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("## Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Download link for the audio file
        with open(f"temp/{result}.mp3", "rb") as f:
            data = f.read()

        def get_binary_file_downloader_html(bin_file, file_label="File"):
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
            return href
        
        st.markdown(get_binary_file_downloader_html(f"temp/{result}.mp3", file_label="Archivo de Audio"), unsafe_allow_html=True)

# Warnings for user action required
if not uploaded_file and analyze_button:
    st.warning("Por favor, sube una imagen.")
if not api_key:
    st.warning("Por favor, ingresa tu API key.")
