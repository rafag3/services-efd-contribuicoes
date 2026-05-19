"""
blocoM_builder.py — Monta M001, M200, M210, M600, M610, M990
Apuração de PIS/COFINS calculada a partir dos blocos A e F100.
"""

from config.constantes import F100_FIXAS, A170_ALIQ_PIS, A170_ALIQ_COFINS
from domain.models import NotaFiscal
from domain.formatadores import montar_linha, fmt_valor


def build_blocoM(notas: list[NotaFiscal]) -> list[str]:
    linhas = []
    linhas.append("|M001|0|")

    # --- Bases de cálculo ---------------------------------------------------
    # CST 01 — notas de serviço (bloco A), alíquota 1,65% PIS / 7,6% COFINS
    base_cst01 = round(sum(n.vl_doc for n in notas), 2)

    # CST 02 — receitas financeiras (F100 fixas), alíquota 0,65% PIS / 4% COFINS
    base_cst02 = round(sum(f["VL_BC_PIS"] for f in F100_FIXAS), 2)

    # --- PIS -----------------------------------------------------------------
    pis_cst01 = round(base_cst01 * A170_ALIQ_PIS / 100, 2)
    pis_cst02 = round(sum(f["VL_PIS"] for f in F100_FIXAS), 2)
    total_pis  = round(pis_cst01 + pis_cst02, 2)

    # M200
    # VL_TOT_CONT_NC_PER | VL_TOT_CRED_DESC | VL_TOT_CRED_DESC_ANT
    # | VL_TOT_CONT_NC_DEV | VL_RET_NC | VL_OUT_DED_NC | VL_CONT_NC_REC
    # | VL_TOT_CONT_CUM_PER | VL_RET_CUM | VL_OUT_DED_CUM | VL_CONT_CUM_REC
    # | VL_TOT_CONT_REC
    # Obs: VL_RET_NC = total_pis (todo PIS coberto por retenção + créditos acumulados)
    linhas.append(montar_linha(
        "M200",
        fmt_valor(total_pis),   # VL_TOT_CONT_NC_PER
        "0",                    # VL_TOT_CRED_DESC
        "0",                    # VL_TOT_CRED_DESC_ANT
        fmt_valor(total_pis),   # VL_TOT_CONT_NC_DEV
        fmt_valor(total_pis),   # VL_RET_NC (todo coberto por retenções acumuladas)
        "0",                    # VL_OUT_DED_NC
        "0",                    # VL_CONT_NC_REC
        "0",                    # VL_TOT_CONT_CUM_PER
        "0",                    # VL_RET_CUM
        "0",                    # VL_OUT_DED_CUM
        "0",                    # VL_CONT_CUM_REC
        "0",                    # VL_TOT_CONT_REC
    ))

    # M210 — 16 campos (layout correto: REG + 15 campos)
    # COD_CONT|VL_REC_BRT|VL_BC_CONT|VL_AJUS_ACRES_BC|VL_AJUS_REDUC_BC|
    # VL_BC_CONT_AJUS|ALIQ|QUANT_BC|VL_CONT_APUR|VL_AJUS_ACRES|VL_AJUS_REDUC|
    # VL_CONT_DIF|VL_CONT_APUR_NT|VL_CONT_DEV
    if base_cst02 > 0:
        linhas.append(montar_linha(
            "M210",
            "02",
            fmt_valor(base_cst02),
            fmt_valor(base_cst02),
            "0", "0",
            fmt_valor(base_cst02),
            "0,65",
            "0",                    # QUANT_BC_PIS
            "",                     # VL_CONT_APUR (calculado pelo PVA)
            fmt_valor(pis_cst02),   # VL_AJUS_ACRES
            "0",                    # VL_AJUS_REDUC
            "0",                    # VL_CONT_DIF
            "0",                    # VL_CONT_APUR_NT
            "0",                    # VL_CONT_DEV_NT (campo extra — layout v006)
            fmt_valor(pis_cst02),   # VL_CONT_DEV
        ))

    if base_cst01 > 0:
        linhas.append(montar_linha(
            "M210",
            "01",
            fmt_valor(base_cst01),
            fmt_valor(base_cst01),
            "0", "0",
            fmt_valor(base_cst01),
            "1,65",
            "0",
            "",
            fmt_valor(pis_cst01),
            "0",
            "0",
            "0",
            "0",
            fmt_valor(pis_cst01),
        ))

    # --- COFINS --------------------------------------------------------------
    cofins_cst01 = round(base_cst01 * A170_ALIQ_COFINS / 100, 2)
    cofins_cst02 = round(sum(f["VL_COFINS"] for f in F100_FIXAS), 2)
    total_cofins  = round(cofins_cst01 + cofins_cst02, 2)

    # M600
    linhas.append(montar_linha(
        "M600",
        fmt_valor(total_cofins),
        "0",
        "0",
        fmt_valor(total_cofins),
        fmt_valor(total_cofins),   # VL_RET_NC
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
    ))

    # M610 — 16 campos (mesmo layout do M210)
    if base_cst02 > 0:
        linhas.append(montar_linha(
            "M610",
            "02",
            fmt_valor(base_cst02),
            fmt_valor(base_cst02),
            "0", "0",
            fmt_valor(base_cst02),
            "4",
            "0",
            "",
            fmt_valor(cofins_cst02),
            "0", "0", "0", "0",
            fmt_valor(cofins_cst02),
        ))

    if base_cst01 > 0:
        linhas.append(montar_linha(
            "M610",
            "01",
            fmt_valor(base_cst01),
            fmt_valor(base_cst01),
            "0", "0",
            fmt_valor(base_cst01),
            "7,6",
            "0",
            "",
            fmt_valor(cofins_cst01),
            "0", "0", "0", "0",
            fmt_valor(cofins_cst01),
        ))

    linhas.append(f"|M990|{len(linhas) + 1}|")
    return linhas
