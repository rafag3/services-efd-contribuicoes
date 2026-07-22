"""
bloco0_builder.py — Monta os registros do Bloco 0 (abertura e cadastros)
"""

from config.constantes import (
    EMPRESA, CONTATO, IND_0110, IND_0111,
    UNIDADES, ITENS, CONTAS,
)
from domain.models import NotaFiscal
from domain.formatadores import montar_linha, fmt_cnpj


def build_bloco0(notas: list[NotaFiscal], dt_ini: str, dt_fin: str) -> list[str]:
    linhas = []

    # 0000 — Abertura
    linhas.append(montar_linha(
        "0000", "006", "0", "", "",
        dt_ini, dt_fin,
        EMPRESA["NOME"], EMPRESA["CNPJ"],
        EMPRESA["UF"], EMPRESA["COD_MUN"],
        EMPRESA["SUFRAMA"], EMPRESA["IND_SIT_ESP"],
        EMPRESA["IND_APUR_IPI"],
    ))

    linhas.append("|0001|0|")

    # 0100 — Dados do contato
    c = CONTATO
    linhas.append(montar_linha(
        "0100",
        c["NOME"], c["CPF"], c["CRC"], "",
        c["CEP"], c["END"], c["NUM"], c["COMPL"], c["BAI"],
        c["FONE"], c["FAX"], c["EMAIL"], c["COD_MUN"],
    ))

    # 0110
    linhas.append(montar_linha(
        "0110",
        IND_0110["IND_INC_IMOB"],
        IND_0110["IND_ATIV_IMOB"],
        IND_0110["IND_ATIV"],
        "",
    ))

    # 0111
    i = IND_0111
    linhas.append(montar_linha(
        "0111",
        i["REC_BRU_NCUM_TRIB_MI"],
        i["REC_BRU_NCUM_NT_MI"],
        i["REC_BRU_NCUM_EXP"],
        i["REC_BRU_CUM"],
        i["REC_BRU_TOTAL"],
    ))

    # 0140 — Estabelecimento
    linhas.append(montar_linha(
        "0140",
        EMPRESA["CNPJ"],
        EMPRESA["NOME"],
        EMPRESA["CNPJ"],
        EMPRESA["UF"],
        "",
        EMPRESA["COD_MUN"],
        EMPRESA["INSCR_MUN"],
        EMPRESA["SUFRAMA"],
    ))

    # 0150 — Participantes
    # Filtra CNPJs inválidos (zeros, brancos ou menores que 11 dígitos numéricos)
    participantes = {}
    for nota in notas:
        cnpj = nota.cnpj.strip()
        # Ignora CNPJ zerado ou inválido
        if not cnpj or int(cnpj) == 0 or len(cnpj) < 11:
            continue
        if cnpj not in participantes:
            participantes[cnpj] = nota.razao

    for cnpj, razao in sorted(participantes.items()):
        linhas.append(montar_linha(
            "0150",
            cnpj,            # COD_PART (campo 2)
            razao,           # NOME
            "1058",          # COD_PAIS — Brasil
            cnpj,            # CNPJ
            "",              # CPF
            "",              # IE
            "9999999",       # COD_MUN — obrigatório p/ contribuintes no Brasil
            "",              # NUM_SUF
            "",              # END
            "",              # NUM
            "",              # COMPL
            "",              # BAI
        ))

    # 0190 — Unidades de medida
    for um, descr in UNIDADES:
        linhas.append(montar_linha("0190", um, descr))

    # 0200 — Itens (11 campos, sem CEST)
    for item in ITENS:
        linhas.append(montar_linha("0200", *item))

    # 0500 — Plano de contas
    for conta in CONTAS:
        linhas.append(montar_linha("0500", *conta))

    # 0990 — Encerramento
    linhas.append(f"|0990|{len(linhas) + 1}|")

    return linhas
