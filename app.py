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

# Título
st.markdown('<p class="title-font">LectorManga</p>', unsafe_allow_html=True)
