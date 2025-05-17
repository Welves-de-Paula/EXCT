RULES = [
    {
        "column": "A",
        "label": "CÓDIGO",
        "name": "code",
        "rules": "nullable"
    },
    {
        "column": "B",
        "label": "CÓDIGO DE BARRAS",
        "name": "gtin",
        "rules": "nullable|unique|digits:13"
    },
    {
        "column": "C",
        "label": "CÓDIGO BALANÇA",
        "name": "balance_code",
        "rules": "nullable|string|max:50"
    },
    {
        "column": "D",
        "label": "REFERÊNCIA",
        "name": "reference",
        "rules": "nullable|string|max:50"
    },
    {
        "column": "E",
        "label": "NOME",
        "name": "name",
        "rules": "required|string|max:255"
    },
    {
        "column": "F",
        "label": "DESCRIÇÃO",
        "name": "description",
        "rules": "nullable|string|max:500"
    },
    {
        "column": "G",
        "label": "ESTOQUE",
        "name": "initial_stock",
        "rules": "nullable|numeric|min:0|max:999999.99"
    },
    {
        "column": "H",
        "label": "ALERTA ESTOQUE MÍNIMO",
        "name": "stock_min",
        "rules": "nullable|numeric|min:0|max:999999.99"
    },
    {
        "column": "I",
        "label": "CUSTO",
        "name": "cost",
        "rules": "nullable|numeric|min:0|max:999999.99"
    },
    {
        "column": "J",
        "label": "PREÇO DE VENDA",
        "name": "price",
        "rules": "nullable|numeric|min:0|max:999999.99"
    },
    {
        "column": "K",
        "label": "CATEGORIA",
        "name": "category",
        "rules": "nullable|string|max:50"
    },
    {
        "column": "L",
        "label": "UNIDADE DE VENDA",
        "name": "unity",
        "rules": "nullable|enum:UNID, KG, M, LITRO, PACOTE, CX, FARDO, KIT, M2, M3, PARES, PC, POTE, VIDRO"
    },
    {
        "column": "M",
        "label": "EXIBIR NO CATÁLOGO",
        "name": "display_on_site",
        "rules": "nullable|enum:S, N, SIM, NÃO, NAO, 1, 0"
    },
    {
        "column": "N",
        "label": "DESTACAR PRODUTO",
        "name": "is_featured",
        "rules": "nullable|enum:S, N, SIM, NÃO, NAO, 1, 0"
    },
    {
        "column": "O",
        "label": "CONTROLAR ESTOQUE",
        "name": "control_stock",
        "rules": "nullable|enum:S, N, SIM, NÃO, NAO, 1, 0"
    },
    {
        "column": "P",
        "label": "PERMITE VENDER FRACIONADO",
        "name": "allow_fractional_sale",
        "rules": "nullable|enum:S, N, SIM, NÃO, NAO, 1, 0"
    },
    {
        "column": "Q",
        "label": "CADASTRO ATIVO",
        "name": "status",
        "rules": "nullable|enum:S, N, SIM, NÃO, NAO, 1, 0"
    },
    {
        "column": "R",
        "label": "NCM",
        "name": "ncm",
        "rules": "nullable|string|max:8"
    },
    {
        "column": "S",
        "label": "ORIGEM",
        "name": "origem",
        "rules": "nullable|enum:0, 1, 2, 3, 4, 5, 6, 7, 8"
    },
    {
        "column": "T",
        "label": "CLASSIFICAÇÃO FISCAL",
        "name": "classificacao_fiscal",
        "rules": "nullable|enum:00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 99"
    },
    {
        "column": "U",
        "label": "CEST",
        "name": "cest",
        "rules": "nullable|string|max:8"
    }
]