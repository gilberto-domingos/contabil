import streamlit as st


def capture_photo():
    st.write("Para capturar sua câmera, por favor, permita o acesso ao dispositivo de captura (webcam) no seu navegador.")

    photo = st.camera_input("Capturar imagem")

    if photo:
        st.image(photo, caption="Captured Photo", use_container_width=True)
        st.success("Imagem capturada com sucesso!")
    else:
        st.warning(
            "Aguardando a captura da sua imagem. Clique no botão para capturar com sua câmera.")


if __name__ == "__main__":
    capture_photo()
