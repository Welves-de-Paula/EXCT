# -*- coding: utf-8 -*-
"""
Arquivo principal do Assistente de Importação de Arquivos Excel (.xlsx)
Responsável por inicializar a aplicação e importar as classes principais.
"""

appTitle = "Assistente de Importação"

# Importações das classes (a serem implementadas nos respectivos módulos)
# from gui import GUI
# from manipulador_arquivos import ManipuladorArquivos
# from validador import Validador
# from divisor import Divisor
# from salvador import Salvador

from ui import start
from ui import home
from ui import incompatible


from script.reading import read_excel
from ui.home import abrir_home_com_dados
from ui.incompatible import exibir_mensagem_incompativel
from script.identifier import identify_table_type
import os
import shutil
import logging

def limpar_data_dir():
    # Fecha todos os handlers do logging para liberar o arquivo de log
    logging.shutdown()
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    if os.path.exists(data_dir):
        for nome_arquivo in os.listdir(data_dir):
            caminho_arquivo = os.path.join(data_dir, nome_arquivo)
            try:
                if os.path.isfile(caminho_arquivo) or os.path.islink(caminho_arquivo):
                    os.unlink(caminho_arquivo)
                elif os.path.isdir(caminho_arquivo):
                    shutil.rmtree(caminho_arquivo)
            except Exception as e:
                print(f"Erro ao remover {caminho_arquivo}: {e}")

def main():
    filepath = start.main()
    if filepath:
        excel_data = read_excel(filepath)
        tipo = identify_table_type(excel_data)
        if tipo == 'desconhecido':
            exibir_mensagem_incompativel()
            return
        elif tipo in ('customer', 'product'):
            abrir_home_com_dados(excel_data)
    limpar_data_dir()

if __name__ == "__main__":
    main()

