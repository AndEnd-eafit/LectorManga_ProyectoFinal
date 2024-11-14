import os
import streamlit as st
import base64
import openai
from PIL import Image

# Configuración de la página de Streamlit
st.set_page_config(page_title="Análisis de Imagen", layout="centered", initial_sidebar_state="collapsed")
st.title("Análisis de Imagen:🤖🏞️")

# Barra lateral con instrucciones
with st.sidebar:
    st.subheader("Este Agente analiza el contenido de la imagen y responde tus preguntas.")

# Entrada para la clave de la API
ke = st.text_input('Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke

# Inicialización de la clave de API
api_key = os.environ.get('OPENAI_API_KEY')

# Carga de archivo
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

# Mostrar imagen cargada
if uploaded_file:
    with st.expander("Imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

# Opción para agregar detalles adicionales
show_details = st.checkbox("Agregar detalles sobre la imagen", value=False)

if show_details:
    additional_details = st.text_area("Adiciona contexto de la imagen aquí:")

# Botón para analizar la imagen
analyze_button = st.button("Analiza la imagen")

# Verificar si se cumplen los requisitos para analizar la imagen
if uploaded_file and api_key and analyze_button:
    with st.spinner("Analizando..."):
        # Codificar la imagen a base64
        base64_image = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

        # Texto del prompt
        prompt_text = "Describe en español lo que ves en la imagen."
        
        if show_details and additional_details:
            prompt_text += f"\n\nDetalles adicionales proporcionados por el usuario:\n{additional_details}"

        try:
            # Llamada a la API de OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt_text}
                ],
                max_tokens=300,
            )
            # Mostrar la respuesta
            full_response = response['choices'][0]['message']['content']
            st.write(full_response)

        except Exception as e:
            st.error(f"Ha ocurrido un error: {e}")
else:
    # Mensajes de advertencia
    if not uploaded_file and analyze_button:
        st.warning("Por favor sube una imagen.")
    if not api_key:
        st.warning("Por favor ingresa tu clave de API.")
