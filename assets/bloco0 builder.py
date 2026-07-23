"""
bloco0_builder.py — Monta os registros do Bloco 0 (abertura e cadastros)
COD_MUN no 0150 é buscado automaticamente via BrasilAPI (gratuita, sem cadastro).
Cache em memória evita múltiplas consultas para o mesmo CNPJ.
"""

import urllib.request
import json
import time
from config.constantes import (
    EMPRESA, CONTATO, IND_0110, IND_0111,
    UNIDADES, ITENS, CONTAS,
)
from domain.models import NotaFiscal
from domain.formatadores import montar_linha

# Cache em memória: CNPJ → (cod_mun_ibge, municipio, uf)
_cache_cnpj: dict = {}


def _buscar_municipio(cnpj: str) -> str:
    """
    Consulta a BrasilAPI para obter o código IBGE do município do CNPJ.
    Retorna o código de 7 dígitos ou '9999999' em caso de falha.
    """
    if cnpj in _cache_cnpj:
        return _cache_cnpj[cnpj]

    try:
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "EFD-Automacao/1.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8"))

        cod = str(data.get("codigo_municipio_ibge", "")).strip()
        if cod and cod != "0":
            _cache_cnpj[cnpj] = cod
            return cod
    except Exception:
        pass

    # Fallback: tenta a ReceitaWS
    try:
        url2 = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
        req2 = urllib.request.Request(
            url2,
            headers={"User-Agent": "EFD-Automacao/1.0"},
        )
        with urllib.request.urlopen(req2, timeout=8) as r2:
            data2 = json.loads(r2.read().decode("utf-8"))
        # ReceitaWS retorna municipio como texto; buscamos o código via IBGE API
        municipio = data2.get("municipio", "")
        uf = data2.get("uf", "")
        if municipio and uf:
            cod = _buscar_cod_ibge(municipio, uf)
            if cod:
                _cache_cnpj[cnpj] = cod
                return cod
    except Exception:
        pass

    # Se tudo falhar, retorna 9999999 (padrão SPED para município não informado)
    _cache_cnpj[cnpj] = "9999999"
    return "9999999"


def _buscar_cod_ibge(municipio: str, uf: str) -> str:
    """Busca o código IBGE de um município pelo nome e UF via API do IBGE."""
    try:
        nome_enc = urllib.parse.quote(municipio)
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
        req = urllib.request.Request(url, headers={"User-Agent": "EFD-Automacao/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            municipios = json.loads(r.read().decode("utf-8"))
        nome_norm = municipio.upper().strip()
        for m in municipios:
            if m.get("nome", "").upper().strip() == nome_norm:
                return str(m.get("id", ""))
    except Exception:
        pass
    return ""


# Importa urllib.parse separadamente (necessário para quote)
import urllib.parse


def build_bloco0(notas: list[NotaFiscal], dt_ini: str, dt_fin: str,
                 callback_progresso=None) -> list[str]:
    """
    callback_progresso(atual, total, msg): função opcional para atualizar
    a barra de progresso da UI durante a consulta de municípios.
    """
    linhas = []

    # 0000
    linhas.append(montar_linha(
        "0000", "006", "0", "", "",
        dt_ini, dt_fin,
        EMPRESA["NOME"], EMPRESA["CNPJ"],
        EMPRESA["UF"], EMPRESA["COD_MUN"],
        EMPRESA["SUFRAMA"], EMPRESA["IND_SIT_ESP"],
        EMPRESA["IND_APUR_IPI"],
    ))

    linhas.append("|0001|0|")

    # 0100
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
        i["REC_BRU_NCUM_TRIB_MI"], i["REC_BRU_NCUM_NT_MI"],
        i["REC_BRU_NCUM_EXP"], i["REC_BRU_CUM"], i["REC_BRU_TOTAL"],
    ))

    # 0140
    linhas.append(montar_linha(
        "0140",
        EMPRESA["CNPJ"], EMPRESA["NOME"], EMPRESA["CNPJ"],
        EMPRESA["UF"], "", EMPRESA["COD_MUN"],
        EMPRESA["INSCR_MUN"], EMPRESA["SUFRAMA"],
    ))

    # 0150 — busca COD_MUN automaticamente para cada participante
    participantes = {}
    for nota in notas:
        cnpj = nota.cnpj.strip()
        if not cnpj or int(cnpj) == 0 or len(cnpj) < 11:
            continue
        if cnpj not in participantes:
            participantes[cnpj] = nota.razao

    total_part = len(participantes)
    for idx, (cnpj, razao) in enumerate(sorted(participantes.items()), 1):
        if callback_progresso:
            callback_progresso(idx, total_part, f"Buscando município {idx}/{total_part}...")

        cod_mun = _buscar_municipio(cnpj)

        linhas.append(montar_linha(
            "0150",
            cnpj,       # COD_PART
            razao,      # NOME
            "1058",     # COD_PAIS — Brasil
            cnpj,       # CNPJ
            "",         # CPF
            "",         # IE
            cod_mun,    # COD_MUN — buscado automaticamente
            "",         # NUM_SUF
            "",         # END
            "",         # NUM
            "",         # COMPL
            "",         # BAI
        ))
        time.sleep(0.2)  # respeita o rate limit da API

    # 0190
    for um, descr in UNIDADES:
        linhas.append(montar_linha("0190", um, descr))

    # 0200 — 11 campos (sem CEST)
    for item in ITENS:
        linhas.append(montar_linha("0200", *item))

    # 0500
    for conta in CONTAS:
        linhas.append(montar_linha("0500", *conta))

    # 0990
    linhas.append(f"|0990|{len(linhas) + 1}|")
    return linhas
