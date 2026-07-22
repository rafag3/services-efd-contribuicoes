"""formatadores.py — Funções de formatação para campos do SPED"""


def fmt_valor(v, decimais: int = 2) -> str:
    if v is None or v == 0.0:
        return "0"
    return f"{v:.{decimais}f}".replace(".", ",")


def fmt_cnpj(cnpj) -> str:
    return str(int(cnpj)).zfill(14)


def fmt_data(dt) -> str:
    import pandas as pd
    if dt is None:
        return ""
    if isinstance(dt, str):
        return dt
    ts = pd.Timestamp(dt)
    return ts.strftime("%d%m%Y")


def montar_linha(*campos) -> str:
    return "|" + "|".join(str(c) for c in campos) + "|"
