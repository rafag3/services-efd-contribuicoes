"""
excel_notas_reader.py — Lê a planilha de notas fiscais emitidas
Suporta dois formatos:
  - Planilha anual: aba 'FATURAMENTO', header na linha 3
  - Planilha mensal (legado): header na linha 2
Filtra pelo mês/ano selecionado pelo usuário.
"""

import pandas as pd
from domain.models import NotaFiscal
from domain.formatadores import fmt_cnpj, fmt_data


def ler_notas(caminho: str, mes: int = None, ano: int = None) -> list[NotaFiscal]:
    """
    Lê a planilha de notas fiscais e filtra pelo período informado (mes/ano).
    - Se mes e ano forem None, retorna todas as notas presentes.
    - F600 só é gerado para notas com Dt. Dep. preenchida (não "EM ABERTO", não 0, não NaN).
    """
    # Tenta aba FATURAMENTO (planilha anual) → senão lê formato legado
    try:
        df = pd.read_excel(caminho, sheet_name='FATURAMENTO', header=3)
    except Exception:
        df = pd.read_excel(caminho, header=2)

    # Remove linhas sem NF
    df = df.dropna(subset=["Nº  NF"]).copy()
    df = df.reset_index(drop=True)

    # Filtra pelo mês/ano selecionado pelo usuário
    if mes is not None and ano is not None:
        comp_alvo = f"{mes:02d}/{ano}"
        df = df[df["COMP EMISSÃO"].astype(str).str.strip() == comp_alvo].copy()
        df = df.reset_index(drop=True)

    notas = []
    for _, row in df.iterrows():
        cnpj       = fmt_cnpj(row["CNPJ"])
        dt_emissao = fmt_data(row["DATA EMISSÃO"])
        regime     = str(row.get("REGIME", "")).strip()
        is_simples = "optante pelo simples" in regime.lower() and "não" not in regime.lower()

        # Dt. Dep. — "EM ABERTO", 0 ou NaN → nota não foi paga → sem F600
        dt_dep_raw  = row.get("Dt. Dep.")
        dt_deposito = None
        foi_pago    = False
        try:
            if pd.notna(dt_dep_raw):
                val = str(dt_dep_raw).strip().upper()
                if val not in ("EM ABERTO", "0", ""):
                    dt_deposito = fmt_data(dt_dep_raw)
                    foi_pago    = True
        except Exception:
            pass

        def _vl(col: str) -> float:
            v = row.get(col, 0)
            try:
                return float(v) if pd.notna(v) else 0.0
            except (ValueError, TypeError):
                return 0.0

        pis_ret    = round(_vl("PIS- 0,65%"), 2)
        cofins_ret = round(_vl("COFINS- 3%"), 2)

        # Gera F600 somente se: tem retenção E foi pago E não é Simples
        tem_retencao = (pis_ret > 0 or cofins_ret > 0) and foi_pago and not is_simples

        nota = NotaFiscal(
            comp_emissao     = str(row.get("COMP EMISSÃO", "")).strip(),
            dt_emissao       = dt_emissao,
            prefeitura       = str(row.get("Prefeitura", "SP")).strip(),
            num_nf           = str(int(row["Nº  NF"])),
            num_sap          = str(row.get("Numero SAP  ", "")).strip(),
            vl_doc           = round(_vl("Valor N. Fiscal"), 2),
            iss              = round(_vl("ISS - 5%"), 2),
            irrf             = round(_vl("IRRF - 1,5%"), 2),
            csll             = round(_vl("CSLL - 1%"), 2),
            cofins_ret       = cofins_ret,
            pis_ret          = pis_ret,
            total_csrf       = round(_vl("TOTAL CSRF"), 2),
            vl_liquido       = round(_vl("Valor"), 2),
            doc_banco        = str(row.get("DOC REC BANCO", "")).strip(),
            dt_deposito      = dt_deposito,
            comp_recebimento = str(row.get("COMP RECEBIMENTO", "")).strip() or None,
            cod_cliente      = str(row.get("Cód", "")).strip(),
            bp               = str(row.get("BP", "")).strip(),
            razao            = str(row.get("Razão", "")).strip(),
            cnpj             = cnpj,
            regime           = regime,
            is_simples       = is_simples,
            tem_retencao     = tem_retencao,
        )
        notas.append(nota)

    return notas


def derivar_periodo(notas: list[NotaFiscal]) -> tuple[str, str]:
    import calendar
    comp = notas[0].comp_emissao
    mes, ano = comp.split("/")
    mes, ano = int(mes), int(ano)
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    return f"01{mes:02d}{ano}", f"{ultimo_dia}{mes:02d}{ano}"
