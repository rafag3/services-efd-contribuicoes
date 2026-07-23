"""blocoM_builder.py — Monta M001, M200, M205, M210, M600, M605, M610, M990"""

from config.constantes import F100_FIXAS, A170_ALIQ_PIS, A170_ALIQ_COFINS
from domain.models import NotaFiscal, RegistroF600
from domain.formatadores import montar_linha, fmt_valor

# Códigos de receita DCTF
COD_REC_PIS    = "6912"   # PIS/PASEP não-cumulativo
COD_REC_COFINS = "5856"   # COFINS não-cumulativa


def build_blocoM(notas: list[NotaFiscal], f600s: list[RegistroF600] = None,
                 f100_data: list[dict] = None) -> list[str]:
    f100 = f100_data if f100_data is not None else F100_FIXAS
    linhas = []
    linhas.append("|M001|0|")

    # ── PIS ──────────────────────────────────────────────────────────────────
    base_cst01 = round(sum(n.vl_doc for n in notas), 2)
    base_cst02 = round(sum(f["VL_BC_PIS"] for f in f100), 2)

    pis_cst01  = round(base_cst01 * A170_ALIQ_PIS / 100, 2)
    pis_cst02  = round(sum(f["VL_PIS"] for f in f100), 2)
    total_pis  = round(pis_cst01 + pis_cst02, 2)

    ret_nc_pis      = round(sum(f.vl_ret_pis for f in f600s), 2) if f600s else 0.0
    cont_nc_rec_pis = round(total_pis - ret_nc_pis, 2)

    # M200
    linhas.append(montar_linha(
        "M200",
        fmt_valor(total_pis),        # 01 VL_TOT_CONT_NC_PER
        "0",                          # 02 VL_TOT_CRED_DESC
        "0",                          # 03 VL_TOT_CRED_DESC_ANT
        fmt_valor(total_pis),        # 04 VL_TOT_CONT_NC_DEV
        fmt_valor(ret_nc_pis),       # 05 VL_RET_NC
        "0",                          # 06 VL_OUT_DED_NC
        fmt_valor(cont_nc_rec_pis),  # 07 VL_CONT_NC_REC
        "0",                          # 08 VL_TOT_CONT_CUM_PER
        "0",                          # 09 VL_RET_CUM
        "0",                          # 10 VL_OUT_DED_CUM
        "0",                          # 11 VL_CONT_CUM_REC
        fmt_valor(cont_nc_rec_pis),  # 12 VL_TOT_CONT_REC
    ))

    # M205 — obrigatório quando VL_CONT_NC_REC > 0 (desde abr/2014)
    # REG | NUM_CAMPO | COD_REC | VL_DEBITO
    if cont_nc_rec_pis > 0:
        linhas.append(montar_linha(
            "M205",
            "07",                          # NUM_CAMPO = campo 07 (VL_CONT_NC_REC)
            COD_REC_PIS,                   # código receita PIS não-cumulativo
            fmt_valor(cont_nc_rec_pis),    # VL_DEBITO
        ))

    # M210 — 16 campos
    if base_cst02 > 0:
        linhas.append(montar_linha(
            "M210", "02",
            fmt_valor(base_cst02), fmt_valor(base_cst02), "0", "0", fmt_valor(base_cst02),
            "0,65", "0", "", fmt_valor(pis_cst02), "0", "0", "0", "0", fmt_valor(pis_cst02),
        ))
    if base_cst01 > 0:
        linhas.append(montar_linha(
            "M210", "01",
            fmt_valor(base_cst01), fmt_valor(base_cst01), "0", "0", fmt_valor(base_cst01),
            "1,65", "0", "", fmt_valor(pis_cst01), "0", "0", "0", "0", fmt_valor(pis_cst01),
        ))

    # ── COFINS ───────────────────────────────────────────────────────────────
    cofins_cst01       = round(base_cst01 * A170_ALIQ_COFINS / 100, 2)
    cofins_cst02       = round(sum(f["VL_COFINS"] for f in f100), 2)
    total_cofins       = round(cofins_cst01 + cofins_cst02, 2)

    ret_nc_cofins      = round(sum(f.vl_ret_cofins for f in f600s), 2) if f600s else 0.0
    cont_nc_rec_cofins = round(total_cofins - ret_nc_cofins, 2)

    # M600
    linhas.append(montar_linha(
        "M600",
        fmt_valor(total_cofins),          # 01 VL_TOT_CONT_NC_PER
        "0",                               # 02 VL_TOT_CRED_DESC
        "0",                               # 03 VL_TOT_CRED_DESC_ANT
        fmt_valor(total_cofins),          # 04 VL_TOT_CONT_NC_DEV
        fmt_valor(ret_nc_cofins),         # 05 VL_RET_NC
        "0",                               # 06 VL_OUT_DED_NC
        fmt_valor(cont_nc_rec_cofins),    # 07 VL_CONT_NC_REC
        "0",                               # 08 VL_TOT_CONT_CUM_PER
        "0",                               # 09 VL_RET_CUM
        "0",                               # 10 VL_OUT_DED_CUM
        "0",                               # 11 VL_CONT_CUM_REC
        fmt_valor(cont_nc_rec_cofins),    # 12 VL_TOT_CONT_REC
    ))

    # M605 — obrigatório quando VL_CONT_NC_REC > 0
    if cont_nc_rec_cofins > 0:
        linhas.append(montar_linha(
            "M605",
            "07",                           # NUM_CAMPO = campo 07 (VL_CONT_NC_REC)
            COD_REC_COFINS,                 # código receita COFINS não-cumulativa
            fmt_valor(cont_nc_rec_cofins),  # VL_DEBITO
        ))

    # M610 — 16 campos
    if base_cst02 > 0:
        linhas.append(montar_linha(
            "M610", "02",
            fmt_valor(base_cst02), fmt_valor(base_cst02), "0", "0", fmt_valor(base_cst02),
            "4", "0", "", fmt_valor(cofins_cst02), "0", "0", "0", "0", fmt_valor(cofins_cst02),
        ))
    if base_cst01 > 0:
        linhas.append(montar_linha(
            "M610", "01",
            fmt_valor(base_cst01), fmt_valor(base_cst01), "0", "0", fmt_valor(base_cst01),
            "7,6", "0", "", fmt_valor(cofins_cst01), "0", "0", "0", "0", fmt_valor(cofins_cst01),
        ))

    linhas.append(f"|M990|{len(linhas) + 1}|")
    return linhas
