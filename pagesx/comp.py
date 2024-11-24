import datetime
import streamlit as st


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("css/comp.css")


def show():
    st.title("Desenvolvimento de componentes")
    st.write("Desenvolvendo e testando componentes antes de usar no sistema")

    option_map = {
        0: ":material/add:",
        1: ":material/zoom_in:",
        2: ":material/zoom_out:",
        3: ":material/zoom_out_map:",
    }

    # Usando st.radio para criar uma seleção de opções
    selection = st.radio(
        "Ferramenta",
        options=list(option_map.keys()),  # Transforma as chaves em uma lista
        # Formatação do texto das opções
        format_func=lambda option: option_map[option],
    )
    st.write(
        "A opção selecionada foi: "
        f"{None if selection is None else option_map[selection]}"
    )

    # Dividindo a tela em 4 colunas
    col1, col2, col3, col4 = st.columns(4)

    if col1.button("Botão simples", use_container_width=True):
        col1.markdown("Você clicou no botão simples.")

    if col2.button("Botão de emoji", icon="😃", use_container_width=True):
        col2.markdown("Você clicou no botão de emoji.")

    if col3.button("Botão material", icon=":material/mood:", use_container_width=True):
        col3.markdown("Você clicou no botão material.")

    if col4.button("Botão customizado", icon="🔥", use_container_width=True):
        col4.markdown("Você clicou no botão customizado.")

    # Novas colunas para outros botões
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button('Botão 1'):
            st.write("Botão 1 clicado")
    with col2:
        if st.button('Botão 2'):
            st.write("Botão 2 clicado")
    with col3:
        if st.button('Botão 3'):
            st.write("Botão 3 clicado")
    with col4:
        if st.button('Botão 4'):
            st.write("Botão 4 clicado")

    # Criando mais colunas para links
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.link_button("Link 1", "https://docs.1")
    with col6:
        st.link_button("Link 2", "https://docs.2")
    with col7:
        st.link_button("Link 3", "https://docs.3")
    with col8:
        st.link_button("Link 4", "https://streamlit.4")

    today = datetime.datetime.now()
    next_year = today.year + 1
    jan_1 = datetime.date(next_year, 1, 1)
    dec_31 = datetime.date(next_year, 12, 31)

    d = st.date_input(
        "Selecione suas férias para o próximo ano",
        (jan_1, datetime.date(next_year, 1, 7)),
        jan_1,
        dec_31,
        format="DD.MM.YYYY",
    )

    d = st.date_input("Selecione a data do compromisso",
                      datetime.date(2019, 7, 6))
    st.write("A data selecionada foi:", d)

    # Definindo as opções para direção
    options = ["Norte", "Leste", "Sul", "Oeste"]

    # Usando st.multiselect para seleção múltipla
    selection = st.multiselect(
        "Direções", options
    )

    row1 = st.columns(3)
    row2 = st.columns(3)

    for col in row1 + row2:
        tile = col.container(height=120)
        tile.title(":balloon:")

    enable = st.checkbox("Ativar a sua câmera")
    picture = st.camera_input(
        "Abaixo clique para tirar a foto", disabled=not enable)

    if picture:
        st.image(picture)
