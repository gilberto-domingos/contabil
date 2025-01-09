import streamlit as st


def capture_photo():
    st.write("Para capturar sua câmera, por favor, permita o acesso ao dispositivo de captura (webcam) no seu navegador.")

    with st.expander("Dúvidas sobre o acesso à câmera?"):
        st.write("### Como permitir o acesso à câmera:")
        st.write(
            "1. No Google Chrome: Clique no ícone de cadeado na barra de endereços e selecione 'Permitir' em 'Câmera'.")
        st.write(
            "2. No Firefox: Clique no ícone de cadeado na barra de endereços e selecione 'Permitir' em 'Câmera'.")
        st.write(
            "3. Em outros navegadores: Verifique a documentação de como permitir o acesso à câmera.")

    photo = st.camera_input("Caputar sua imagem")

    if photo:
        st.image(photo, caption="Captured Photo", use_container_width=True)
        st.success("Imagem capturada com sucesso!")
    else:
        st.warning(
            "Aguardando a captura da sua imagem. Clique no botão para capturar com sua câmera.")


if __name__ == "__main__":
    capture_photo()
