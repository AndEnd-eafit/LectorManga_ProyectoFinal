import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from gtts import gTTS
from PIL import Image

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")


st.set_page_config(page_title="Analisis de imagen", layout="centered", initial_sidebar_state="collapsed")
# Streamlit page setup
st.title("LectorManga")
with st.sidebar:
    st.subheader("¡Hola! En esta app podrás obtener descripciones detalladas de la página manga que requieras.")

ke = st.text_input('Ingresa tu Clave', type="password")
os.environ['OPENAI_API_KEY'] = ke

# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# File uploader allows user to add their own image
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the uploaded image
    with st.expander("Imagen subida", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

# Toggle for showing additional details input
show_details = st.checkbox("Añadir detalles sobre la imagen", value=False)

if show_details:
    # Text input for additional details about the image, shown only if toggle is True
    additional_details = st.text_area(
        "Añade contexto de la imagen aquí:",
        disabled=not show_details
    )

# Button to trigger the analysis
analyze_button = st.button("Analizar la imagen")

# Check if an image has been uploaded, if the API key is available, and if the button has been pressed
if uploaded_file is not None and api_key and analyze_button:

    with st.spinner("Analizando..."):
        # Encode the image
        base64_image = encode_image(uploaded_file)
    
        # Optimized prompt for additional clarity and detail
        prompt_text = (
            "Eres un lector de manga, un estilo de cómic que se lee de derecha a izquierda. "
            "Estás aquí para asistir a los usuarios que tengan dificultades para interpretar imágenes o cómics. "
            "Analiza cada panel y proporciona una descripción detallada. "
            "Ejemplo: - Mira, Pablo - dice Juan mientras observa intensamente a Pablo, quien responde - No hay nada que puedas hacer. -"
        )
    
        if show_details and additional_details:
            prompt_text += (
                f"\n\nContexto adicional proporcionado por el usuario:\n{additional_details}"
            )
    
        # Make the request to the OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt_text}],
                max_tokens=300,
            )
            
            # Get the generated text
            analysis_result = response.choices[0].message["content"]
            st.markdown("### Resultado del análisis:")
            st.write(analysis_result)
            
            # Convert the result to audio
            st.markdown("### Escuchar resultado:")
            tts = gTTS(text=analysis_result, lang="es")
            audio_file = "output.mp3"
            tts.save(audio_file)
            
            # Play the audio
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
            
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
else:
    # Warnings for user action required
    if not uploaded_file and analyze_button:
        st.warning("Por favor, sube una imagen.")
    if not api_key:
        st.warning("Por favor, ingresa tu API key.")
