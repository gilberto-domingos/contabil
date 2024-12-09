import streamlit as st


def apply_light_theme():
    primary_color = "#FF4B4B"
    background_color = "#ffffff"
    secondary_background_color = "#F0F2F6"
    text_color = "#31333F"
    font = "sans serif"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {background_color};
        }}
        .stSidebar {{
            background-color: {secondary_background_color};
        }}
        .stButton>button {{
            background-color: {primary_color};
            color: {text_color};
        }}
        body {{
            font-family: {font};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def apply_dark_theme():
    primary_color = "#e31b22"
    background_color = "#0E1117"
    secondary_background_color = "#262730"
    text_color = "#fafafa"
    font = "sans serif"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {background_color};
        }}
        .stSidebar {{
            background-color: {secondary_background_color};
        }}
        .stButton>button {{
            background-color: {primary_color};
            color: {text_color};
        }}
        body {{
            font-family: {font};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def show():
    # Inicializar o estado do tema
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Escuro"

    # Alternar o tema quando o toggle for alterado
    on = st.toggle("🌓 Claro/Escuro", key="theme_toggle",
                   value=st.session_state["theme"] == "Claro")

    if on:
        st.session_state["theme"] = "Claro"
    else:
        st.session_state["theme"] = "Escuro"

    # Aplicar o tema atual
    if st.session_state["theme"] == "Claro":
        apply_light_theme()
    else:
        apply_dark_theme()


if __name__ == "__main__":
    show()
