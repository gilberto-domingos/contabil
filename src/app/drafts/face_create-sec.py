import streamlit as st
import cv2
import numpy as np
import face_recognition
from src.database.face_database import Database


def process_image(image_data):
    """Processa a imagem capturada pelo st.camera_input."""
    try:
        img_array = np.array(bytearray(image_data.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return rgb_frame
    except Exception as e:
        st.error(f"Erro ao processar a imagem: {str(e)}")
        return None


def register_face():
    """
    Captura uma foto com WebRTC para registro do usuário no banco de dados.
    """
    st.header("Registrar Novo Usuário")
    username = st.text_input("Nome de Usuário")

    # Captura a imagem da câmera via WebRTC
    image = st.camera_input("Capture uma imagem da câmera")

    if st.button("Registrar") and username:
        if image:
            rgb_frame = process_image(image)
            if rgb_frame is not None:
                # Detectar e codificar a face
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_frame, face_locations
                )

                if face_encodings:
                    try:
                        face_encoding_bytes = face_encodings[0].tobytes()

                        # Salvar no banco de dados
                        db = Database()
                        db.connect()
                        db.insert_face(username, face_encoding_bytes)

                        st.success(
                            f"Usuário {username} registrado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao salvar no banco de dados: {str(e)}")
                else:
                    st.error(
                        "Nenhuma face detectada. Certifique-se de que está bem visível para a câmera."
                    )
            else:
                st.error("Erro ao processar a imagem.")
        else:
            st.error(
                "Nenhuma imagem capturada. Verifique se a câmera está funcionando.")
