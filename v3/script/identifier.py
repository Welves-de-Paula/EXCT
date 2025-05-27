from rules.customer import RULES as CUSTOMER_RULES
from rules.product import RULES as PRODUCT_RULES


def identify_table_type(excel_data):
    headers = excel_data['headers']
    # Cria pares (key, column) dos headers lidos
    header_pairs = set((h['key'], h['column']) for h in headers)

    # Cria pares (key, column) das regras
    customer_pairs = set((r['key'], r['column']) for r in CUSTOMER_RULES)
    product_pairs = set((r['key'], r['column']) for r in PRODUCT_RULES)

    # Diferenças detalhadas
    customer_missing = customer_pairs - header_pairs
    customer_extra = header_pairs - customer_pairs
    product_missing = product_pairs - header_pairs
    product_extra = header_pairs - product_pairs

    if not customer_missing and not customer_extra:
        return 'CUSTOMER'
    elif not product_missing and not product_extra:
        return 'PRODUCT'
    else:
        print('Diferenças para CUSTOMER:')
        print('Faltando nos headers:', customer_missing)
        print('Sobrando nos headers:', customer_extra)
        print('Diferenças para PRODUCT:')
        print('Faltando nos headers:', product_missing)
        print('Sobrando nos headers:', product_extra)
        return 'UNKNOWN'
