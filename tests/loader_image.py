import io
import streamlit as st
from PIL import Image

# Substituir imagem por uma carregada manualmente
image_file = st.file_uploader("Envie uma imagem")
if image_file:
    image = Image.open(io.BytesIO(image_file.read()))
    st.image(image, caption="Imagem carregada.")
