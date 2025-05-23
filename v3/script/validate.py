import re
from datetime import datetime, date
from rules.customer import RULES as CUSTOMER_RULES
from rules.product import RULES as PRODUCT_RULES

# Funções auxiliares para validação
def is_required(value):
    return value is not None and str(value).strip() != ""

def is_string(value):
    return isinstance(value, str)

def is_numeric(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False

def is_digits(value, length):
    value_str = str(value)
    return value_str.isdigit() and len(value_str) == length

def is_digits_between(value, min_len, max_len):
    value_str = str(value)
    return value_str.isdigit() and min_len <= len(value_str) <= max_len

def is_email(value):
    if not value:
        return True
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", str(value)))

def is_enum(value, options):
    return str(value).upper() in (str(opt).upper() for opt in options)

def is_boolean(value):
    return str(value).upper() in {"TRUE", "FALSE", "1", "0", "Y", "N", "S", "SIM", "NAO", "NÃO"}

def is_date(value):
    if isinstance(value, date):
        return True
    try:
        datetime.strptime(str(value), "%Y-%m-%d")
        return True
    except Exception:
        return False

def is_before_or_equal_today(value):
    try:
        d = value if isinstance(value, date) else datetime.strptime(str(value), "%Y-%m-%d").date()
        return d <= date.today()
    except Exception:
        return False

def validate_value(value, rule, unique_sets=None):
    errors = []
    rule_parts = rule["rules"].split("|")
    rule_keys = [p.split(":")[0] for p in rule_parts]
    is_nullable = "nullable" in rule_keys

    # Se for nullable e vazio, não faz mais validações
    if is_nullable and (value is None or str(value).strip() == ""):
        return errors

    for part in rule_parts:
        if ":" in part:
            key, param = part.split(":", 1)
        else:
            key, param = part, None

        label = rule['label']

        if key == "required" and not is_required(value):
            errors.append(f"{label} é obrigatório.")
        elif key == "string" and value and not is_string(value):
            errors.append(f"{label} deve ser texto.")
        elif key == "max" and value:
            if is_string(value) and len(str(value)) > int(param):
                errors.append(f"{label} deve ter no máximo {param} caracteres.")
            elif is_numeric(value) and float(value) > float(param):
                errors.append(f"{label} deve ser no máximo {param}.")
        elif key == "min" and value and is_numeric(value) and float(value) < float(param):
            errors.append(f"{label} deve ser no mínimo {param}.")
        elif key == "nullable":
            continue
        elif key == "unique" and unique_sets is not None:
            name = rule["name"]
            if value in unique_sets.get(name, set()):
                errors.append(f"{label} deve ser único.")
            else:
                unique_sets.setdefault(name, set()).add(value)
        elif key == "digits" and value and not is_digits(value, int(param)):
            errors.append(f"{label} deve conter exatamente {param} dígitos.")
        elif key == "digits_between" and value:
            min_len, max_len = map(int, param.split(","))
            if not is_digits_between(value, min_len, max_len):
                errors.append(f"{label} deve conter entre {min_len} e {max_len} dígitos.")
        elif key == "email" and value and not is_email(value):
            errors.append(f"{label} deve ser um e-mail válido.")
        elif key == "numeric" and value and not is_numeric(value):
            errors.append(f"{label} deve ser numérico.")
        elif key in {"enum", "in"} and value:
            options = param.split(",")
            if not is_enum(value, options):
                errors.append(f"{label} deve ser um dos valores: {', '.join(options)}.")
        elif key == "boolean" and value and not is_boolean(value):
            errors.append(f"{label} deve ser booleano.")
        elif key == "date" and value and not is_date(value):
            errors.append(f"{label} deve ser uma data válida (YYYY-MM-DD).")
        elif key == "before_or_equal" and value and param == "today" and not is_before_or_equal_today(value):
            errors.append(f"{label} deve ser uma data igual ou anterior a hoje.")
        # ...outras regras...

    return errors

def validate_row(row, rules=CUSTOMER_RULES, unique_sets=None):
    errors = []
    for rule in rules:
        value = row.get(rule["name"])
        errs = validate_value(value, rule, unique_sets)
        if errs:
            errors.extend(errs)
    return errors

def validate_rows(rows, rules=CUSTOMER_RULES):
    all_errors = []
    unique_sets = {}
    for idx, row in enumerate(rows):
        row_errors = validate_row(row, rules, unique_sets)
        if row_errors:
            all_errors.append({"row": idx + 1, "errors": row_errors})
    return all_errors

def get_labels_from_rules(rules):
    """Retorna a lista de labels das regras, na ordem definida."""
    return [rule["label"].strip().upper() for rule in rules]

def validate_exact_header(header, rules):
    """Valida se o header da planilha corresponde exatamente (ordem, nomes, quantidade) aos labels das regras."""
    expected = get_labels_from_rules(rules)
    received = [str(h).strip().upper() for h in header]
    return received == expected

def identify_table_type(columns):
    """
    Identifica se a tabela é de clientes ou produtos com base nas colunas e labels das regras.
    Retorna 'customer', 'product' ou None.
    Agora exige correspondência exata e ordem dos labels.
    """
    if validate_exact_header(columns, CUSTOMER_RULES):
        return "customer"
    elif validate_exact_header(columns, PRODUCT_RULES):
        return "product"
    else:
        return None