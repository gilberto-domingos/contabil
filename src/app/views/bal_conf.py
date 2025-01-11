import streamlit as st
from openpyxl import load_workbook
from pathlib import Path
import pandas as pd
import os


def show():

    st.subheader("Conferindo Balanceador")

    # Obtém o diretório onde o script está sendo executado
    current_dir = Path(__file__).resolve().parent

    # Caminho correto para o arquivo balanco.xlsx
    file_path = current_dir.parents[1] / 'balance' / 'balanco.xlsx'

    try:
        file = load_workbook(file_path)
        st.subheader(file.sheetnames)
    except FileNotFoundError as e:
        st.write(f"Erro ao abrir o arquivo: {e}")


if __name__ == "__main__":
    show()
