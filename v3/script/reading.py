import os
import shutil
from openpyxl import load_workbook

 

def read_excel(filepath):
    """
    Lê um arquivo Excel (.xlsx) e retorna (headers, dados).
    headers: lista de strings (nomes das colunas)
    dados: lista de listas (linhas, cada linha é uma lista de strings)
    """
    ext = os.path.splitext(filepath)[1].lower()
    if ext != ".xlsx":
        raise ValueError("Arquivo não suportado. Por favor, utilize apenas arquivos .xlsx.")
    wb = load_workbook(filepath, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return [], []
    headers = [str(h) if h is not None else "" for h in rows[0]]
    data = [
        [str(cell) if cell is not None else "" for cell in row]
        for row in rows[1:]
    ]
    return headers, data
