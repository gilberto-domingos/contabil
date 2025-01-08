import streamlit as st
from src.app.views.face_create import start_http_server
from src.app.views.face_login import login_face
import threading


def show():
    st.title("Sistema de Reconhecimento Facial")

    menu = ["Registrar", "Login"]
    choice = st.sidebar.selectbox("Reconhecimento facial", menu)

    if choice == "Registrar":
        threading.Thread(target=start_http_server, daemon=True).start()
    elif choice == "Login":
        login_face()
