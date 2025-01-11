import streamlit as st
import pandas as pd
import os

# Caminho para salvar os arquivos
SAVE_PATH = "src/balance"
os.makedirs(SAVE_PATH, exist_ok=True)


def save_uploaded_file(uploaded_file):
    """Salva o arquivo enviado no diretório especificado."""
    try:
        file_path = os.path.join(SAVE_PATH, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Arquivo '{uploaded_file.name}' salvo com sucesso!")
        return file_path
    except Exception as e:
        st.error(f"Erro ao salvar o arquivo: {e}")
        return None


def load_file(file_path):
    """Carrega o arquivo enviado como DataFrame."""
    try:
        if file_path.endswith(".xlsx"):
            dataframe = pd.read_excel(file_path)
        elif file_path.endswith(".ods"):
            dataframe = pd.read_excel(file_path, engine="odf")
        else:
            raise ValueError("Formato de arquivo não suportado.")
        return dataframe
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None


def read_file(dataframe):
    """Lê o título do arquivo da primeira linha e exibe na interface."""
    try:
        title = dataframe.loc[0, 0]  # Primeira célula da primeira linha
        st.subheader(f"Título do Arquivo: {title}")
    except Exception as e:
        st.error(f"Erro ao ler o título do arquivo: {e}")


def display_uploaded_files():
    """Exibe os arquivos já salvos no diretório."""
    st.subheader("Arquivos salvos na pasta:")
    files = os.listdir(SAVE_PATH)
    if files:
        for file in files:
            st.write(f"- {file}")
    else:
        st.write("Nenhum arquivo salvo na pasta.")


def show():
    """Exibe a interface principal do aplicativo."""
    st.title("Uploads de Balanços")

    # Exibe os arquivos salvos
    display_uploaded_files()

    # Carrega o arquivo enviado pelo usuário
    uploaded_file = st.file_uploader(
        "Escolha um arquivo Excel (.xlsx) ou OpenDocument Spreadsheet (.ods)",
        type=["xlsx", "ods"]
    )

    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file)
        if file_path:
            dataframe = load_file(file_path)
            if dataframe is not None:
                # Lê e exibe o título do arquivo
                read_file(dataframe)

                # Exibe os dados carregados
                st.write("Visualização dos dados carregados:")
                st.dataframe(dataframe)

                # Exibe as dimensões do DataFrame
                st.write("Dimensões do DataFrame:")
                st.write(f"Linhas: {dataframe.shape[0]}, Colunas: {
                         dataframe.shape[1]}")
    else:
        st.info(
            "Por favor, envie um arquivo Excel (.xlsx) ou OpenDocument Spreadsheet (.ods)."
        )


# Chamando a função principal
if __name__ == "__main__":
    show()
