RULES = [
    {
        "column": "A",
        "label": "CÓDIGO",
        "key": "codigo",
        "rules": "nullable",
    },
    {
        "column": "B",
        "label": "NOME",
        "key": "nome",
        "rules": "required|string|max:50",
    },
    {
        "column": "C",
        "label": "CPF",
        "key": "cpf",
        "rules": "nullable|unique|digits:11",
    },
    {
        "column": "D",
        "label": "RG",
        "key": "rg",
        "rules": "nullable|string|max:20",
    },
    {
        "column": "E",
        "label": "CNPJ",
        "key": "cnpj",
        "rules": "nullable|unique|digits:14",
    },
    {
        "column": "F",
        "label": "IE",
        "key": "ie",
        "rules": "nullable|string|max:20",
    },
    {
        "column": "G",
        "label": "INDICADOR ICMS",
        "key": "indicador_icms",
        "rules": "nullable|enum:1,2,9",
    },
    {
        "column": "H",
        "label": "TELEFONE",
        "key": "telefone",
        "rules": "nullable|digits_between:10,11",
    },
    {
        "column": "I",
        "label": "WHATSAPP",
        "key": "whatsapp",
        "rules": "nullable|digits_between:10,11",
    },
    {
        "column": "J",
        "label": "EMAIL",
        "key": "email",
        "rules": "nullable|email|max:50",
    },
    {
        "column": "K",
        "label": "LIMITE DE CRÉDITO",
        "key": "limite_de_credito",
        "rules": "nullable|numeric|min:0|max:999999.99",
    },
    {
        "column": "L",
        "label": "ATIVO",
        "key": "ativo",
        "rules": "nullable|enum:1,0,Y,N,S,NÃO,SIM,NAO",
    },
    {
        "column": "M",
        "label": "NOME DA MÃE",
        "key": "nome_da_mae",
        "rules": "nullable|string|max:50",
    },
    {
        "column": "N",
        "label": "OBSERVAÇÕES",
        "key": "observacoes",
        "rules": "nullable|string|max:500",
    },
    {
        "column": "O",
        "label": "DATA DE NASCIMENTO",
        "key": "data_de_nascimento",
        "rules": "nullable|date|before_or_equal:today",
    },
    {
        "column": "P",
        "label": "ENDEREÇO",
        "key": "endereco",
        "rules": "nullable|string|max:50",
    },
    {
        "column": "Q",
        "label": "NÚMERO",
        "key": "numero",
        "rules": "nullable|string|max:10",
    },
    {
        "column": "R",
        "label": "COMPLEMENTO",
        "key": "complemento",
        "rules": "nullable|string|max:50",
    },
    {
        "column": "S",
        "label": "BAIRRO",
        "key": "bairro",
        "rules": "nullable|string|max:50",
    },
    {
        "column": "T",
        "label": "CIDADE",
        "key": "cidade",
        "rules": "nullable|string|max:50",
    },
    {
        "column": "U",
        "label": "ESTADO",
        "key": "estado",
        "rules": "nullable|string|max:2",
    },
    {
        "column": "V",
        "label": "CEP",
        "key": "cep",
        "rules": "nullable|digits:8",
    },
]
