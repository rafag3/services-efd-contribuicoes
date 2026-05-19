"""
formatadores.py — Funções de formatação para campos do SPED
"""


def fmt_valor(v: float | None, decimais: int = 2) -> str:
    """Formata float como string com vírgula decimal, sem separador de milhar."""
    if v is None or v == 0.0:
        return "0"
    return f"{v:.{decimais}f}".replace(".", ",")


def fmt_cnpj(cnpj) -> str:
    """Normaliza CNPJ para 14 dígitos sem pontuação."""
    return str(int(cnpj)).zfill(14)


def fmt_data(dt) -> str:
    """Converte datetime para DDMMAAAA."""
    import pandas as pd
    if dt is None:
        return ""
    if isinstance(dt, str):
        return dt
    ts = pd.Timestamp(dt)
    return ts.strftime("%d%m%Y")


def montar_linha(*campos) -> str:
    """Monta uma linha SPED com pipes."""
    return "|" + "|".join(str(c) for c in campos) + "|"
