"""blocoA_builder.py — Monta A001, A010, A100, A170, A990"""

from config.constantes import (
    EMPRESA,
    A100_IND_EMIT, A100_IND_OPER, A100_COD_SIT, A100_IND_PGTO,
    A170_NUM_ITEM, A170_COD_ITEM, A170_CST_PIS, A170_ALIQ_PIS,
    A170_CST_COFINS, A170_ALIQ_COFINS, A170_COD_CTA,
)
from domain.models import NotaFiscal
from domain.formatadores import montar_linha, fmt_valor


def build_blocoA(notas: list[NotaFiscal]) -> list[str]:
    linhas = []
    linhas.append("|A001|0|")
    linhas.append(f"|A010|{EMPRESA['CNPJ']}|")
    for nota in notas:
        linhas += _build_a100_a170(nota)
    linhas.append(f"|A990|{len(linhas) + 1}|")
    return linhas


def _build_a100_a170(nota: NotaFiscal) -> list[str]:
    base = nota.vl_doc
    vl_pis_proprio    = round(base * A170_ALIQ_PIS / 100, 2)
    vl_cofins_proprio = round(base * A170_ALIQ_COFINS / 100, 2)

    a100 = montar_linha(
        "A100",
        A100_IND_EMIT, A100_IND_OPER,
        nota.cnpj,
        A100_COD_SIT,
        "A",              # CHV_NFSE
        "",               # RES_CHV
        nota.num_nf,
        "",               # COD_ITEM
        nota.dt_emissao,
        nota.dt_emissao,  # DT_EXE_SERV
        fmt_valor(base),
        A100_IND_PGTO,
        "",               # VL_DESC
        fmt_valor(base),
        fmt_valor(vl_pis_proprio),
        fmt_valor(base),
        fmt_valor(vl_cofins_proprio),
        fmt_valor(nota.pis_ret),
        fmt_valor(nota.cofins_ret),
        "",               # VL_ISS
    )

    # A170 — 18 campos
    # REG|NUM_ITEM|COD_ITEM|DESCR_COMPL|VL_ITEM|VL_DESC|
    # NAT_BC_CRED|IND_ORIG_CRED|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|
    # CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|INFO_COMPL
    a170 = montar_linha(
        "A170",
        A170_NUM_ITEM, A170_COD_ITEM,
        "",               # DESCR_COMPL
        fmt_valor(base),
        "",               # VL_DESC
        "",               # NAT_BC_CRED
        "",               # IND_ORIG_CRED
        A170_CST_PIS,
        fmt_valor(base),
        fmt_valor(A170_ALIQ_PIS, 2),
        fmt_valor(vl_pis_proprio),
        A170_CST_COFINS,
        fmt_valor(base),
        fmt_valor(A170_ALIQ_COFINS, 1),
        fmt_valor(vl_cofins_proprio),
        A170_COD_CTA,
        "",               # INFO_COMPL
    )
    return [a100, a170]
