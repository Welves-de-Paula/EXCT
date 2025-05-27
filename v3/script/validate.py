from rules.customer import RULES as CUSTOMER_RULES
from rules.product import RULES as PRODUCT_RULES
import re
from datetime import datetime


def _parse_rule(rule):
    """Divide uma regra composta em partes."""
    return rule.split('|')


def _parse_enum(enum_rule):
    """Extrai os valores permitidos de uma regra enum."""
    return enum_rule.split(':', 1)[1].split(',')


def _parse_digits(rule):
    """Extrai o número de dígitos de uma regra digits ou digits_between."""
    if rule.startswith('digits_between:'):
        return tuple(map(int, rule.split(':', 1)[1].split(',')))
    return int(rule.split(':', 1)[1])


def _parse_max(rule):
    return float(rule.split(':', 1)[1])


def _parse_min(rule):
    return float(rule.split(':', 1)[1])


def _parse_string_max(rule):
    return int(rule.split(':', 1)[1])


def _parse_date_rule(rule):
    return rule.split(':', 1)[1]


def _is_empty(val):
    return val is None or (isinstance(val, str) and val.strip() == "")


def _is_numeric(val):
    try:
        float(val)
        return True
    except Exception:
        return False


def _is_email(val):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", val))


def _is_boolean(val):
    return str(val).strip().upper() in ['1', '0', 'Y', 'N', 'S', 'NÃO', 'SIM', 'NAO']


def _is_date(val):
    # Aceita formatos comuns de data
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            datetime.strptime(val, fmt)
            return True
        except Exception:
            continue
    return False


def _date_value(val):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(val, fmt)
        except Exception:
            continue
    return None


def validate(row, tipo, all_rows=None):
    """
    Valida uma linha de dados conforme as regras do tipo (customer ou product).
    row: dict {coluna: {key, value, ...}}
    tipo: 'customer' ou 'product'
    all_rows: lista de todas as linhas (para validação de duplicidade)
    Retorna: lista de mensagens de erro (ou lista vazia se válido)
    """
    errors = []
    tipo = str(tipo).strip().lower()
    if tipo == "customer":
        RULES = CUSTOMER_RULES
    elif tipo == "product":
        RULES = PRODUCT_RULES
    else:
        return ["Tipo de regra não encontrado."]

    if all_rows is None:
        all_rows = []

    # Para validação de duplicidade: mapeia valores únicos para contagem
    unique_fields = [r["key"] for r in (
        CUSTOMER_RULES if tipo == "customer" else PRODUCT_RULES) if "unique" in r.get("rules", "")]
    duplicates = {}
    for field in unique_fields:
        values = [r.get(field, {}).get("value", "")
                  for r in all_rows if r.get(field, {}).get("value", "")]
        for v in set(values):
            duplicates.setdefault(field, set()).add(v)

    for rule in RULES:
        key = rule["key"]
        label = rule.get("label", key)
        rules = _parse_rule(rule.get("rules", ""))
        val = row.get(key, {}).get("value", "")
        # required
        if "required" in rules and _is_empty(val):
            errors.append(f"{label}: obrigatório.")
            continue
        # nullable
        if "nullable" in rules and _is_empty(val):
            continue
        # unique (agora marca todas as linhas duplicadas)
        if "unique" in rules and val and all_rows:
            if key in duplicates and val in duplicates[key]:
                errors.append(f"{label}: valor duplicado ({val}).")
        # string
        if "string" in rules and not isinstance(val, str):
            errors.append(f"{label}: deve ser texto.")
        # numeric
        if "numeric" in rules and not _is_numeric(val):
            errors.append(f"{label}: deve ser numérico.")
        # digits
        for r in rules:
            if r.startswith("digits:"):
                n = _parse_digits(r)
                if not (val.isdigit() and len(val) == n):
                    errors.append(f"{label}: deve conter {n} dígitos.")
            if r.startswith("digits_between:"):
                min_d, max_d = _parse_digits(r)
                if not (val.isdigit() and min_d <= len(val) <= max_d):
                    errors.append(
                        f"{label}: deve conter entre {min_d} e {max_d} dígitos.")
        # max
        for r in rules:
            if r.startswith("max:"):
                max_v = _parse_max(r)
                if "string" in rules:
                    if len(val) > max_v:
                        errors.append(
                            f"{label}: máximo {int(max_v)} caracteres.")
                elif "numeric" in rules and _is_numeric(val):
                    if float(val) > max_v:
                        errors.append(f"{label}: máximo {max_v}.")
        # min
        for r in rules:
            if r.startswith("min:"):
                min_v = _parse_min(r)
                if "numeric" in rules and _is_numeric(val):
                    if float(val) < min_v:
                        errors.append(f"{label}: mínimo {min_v}.")
        # enum
        for r in rules:
            if r.startswith("enum:"):
                allowed = _parse_enum(r)
                if str(val).strip() and str(val).strip() not in allowed:
                    errors.append(f"{label}: valor inválido ({val}).")
        # email
        if "email" in rules and val and not _is_email(val):
            errors.append(f"{label}: e-mail inválido.")
        # boolean
        if "boolean" in rules and val and not _is_boolean(val):
            errors.append(f"{label}: valor booleano inválido.")
        # date
        if "date" in rules and val and not _is_date(val):
            errors.append(f"{label}: data inválida.")
        # before_or_equal:today
        for r in rules:
            if r.startswith("before_or_equal:"):
                if val and _is_date(val):
                    cmp = _parse_date_rule(r)
                    if cmp == "today":
                        dt = _date_value(val)
                        if dt and dt > datetime.today():
                            errors.append(
                                f"{label}: deve ser anterior ou igual a hoje.")
    return errors
