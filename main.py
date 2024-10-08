import streamlit as st
from streamlit_option_menu import option_menu

st.markdown(
    """
    <style>    
    [data-testid="stSidebar"] {
        border-right-style: solid;
        border-right-width: thin;
        border-right-color: #7d7d83;
    }    
    </style>
    """,
    unsafe_allow_html=True
)

# 1. Sidebar Menu
with st.sidebar:
    selected = option_menu("Mosimann",
                           ["Home", 'Sistema', 'Obrigações', 'Empresas', 'Lista de entregas', 'Gestão de Pessoas',
                            'Solicitações', 'Método APLA', 'Relatórios'],
                           icons=['house', 'sliders', 'clipboard-check', 'building', 'list-check', 'people', 'chat',
                                  'book', 'file-earmark-text'],
                           menu_icon="cast",
                           default_index=0)

if selected == "Home":
    st.title("Página Inicial")
elif selected == "Sistema":
    st.page_link("pages/sys.py")
elif selected == "Obrigações":
    st.title("Obrigações")
elif selected == "Empresas":
    st.title("Empresas")
# import pages.companies as companies
# companies.show()
elif selected == "Lista de entregas":
    st.title("Lista de Entregas")
elif selected == "Gestão de Pessoas":
    st.title("Gestão de Pessoas")
elif selected == "Solicitações":
    st.title("Solicitações")
elif selected == "Método APLA":
    st.title("Método APLA")
elif selected == "Relatórios":
    st.title("Relatórios")
