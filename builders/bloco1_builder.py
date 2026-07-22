"""bloco1_builder.py — Monta 1001, 1300, 1700, 1990"""

from config.constantes import (
    RETENCAO_ACUMULADA_PIS,
    RETENCAO_ACUMULADA_COFINS,
    RETENCAO_PER_APU,
    F100_FIXAS,
)
from domain.models import NotaFiscal
from domain.formatadores import montar_linha, fmt_valor


def build_bloco1(notas: list[NotaFiscal]) -> list[str]:
    """
    VL_RET_EFE = soma VL_PIS / VL_COFINS dos registros F100 (receitas financeiras)
    VL_RET_A_EFET = VL_RET_APU - VL_RET_EFE
    """
    linhas = []
    linhas.append("|1001|0|")

    ret_efe_pis    = round(sum(f["VL_PIS"]    for f in F100_FIXAS), 2)
    ret_efe_cofins = round(sum(f["VL_COFINS"] for f in F100_FIXAS), 2)

    # 1300 — PIS
    vl_apu_pis   = RETENCAO_ACUMULADA_PIS
    vl_efet_pis  = round(vl_apu_pis - ret_efe_pis, 2)
    linhas.append(montar_linha(
        "1300", "03", RETENCAO_PER_APU,
        fmt_valor(vl_apu_pis),
        fmt_valor(ret_efe_pis),
        "0", "0",
        fmt_valor(vl_efet_pis),
    ))

    # 1700 — COFINS
    vl_apu_cofins  = RETENCAO_ACUMULADA_COFINS
    vl_efet_cofins = round(vl_apu_cofins - ret_efe_cofins, 2)
    linhas.append(montar_linha(
        "1700", "03", RETENCAO_PER_APU,
        fmt_valor(vl_apu_cofins),
        fmt_valor(ret_efe_cofins),
        "0", "0",
        fmt_valor(vl_efet_cofins),
    ))

    linhas.append(f"|1990|{len(linhas) + 1}|")
    return linhas
