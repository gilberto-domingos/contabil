import streamlit as st


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("css/sys.css")


def show():
    st.title("Sistema")
    st.write("conteúdo pagina sistema")
