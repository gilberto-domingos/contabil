import streamlit as st
from streamlit_option_menu import option_menu
import pathlib
import psycopg2
from dotenv import load_dotenv
import os
import sys

project_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..'))

if project_path not in sys.path:
    sys.path.insert(0, project_path)

st.set_page_config(
    page_title="Mosimann",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def load_css(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, 'css', file_name)

    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("main.css")
st.markdown(
    """
    <style>
        button[data-testid="stBaseButton-header"] {
            display: none !important;
        }        
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
        button[data-testid="stBaseButton-headerNoPadding"] { 
            box-shadow: #ff4b4b;
        }

        button[data-testid="stBaseButton-headerNoPadding"]:hover {
             color: #ff4b4b;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '''
        <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 15px;">
            <div style="display: inline-flex; align-items: center; margin-bottom: 5px;">
                <span class="status-indicator" style="margin-right: 8px;"></span> 
                <span>Online</span>
            </div>
            <div style="display: inline-flex; align-items: center; margin-bottom: 5px;">
                <span class="status-indicator" style="margin-right: 8px;"></span> 
                <span>Itamar Mosimann</span>
            </div>
            <div style="display: inline-flex; align-items: center; margin-bottom: 5px;">
                <!-- Ícone de prédio com tamanho reduzido -->
                <i class="fas fa-building" style="margin-right: 8px; font-size: 13px;"></i>
                <span>Empresa : Mosimann LTDA</span>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    selected = option_menu(
        "Mosimann",
        [
            "Home",
            "Cadastro",
            "Empresas",
            "Método APLA",
            "Gráficos",
            "Upload arquivo",
            "Conferênciador",
            "Face login",
            "Imagens",

        ],
        icons=[
            "house",
            "file-earmark-text",
            "building",
            "file-earmark-text",
            "image",
            "cloud-arrow-up",
            "list-check",
            "instagram",
            "clipboard-check",
            # "bar-chart",
            # "file-earmark-text",
            # ""people",
            # ""chat",
            # "database",
            # "clipboard-check",
            # "building",
            # "sliders",
            # "book"
        ],
        menu_icon="cast",
        default_index=1,
    )


if selected == "Componentes":
    from src.app.views import comp
    comp.show()

elif selected == "Home":
    from src.app.views import homex
    homex.show()

elif selected == "Cadastro":
    cadastro_menu = option_menu(
        "Opções de Cadastro",
        [
            "Operadora",
            "Cliente",
            "Célula",
            "Funcionário",
            "Tipo de empresa",
            "Regime tributário",
        ],
        icons=[
            "building",
            "person-lines-fill",
            "box",
            "person-bounding-box",
            "building",
            "list-check",
        ],
        menu_icon="card-list",
        default_index=0,
        orientation="horizontal",
    )

    if cadastro_menu == "Operadora":
        from src.app.views import operator
        operator.show()

    if cadastro_menu == "Cliente":
        from src.app.views import customer
        customer.show()

    elif cadastro_menu == "Célula":
        from src.app.views import cell
        cell.show()

    elif cadastro_menu == "Funcionário":
        from src.app.views import employee
        employee.show()

    elif cadastro_menu == "Tipo de empresa":
        from src.app.views import type_company
        type_company.show()

    elif cadastro_menu == "Regime tributário":
        from src.app.views import tax_regime
        tax_regime.show()

elif selected == "Empresas":
    from src.app.views import companies
    companies.show()

elif selected == "Solicitações":
    from src.app.views import request
    request.show()

elif selected == "Método APLA":
    from src.app.views import apla
    apla.show()

elif selected == "Gráficos":
    from src.app.views import dashboards
    dashboards.show()

elif selected == "Imagens":
    from src.app.views import img
    img.show()

elif selected == "Upload arquivo":
    from src.app.views import up_files
    up_files.show()

elif selected == "Conferênciador":
    from src.app.views import conferencer
    conferencer.show()

elif selected == "Face login":
    from src.app.views import face
    face.show()


# Carrega as variáveis do arquivo .env
load_dotenv()

# Acessa as variáveis de ambiente
database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")
debug = os.getenv("DEBUG")

# Caso o SECRET_KEY tenha quebras de linha, o strip() pode ser usado para removê-las
secret_key = secret_key.strip() if secret_key else None
