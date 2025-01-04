import streamlit as st
from src.app.views.face_create import register_face
from src.app.views.face_login import login_face


def show():
    st.title("Sistema de Reconhecimento Facial")

    menu = ["Registrar", "Login"]
    choice = st.sidebar.selectbox("Reconhecimento facial", menu)

    if choice == "Registrar":
        register_face()
    elif choice == "Login":
        login_face()
