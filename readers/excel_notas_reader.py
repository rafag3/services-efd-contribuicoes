"""
excel_notas_reader.py — Lê a planilha de notas fiscais emitidas (XLSX)
e retorna lista de NotaFiscal normalizados.
"""

import pandas as pd
from domain.models import NotaFiscal
from domain.formatadores import fmt_cnpj, fmt_data


def ler_notas(caminho: str) -> list[NotaFiscal]:
    """
    Lê a planilha de notas fiscais.
    - Linha 0: cabeçalho da empresa (ignorada)
    - Linha 1: linha em branco (ignorada)
    - Linha 2: headers das colunas  → header=2
    - Linha 3+: dados
    """
    df = pd.read_excel(caminho, header=2)

    # Remove linhas sem número de NF
    df = df.dropna(subset=["Nº  NF"]).copy()
    df = df.reset_index(drop=True)

    notas = []
    for _, row in df.iterrows():
        cnpj = fmt_cnpj(row["CNPJ"])
        dt_emissao = fmt_data(row["DATA EMISSÃO"])
        regime = str(row.get("REGIME", "")).strip()
        is_simples = "optante pelo simples" in regime.lower() and "não" not in regime.lower()

        # Dt. Dep. pode ser "EM ABERTO" ou NaN
        dt_dep_raw = row.get("Dt. Dep.")
        try:
            dt_deposito = fmt_data(dt_dep_raw) if pd.notna(dt_dep_raw) else None
        except Exception:
            dt_deposito = None

        def _vl(col: str) -> float:
            v = row.get(col, 0)
            try:
                return float(v) if pd.notna(v) else 0.0
            except (ValueError, TypeError):
                return 0.0

        pis_ret    = round(_vl("PIS- 0,65%"), 2)
        cofins_ret = round(_vl("COFINS- 3%"), 2)
        tem_retencao = (pis_ret > 0) or (cofins_ret > 0)

        nota = NotaFiscal(
            comp_emissao    = str(row.get("COMP EMISSÃO", "")).strip(),
            dt_emissao      = dt_emissao,
            prefeitura      = str(row.get("Prefeitura", "SP")).strip(),
            num_nf          = str(int(row["Nº  NF"])),
            num_sap         = str(row.get("Numero SAP  ", "")).strip(),
            vl_doc          = round(_vl("Valor N. Fiscal"), 2),
            iss             = round(_vl("ISS - 5%"), 2),
            irrf            = round(_vl("IRRF - 1,5%"), 2),
            csll            = round(_vl("CSLL - 1%"), 2),
            cofins_ret      = cofins_ret,
            pis_ret         = pis_ret,
            total_csrf      = round(_vl("TOTAL CSRF"), 2),
            vl_liquido      = round(_vl("Valor"), 2),
            doc_banco       = str(row.get("DOC REC BANCO", "")).strip(),
            dt_deposito     = dt_deposito,
            comp_recebimento= str(row.get("COMP RECEBIMENTO", "")).strip() or None,
            cod_cliente     = str(row.get("Cód", "")).strip(),
            bp              = str(row.get("BP", "")).strip(),
            razao           = str(row.get("Razão", "")).strip(),
            cnpj            = cnpj,
            regime          = regime,
            is_simples      = is_simples,
            tem_retencao    = tem_retencao,
        )
        notas.append(nota)

    return notas


def derivar_periodo(notas: list[NotaFiscal]) -> tuple[str, str]:
    """
    Retorna (DT_INI, DT_FIN) no formato DDMMAAAA a partir das notas.
    Usa o COMP EMISSÃO da primeira nota para determinar o mês.
    """
    import calendar
    comp = notas[0].comp_emissao  # ex: "03/2026"
    mes, ano = comp.split("/")
    mes, ano = int(mes), int(ano)
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    dt_ini = f"01{mes:02d}{ano}"
    dt_fin = f"{ultimo_dia}{mes:02d}{ano}"
    return dt_ini, dt_fin
