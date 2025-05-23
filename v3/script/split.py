import os
import pandas as pd
from openpyxl import load_workbook

def split_excel(filepath, output_dir, linhas_por_parte=1000, manter_cabecalho=True, manter_formatacao=True):
    """
    Divide um arquivo Excel em partes menores.
    filepath: caminho do arquivo de origem
    output_dir: diretório de saída
    linhas_por_parte: número de linhas por parte
    manter_cabecalho: se True, mantém o cabeçalho em cada parte
    manter_formatacao: se True, tenta manter a formatação (apenas para .xlsx)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df = pd.read_excel(filepath)
    total_linhas = len(df)
    partes = (total_linhas // linhas_por_parte) + (1 if total_linhas % linhas_por_parte else 0)
    arquivos_gerados = []
    for i in range(partes):
        inicio = i * linhas_por_parte
        fim = inicio + linhas_por_parte
        parte_df = df.iloc[inicio:fim]
        nome_base = os.path.splitext(os.path.basename(filepath))[0]
        nome_saida = f"{nome_base}_{i+1}.xlsx"
        caminho_saida = os.path.join(output_dir, nome_saida)
        if manter_cabecalho:
            parte_df.to_excel(caminho_saida, index=False)
        else:
            parte_df.to_excel(caminho_saida, index=False, header=False)
        arquivos_gerados.append(caminho_saida)
    return arquivos_gerados
