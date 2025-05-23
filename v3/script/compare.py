import re
from datetime import datetime
import pandas as pd
from script.reading import read_excel

def validar_nome(nome):
    if not nome or not (3 <= len(nome) <= 50):
        return False, "NOME deve ter entre 3 e 50 caracteres e ser obrigatório."
    return True, ""

def validar_cpf(cpf, cpfs_existentes=None):
    if not cpf:
        return True, ""
    if not re.fullmatch(r"\d{11}", cpf):
        return False, "CPF deve conter 11 dígitos."
    if cpfs_existentes and cpf in cpfs_existentes:
        return False, "CPF deve ser único."
    return True, ""

def validar_cnpj(cnpj, cnpjs_existentes=None):
    if not cnpj:
        return True, ""
    if not re.fullmatch(r"\d{14}", cnpj):
        return False, "CNPJ deve conter 14 dígitos."
    if cnpjs_existentes and cnpj in cnpjs_existentes:
        return False, "CNPJ deve ser único."
    return True, ""

def sanitizar_email(email):
    return email.strip().lower() if email else ""

def validar_email(email):
    if not email:
        return True, ""
    email = sanitizar_email(email)
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "EMAIL inválido."
    return True, ""

def sanitizar_telefone(telefone):
    return re.sub(r"\D", "", telefone) if telefone else ""

def validar_telefone(telefone):
    if not telefone:
        return True, ""
    telefone = sanitizar_telefone(telefone)
    if len(telefone) < 8 or len(telefone) > 15:
        return False, "TELEFONE deve ter entre 8 e 15 dígitos."
    return True, ""

def validar_whatsapp(whatsapp):
    return validar_telefone(whatsapp)

def validar_ativo(ativo):
    valores_permitidos = {"S", "N", "SIM", "NÃO", "1", "0"}
    if ativo is None or ativo == "":
        return True, ""  # padrão será tratado externamente
    if str(ativo).upper() not in valores_permitidos:
        return False, "ATIVO deve ser um dos valores permitidos: S, N, SIM, NÃO, 1, 0."
    return True, ""

def validar_data_nascimento(data):
    if not data:
        return True, ""
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True, ""
    except ValueError:
        return False, "DATA DE NASCIMENTO deve estar no formato dd/mm/aaaa."

def validar_tamanho_campo(valor, tamanho_max, campo_nome):
    if valor and len(str(valor)) > tamanho_max:
        return False, f"{campo_nome} excede o tamanho máximo de {tamanho_max} caracteres."
    return True, ""

def compare_data(file1, file2):
    # Lê os dois arquivos Excel
    headers1, data1 = read_excel(file1)
    headers2, data2 = read_excel(file2)
    df1 = pd.DataFrame(data1, columns=headers1)
    df2 = pd.DataFrame(data2, columns=headers2)
    # Interseção de colunas
    common_cols = list(set(df1.columns) & set(df2.columns))
    if not common_cols:
        return [], [], []
    # Dados duplicados
    duplicados = pd.merge(df1, df2, on=common_cols, how='inner')
    # Dados exclusivos
    exclusivos1 = pd.merge(df1, df2, on=common_cols, how='left', indicator=True)
    exclusivos1 = exclusivos1[exclusivos1['_merge'] == 'left_only'].drop('_merge', axis=1)
    exclusivos2 = pd.merge(df2, df1, on=common_cols, how='left', indicator=True)
    exclusivos2 = exclusivos2[exclusivos2['_merge'] == 'left_only'].drop('_merge', axis=1)
    return duplicados.values.tolist(), exclusivos1.values.tolist(), exclusivos2.values.tolist()