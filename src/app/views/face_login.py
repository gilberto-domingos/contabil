import streamlit as st
import cv2
import numpy as np
import face_recognition
from src.database.face_database import Database


def login_face():
    """
    Captura uma foto para login por reconhecimento facial.
    """
    st.header("Login por Reconhecimento Facial")
    st.info("Olhe para a câmera e aguarde a identificação...")

    # Abrir a câmera via WebRTC
    image = st.camera_input("Captura da câmera")

    if image:
        # Processar imagem capturada
        img_array = np.array(bytearray(image.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectar e codificar face
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_frame, face_locations
        )

        if face_encodings:
            db = Database()
            db.connect()

            # Buscar faces conhecidas no banco
            known_faces = db.get_all_faces()

            for row in known_faces:
                username = row["username"]
                known_encoding = np.frombuffer(
                    row["face_encoding"], dtype=np.float64
                )

                match = face_recognition.compare_faces(
                    [known_encoding], face_encodings[0]
                )
                if match[0]:
                    st.success(f"Bem-vindo, {username}!")
                    return

            st.error("Face não reconhecida. Tente novamente.")
        else:
            st.error("Nenhuma face detectada. Tente novamente.")
