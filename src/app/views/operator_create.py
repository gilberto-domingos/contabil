import streamlit as st
from pathlib import Path
from src.database.operator_database import Database
import re


class Operator:
    def __init__(self, cod_operator, name_operator, cnpj_operator):
        self.cod_operator = cod_operator
        self.name_operator = name_operator
        self.cnpj_operator = cnpj_operator


def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def validate_cnpj(cnpj):
    """Valida se o CNPJ tem 14 dígitos numéricos e não contém caracteres especiais."""
    # Verifica se o CNPJ tem exatamente 14 dígitos numéricos
    if re.match(r'^\d{14}$', cnpj):
        return True
    return False


def show():
    css_path = Path("src/app/css/operator_create.css")
    load_css(css_path)

    db = Database()

    st.subheader('Cadastro de operadoras')

    # Campos de entrada para o formulário
    cod_operator = st.text_input("Código:", max_chars=5)
    cnpj_operator = st.text_input("CNPJ (somente números):", max_chars=14)
    name_operator = st.text_input("Nome da operadora:")

    # Validação do CNPJ
    cnpj_valid = True
    if cnpj_operator:
        if len(cnpj_operator) > 14:
            cnpj_operator = cnpj_operator[:14]
            st.warning("O CNPJ foi truncado para 14 dígitos.")

        if len(cnpj_operator) != 14:
            st.error("O CNPJ deve conter exatamente 14 números.")
            cnpj_valid = False
        elif not cnpj_operator.isdigit():
            st.error("Digite somente números no campo CNPJ.")
            cnpj_valid = False
        elif not validate_cnpj(cnpj_operator):
            st.error(
                "O CNPJ deve conter exatamente 14 números, sem caracteres especiais.")
            cnpj_valid = False

    # Ao clicar no botão "Salvar"
    if st.button("Salvar"):
        if not cod_operator or not cnpj_operator or not name_operator:
            st.error("Todos os campos são obrigatórios.")
        elif not cnpj_valid:
            st.error("Corrija os erros no CNPJ antes de salvar.")
        else:
            # Criar o objeto Operadora
            operator_obj = Operator(cod_operator, name_operator, cnpj_operator)

            # Inserir no banco de dados
            try:
                db.insert_operator(
                    operator_obj.cod_operator,
                    operator_obj.name_operator,
                    operator_obj.cnpj_operator
                )
                st.success("Operadora salva com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar no banco de dados: {e}")


if __name__ == "__main__":
    show()
