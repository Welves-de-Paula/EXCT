import json

def load_labels_from_rule(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        regras = json.load(f)
    # Supondo que as regras tenham uma chave 'labels' com lista de nomes de colunas
    return set(regras.get('labels', []))

def identify_table_type(header, regras_produtos_path, regras_clientes_path):
    labels_produtos = load_labels_from_rule(regras_produtos_path)
    labels_clientes = load_labels_from_rule(regras_clientes_path)
    header_set = set(header)

    match_produtos = len(header_set & labels_produtos)
    match_clientes = len(header_set & labels_clientes)

    if match_produtos > match_clientes and match_produtos > 0:
        return "produtos"
    elif match_clientes > match_produtos and match_clientes > 0:
        return "clientes"
    else:
        return "desconhecido"

# Exemplo de uso:
# header = ['nome', 'preco', 'quantidade']
# tipo = identify_table_type(header, 'regras_produtos.json', 'regras_clientes.json')
# print(tipo)
