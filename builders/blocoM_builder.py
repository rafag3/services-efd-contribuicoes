"""
blocoM_builder.py — Monta M001, M200, M210, M600, M610, M990
Apuração de PIS/COFINS calculada a partir dos blocos A e F100.

REGRA M200/M600 VL_RET_NC:
  Deve ser igual à soma de VL_RET_PIS / VL_RET_COFINS dos registros F600 do período.
  Não pode ser maior que esse valor (PVA rejeita).
"""

from config.constantes import F100_FIXAS, A170_ALIQ_PIS, A170_ALIQ_COFINS
from domain.models import NotaFiscal, RegistroF600
from domain.formatadores import montar_linha, fmt_valor


def build_blocoM(notas: list[NotaFiscal], f600s: list[RegistroF600] = None) -> list[str]:
    linhas = []
    linhas.append("|M001|0|")

    # ── Bases de cálculo ────────────────────────────────────────────────────
    # CST 01 — serviços (bloco A): alíquota 1,65% PIS / 7,6% COFINS
    base_cst01 = round(sum(n.vl_doc for n in notas), 2)

    # CST 02 — receitas financeiras (F100): alíquota 0,65% PIS / 4% COFINS
    base_cst02 = round(sum(f["VL_BC_PIS"] for f in F100_FIXAS), 2)

    # ── PIS ──────────────────────────────────────────────────────────────────
    pis_cst01 = round(base_cst01 * A170_ALIQ_PIS / 100, 2)
    pis_cst02 = round(sum(f["VL_PIS"] for f in F100_FIXAS), 2)
    total_pis  = round(pis_cst01 + pis_cst02, 2)

    # VL_RET_NC = soma VL_RET_PIS de todos os F600 do período
    # (PVA exige que VL_RET_NC + VL_RET_CUM <= soma F600 VL_RET_PIS)
    ret_nc_pis = round(sum(f.vl_ret_pis for f in f600s), 2) if f600s else 0.0

    # M200
    linhas.append(montar_linha(
        "M200",
        fmt_valor(total_pis),    # VL_TOT_CONT_NC_PER
        "0",                     # VL_TOT_CRED_DESC
        "0",                     # VL_TOT_CRED_DESC_ANT
        fmt_valor(total_pis),    # VL_TOT_CONT_NC_DEV
        fmt_valor(ret_nc_pis),   # VL_RET_NC = soma F600 VL_RET_PIS
        "0",                     # VL_OUT_DED_NC
        "0",                     # VL_CONT_NC_REC
        "0",                     # VL_TOT_CONT_CUM_PER
        "0",                     # VL_RET_CUM
        "0",                     # VL_OUT_DED_CUM
        "0",                     # VL_CONT_CUM_REC
        "0",                     # VL_TOT_CONT_REC
    ))

    # M210 — 16 campos
    if base_cst02 > 0:
        linhas.append(montar_linha(
            "M210", "02",
            fmt_valor(base_cst02), fmt_valor(base_cst02),
            "0", "0", fmt_valor(base_cst02),
            "0,65", "0", "",
            fmt_valor(pis_cst02), "0", "0", "0", "0",
            fmt_valor(pis_cst02),
        ))

    if base_cst01 > 0:
        linhas.append(montar_linha(
            "M210", "01",
            fmt_valor(base_cst01), fmt_valor(base_cst01),
            "0", "0", fmt_valor(base_cst01),
            "1,65", "0", "",
            fmt_valor(pis_cst01), "0", "0", "0", "0",
            fmt_valor(pis_cst01),
        ))

    # ── COFINS ───────────────────────────────────────────────────────────────
    cofins_cst01 = round(base_cst01 * A170_ALIQ_COFINS / 100, 2)
    cofins_cst02 = round(sum(f["VL_COFINS"] for f in F100_FIXAS), 2)
    total_cofins  = round(cofins_cst01 + cofins_cst02, 2)

    ret_nc_cofins = round(sum(f.vl_ret_cofins for f in f600s), 2) if f600s else 0.0

    # M600
    linhas.append(montar_linha(
        "M600",
        fmt_valor(total_cofins),
        "0", "0",
        fmt_valor(total_cofins),
        fmt_valor(ret_nc_cofins),  # VL_RET_NC = soma F600 VL_RET_COFINS
        "0", "0", "0", "0", "0", "0", "0",
    ))

    # M610 — 16 campos
    if base_cst02 > 0:
        linhas.append(montar_linha(
            "M610", "02",
            fmt_valor(base_cst02), fmt_valor(base_cst02),
            "0", "0", fmt_valor(base_cst02),
            "4", "0", "",
            fmt_valor(cofins_cst02), "0", "0", "0", "0",
            fmt_valor(cofins_cst02),
        ))

    if base_cst01 > 0:
        linhas.append(montar_linha(
            "M610", "01",
            fmt_valor(base_cst01), fmt_valor(base_cst01),
            "0", "0", fmt_valor(base_cst01),
            "7,6", "0", "",
            fmt_valor(cofins_cst01), "0", "0", "0", "0",
            fmt_valor(cofins_cst01),
        ))

    linhas.append(f"|M990|{len(linhas) + 1}|")
    return linhas
