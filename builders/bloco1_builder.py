"""
bloco1_builder.py — Monta o Bloco 1 (1300, 1700) e blocos vazios C, D, I, P
"""

from config.constantes import (
    RETENCAO_ACUMULADA_PIS,
    RETENCAO_ACUMULADA_COFINS,
    RETENCAO_PER_APU,
    F100_FIXAS,
)
from domain.models import NotaFiscal
from domain.formatadores import montar_linha, fmt_valor


def build_blocos_vazios() -> list[str]:
    """Blocos C, D, I e P sem movimento (fechados)."""
    return [
        "|C001|1|", "|C990|2|",
        "|D001|1|", "|D990|2|",
        "|I001|1|", "|I990|2|",
        "|P001|1|", "|P990|2|",
    ]


def build_bloco1(notas: list[NotaFiscal]) -> list[str]:
    """
    1300 — PIS retido acumulado
    1700 — COFINS retido acumulado
    VL_RET_EFE = soma do VL_PIS / VL_COFINS dos registros F100 do período
                 (receitas financeiras — regra confirmada pela área)
    VL_RET_A_EFET = VL_RET_APU - VL_RET_EFE
    """
    linhas = []
    linhas.append("|1001|0|")

    # VL_RET_EFE vem do total de PIS/COFINS do F100 (não das notas)
    ret_efe_pis    = round(sum(f["VL_PIS"]    for f in F100_FIXAS), 2)
    ret_efe_cofins = round(sum(f["VL_COFINS"] for f in F100_FIXAS), 2)

    # 1300 — PIS
    vl_ret_apu_pis   = RETENCAO_ACUMULADA_PIS
    vl_ret_efet_pis  = round(vl_ret_apu_pis - ret_efe_pis, 2)
    linhas.append(montar_linha(
        "1300",
        "03",
        RETENCAO_PER_APU,
        fmt_valor(vl_ret_apu_pis),
        fmt_valor(ret_efe_pis),
        "0",
        "0",
        fmt_valor(vl_ret_efet_pis),
    ))

    # 1700 — COFINS
    vl_ret_apu_cofins  = RETENCAO_ACUMULADA_COFINS
    vl_ret_efet_cofins = round(vl_ret_apu_cofins - ret_efe_cofins, 2)
    linhas.append(montar_linha(
        "1700",
        "03",
        RETENCAO_PER_APU,
        fmt_valor(vl_ret_apu_cofins),
        fmt_valor(ret_efe_cofins),
        "0",
        "0",
        fmt_valor(vl_ret_efet_cofins),
    ))

    linhas.append(f"|1990|{len(linhas) + 1}|")
    return linhas
