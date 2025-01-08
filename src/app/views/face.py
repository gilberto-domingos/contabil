import streamlit as st
from src.app.views.face_create import start_server
from src.app.views.face_login import login_face


def show():
    st.title("Sistema de Reconhecimento Facial")

    menu = ["Registrar", "Login"]
    choice = st.sidebar.selectbox("Reconhecimento facial", menu)

    if choice == "Registrar":
        start_server()
    elif choice == "Login":
        login_face()
