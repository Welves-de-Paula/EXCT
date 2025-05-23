import re

from rules.customer import RULES as CUSTOMER_RULES
from rules.product import RULES as PRODUCT_RULES


def normalize_header(header):
    """
    Normaliza o nome do header para snake_case.
    """
    header = header.strip().lower()
    header = re.sub(r"[áàãâä]", "a", header)
    header = re.sub(r"[éèêë]", "e", header)
    header = re.sub(r"[íìîï]", "i", header)
    header = re.sub(r"[óòõôö]", "o", header)
    header = re.sub(r"[úùûü]", "u", header)
    header = re.sub(r"[ç]", "c", header)
    header = re.sub(r"[^a-z0-9]+", "_", header)
    header = re.sub(r"_+", "_", header)
    header = header.strip("_")
    return header

def map_rules(rules):
    """
    Mapeia as regras de validação para um formato específico.
    """
    mapped_rules = []
    for rule in rules:
        mapped_rule = {
            'name':   rule["label"],
            'value':  normalize_header(rule["label"]), 
            'column': rule["column"],  
        }
        mapped_rules.append(mapped_rule)
    return mapped_rules


def identify_table_type(excel_data):
    headers = excel_data['headers']
    # Extrai os pares (column, value) dos headers lidos
    file_columns = [(h['column'], h['value']) for h in headers]
    # Regras clientes
    customer_rules = map_rules(CUSTOMER_RULES)
    customer_columns = [(r['column'], r['value']) for r in customer_rules]
    is_customer = file_columns == customer_columns
    # Regras produtos
    product_rules = map_rules(PRODUCT_RULES)
    product_columns = [(r['column'], r['value']) for r in product_rules]
    is_product = file_columns == product_columns
    if is_customer:
        return 'customer'
    elif is_product:
        return 'product'
    else:
        return 'desconhecido'


# Exemplo de uso:
# header = ['nome', 'preco', 'quantidade']
# tipo = identify_table_type(header, 'regras_produtos.json', 'regras_clientes.json')
# print(tipo)
