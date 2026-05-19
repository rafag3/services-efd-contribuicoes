"""
blocoF_builder.py — Monta F001, F010, F100 (fixo) e F600 (das notas)
"""

from collections import defaultdict
from config.constantes import (
    EMPRESA,
    F100_FIXAS,
    F600_IND_NAT_RET, F600_COD_REC, F600_IND_NAT_PJ, F600_IND_DEC,
)
from domain.models import NotaFiscal, RegistroF600
from domain.formatadores import montar_linha, fmt_valor


def build_blocoF(notas: list[NotaFiscal]) -> list[str]:
    linhas = []

    linhas.append("|F001|0|")
    linhas.append(f"|F010|{EMPRESA['CNPJ']}|")

    # F100 — Receitas financeiras (valores fixos provisórios)
    # F100 — 19 campos (sem DESC_DOC_OPE, que não existe na EFD Contribuições)
    # REG|IND_OPER|IND_ORIG|COD_ITEM|DT_OPER|VL_OPER|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|
    # CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|NAT_BC_CRED|IND_ORIG_CRED|COD_CTA|COD_CENTRO|COD_PART
    for f in F100_FIXAS:
        linhas.append(montar_linha(
            "F100",
            f["IND_OPER"], f["IND_ORIG"], f["COD_ITEM"],
            f["DT_OPER"],
            fmt_valor(f["VL_OPER"]),
            f["CST_PIS"],
            fmt_valor(f["VL_BC_PIS"]),
            fmt_valor(f["ALIQ_PIS"], 2),
            fmt_valor(f["VL_PIS"]),
            f["CST_COFINS"],
            fmt_valor(f["VL_BC_COFINS"]),
            fmt_valor(f["ALIQ_COFINS"]),
            fmt_valor(f["VL_COFINS"]),
            f["NAT_BC_CRED"], f["IND_ORIG_CRED"],
            f["COD_CTA"], f["COD_CENTRO"], f["COD_PART"],
            # DESC_DOC_OPE removido — não existe no layout da EFD Contribuições
        ))

    # F600 — Retenções agrupadas por CNPJ + data
    for f600 in _agrupar_retencoes(notas):
        linhas.append(montar_linha(
            "F600",
            F600_IND_NAT_RET,
            f600.dt_ret,
            fmt_valor(f600.vl_bc_ret),
            fmt_valor(f600.vl_ret_total),
            F600_COD_REC,
            F600_IND_NAT_PJ,
            f600.cnpj_tomador,
            fmt_valor(f600.vl_ret_pis),
            fmt_valor(f600.vl_ret_cofins),
            F600_IND_DEC,
        ))

    linhas.append(f"|F990|{len(linhas) + 1}|")
    return linhas


def _agrupar_retencoes(notas: list[NotaFiscal]) -> list[RegistroF600]:
    """
    Agrupa notas com retenção por (CNPJ, data).
    Retorna uma lista de RegistroF600 ordenada por CNPJ.
    """
    grupos: dict[tuple, dict] = defaultdict(lambda: {
        "vl_bc_ret": 0.0, "vl_ret_pis": 0.0, "vl_ret_cofins": 0.0
    })

    for nota in notas:
        if not nota.tem_retencao:
            continue
        chave = (nota.cnpj, nota.dt_emissao)
        grupos[chave]["vl_bc_ret"]    += nota.vl_doc
        grupos[chave]["vl_ret_pis"]   += nota.pis_ret
        grupos[chave]["vl_ret_cofins"] += nota.cofins_ret

    resultado = []
    for (cnpj, dt_ret), vals in sorted(grupos.items()):
        resultado.append(RegistroF600(
            cnpj_tomador  = cnpj,
            dt_ret        = dt_ret,
            vl_bc_ret     = round(vals["vl_bc_ret"], 2),
            vl_ret_pis    = round(vals["vl_ret_pis"], 2),
            vl_ret_cofins = round(vals["vl_ret_cofins"], 2),
        ))

    return resultado
