RULES = [
    {
        "column": "A",
        "label": "CÓDIGO",
        "key": "codigo",
        "rules": "nullable"
    },
    {
        "column": "B",
        "label": "CÓDIGO DE BARRAS",
        "key": "codigo_barras",
        "rules": "nullable|unique|digits:13",
    },
    {
        "column": "C",
        "label": "CÓDIGO BALANÇA",
        "key": "codigo_balanca",
        "rules": "nullable|string|max:50",
    },
    {
        "column": "D",
        "label": "REFERÊNCIA",
        "key": "referencia",
        "rules": "nullable|string|max:50",
    },
    {
        "column": "E",
        "label": "NOME",
        "key": "nome",
        "rules": "required|string|max:255"},
    {
        "column": "F",
        "label": "DESCRIÇÃO",
        "key": "descricao",
        "rules": "nullable|string|max:500",
    },
    {
        "column": "G",
        "label": "ESTOQUE",
        "key": "estoque_inicial",
        "rules": "nullable|numeric|min:0|max:999999.99",
    },
    {
        "column": "H",
        "label": "ALERTA ESTOQUE MÍNIMO",
        "key": "estoque_minimo",
        "rules": "nullable|numeric|min:0|max:999999.99",
    },
    {
        "column": "I",
        "label": "CUSTO",
        "key": "custo",
        "rules": "nullable|numeric|min:0|max:999999.99",
    },
    {
        "column": "J",
        "label": "PREÇO DE VENDA",
        "key": "preco",
        "rules": "nullable|numeric|min:0|max:999999.99",
    },
    {
        "column": "K",
        "label": "CATEGORIA",
        "key": "categoria",
        "rules": "nullable|string|max:50",
    },
    {
        "column": "L",
        "label": "UNIDADE DE VENDA",
        "key": "unidade_venda",
        "rules": "nullable|enum:UNID,KG,M,LITRO,PACOTE,CX,FARDO,KIT,M2,M3,PARES,PC,POTE,VIDRO",
    },
    {
        "column": "M",
        "label": "EXIBIR NO CATÁLOGO",
        "key": "exibir_catalogo",
        "rules": "nullable|enum:S,N",
    },
    {
        "column": "N",
        "label": "DESTACAR PRODUTO",
        "key": "produto_destaque",
        "rules": "nullable|enum:S,N",
    },
    {
        "column": "O",
        "label": "CONTROLAR ESTOQUE",
        "key": "controlar_estoque",
        "rules": "nullable|enum:S,N",
    },
    {
        "column": "P",
        "label": "PERMITE VENDER FRACIONADO",
        "key": "venda_fracionada",
        "rules": "nullable|enum:S,N",
    },
    {
        "column": "Q",
        "label": "CADASTRO ATIVO",
        "key": "cadastro_ativo",
        "rules": "nullable|enum:S,N",
    },
    {
        "column": "R",
        "label": "NCM",
        "key": "ncm",
        "rules": "nullable|string|max:8"},
    {
        "column": "S",
        "label": "ORIGEM",
        "key": "origem",
        "rules": "nullable|enum:0,1,2,3,4,5,6,7,8",
    },
    {
        "column": "T",
        "label": "CLASSIFICAÇÃO FISCAL",
        "key": "classificacao_fiscal",
        "rules": "nullable|enum:00,01,02,03,04,05,06,07,08,09,10,99",
    },
    {
        "column": "U",
        "label": "CEST",
        "key": "cest",
        "rules": "nullable|string|max:8"
    },
]
