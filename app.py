import os
import streamlit as st
import base64
import openai
from PIL import Image

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Configuración de la página
st.set_page_config(page_title="LectorManga", layout="centered", initial_sidebar_state="collapsed")

# Streamlit page setup
st.title("LectorManga")
with st.sidebar:
    st.subheader("¡Hola! en está pagina podrás subir paginas de manga y te lo describira sin problema.")
    st.subheader("Tambien lee en voz alta.")
    
# Entrada de la clave API
ke = st.text_input('Ingresa tu Clave de API', type="password")
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ.get('OPENAI_API_KEY')

# Subida de archivo de imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Mostrar la imagen cargada
    with st.expander("Imagen subida", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

# Opción para añadir contexto adicional
show_details = st.checkbox("Agregar detalles sobre la imagen", value=False)
additional_details = ""
if show_details:
    additional_details = st.text_area("Añade contexto adicional aquí:")

# Botón para analizar la imagen
if st.button("Analizar la imagen"):
    if not uploaded_file:
        st.warning("Por favor, sube una imagen para analizar.")
    elif not api_key:
        st.warning("Por favor, ingresa tu clave de API.")
    else:
        with st.spinner("Analizando la imagen..."):
            try:
                # Codificar la imagen en base64
                base64_image = encode_image(uploaded_file)

                # Crear el prompt detallado
                prompt_text = """
                Eres un lector ávido de manga.
                Tu tarea es analizar la siguiente imagen, que debe leerse de derecha a izquierda.
                Proporciona un análisis detallado que incluya:
                1. Descripción de los personajes presentes.
                2. Transcripción de los diálogos en los globos de texto, indicando quién los dice.
                3. Explicación del significado de los paneles clave.
                Responde en español y usa un formato claro y estructurado en markdown.
                """
                if additional_details:
                    prompt_text += f"\n\nDetalles adicionales proporcionados por el usuario:\n{additional_details}"

                # Llamada a la API de OpenAI
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un experto en análisis de imágenes de manga."},
                        {"role": "user", "content": prompt_text},
                        {"role": "user", "content": f"Imagen en base64: data:image/jpeg;base64,{base64_image}"}
                    ],
                    max_tokens=1000,
                    temperature=0.7,
                )

                # Obtener la respuesta
                analysis_text = response["choices"][0]["message"]["content"]

                # Mostrar el análisis en la app
                st.success("Análisis completado:")
                st.markdown(analysis_text)

            except Exception as e:
                st.error(f"Ocurrió un error al analizar la imagen: {e}")
