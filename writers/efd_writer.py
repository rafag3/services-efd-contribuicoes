"""
efd_writer.py — Orquestra a montagem final do TXT da EFD Contribuições
"""

from domain.models import NotaFiscal
from builders.bloco0_builder import build_bloco0
from builders.blocoA_builder import build_blocoA
from builders.blocoF_builder import build_blocoF
from builders.blocoM_builder import build_blocoM
from builders.bloco1_builder import build_bloco1, build_blocos_vazios
from builders.bloco9_builder import build_bloco9


def gerar_efd(notas: list[NotaFiscal], dt_ini: str, dt_fin: str) -> bytes:
    """
    Gera o conteúdo completo do TXT da EFD Contribuições.
    Retorna bytes em encoding latin-1 (padrão SPED).
    """
    todas = []

    todas += build_bloco0(notas, dt_ini, dt_fin)
    todas += build_blocoA(notas)

    # Blocos C e D (sem movimento) — inseridos aqui, antes do F
    for bloco in ["C", "D"]:
        todas += [f"|{bloco}001|1|", f"|{bloco}990|2|"]

    todas += build_blocoF(notas)

    # Bloco I (sem movimento)
    todas += ["|I001|1|", "|I990|2|"]

    todas += build_blocoM(notas)

    # Bloco P (sem movimento)
    todas += ["|P001|1|", "|P990|2|"]

    todas += build_bloco1(notas)

    # Bloco 9 — sempre por último
    todas += build_bloco9(todas)

    conteudo = "\r\n".join(todas) + "\r\n"
    return conteudo.encode("latin-1", errors="replace")
