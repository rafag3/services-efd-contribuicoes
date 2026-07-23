"""
efd_writer.py — Orquestra a montagem final do TXT da EFD Contribuições
"""

from domain.models import NotaFiscal
from builders.bloco0_builder import build_bloco0
from builders.blocoA_builder import build_blocoA
from builders.blocoF_builder import build_blocoF, _agrupar_retencoes
from builders.blocoM_builder import build_blocoM
from builders.bloco1_builder import build_bloco1
from builders.bloco9_builder import build_bloco9


def gerar_efd(notas: list[NotaFiscal], dt_ini: str, dt_fin: str,
              callback_progresso=None) -> bytes:
    """
    Gera o TXT completo da EFD Contribuições.
    callback_progresso(atual, total, msg): atualiza a UI durante busca de municípios.
    """
    f600s = _agrupar_retencoes(notas)

    todas = []
    todas += build_bloco0(notas, dt_ini, dt_fin, callback_progresso)
    todas += build_blocoA(notas)
    todas += ["|C001|1|", "|C990|2|"]
    todas += ["|D001|1|", "|D990|2|"]
    todas += build_blocoF(notas)
    todas += ["|I001|1|", "|I990|2|"]
    todas += build_blocoM(notas, f600s)
    todas += ["|P001|1|", "|P990|2|"]
    todas += build_bloco1(notas)
    todas += build_bloco9(todas)

    return ("\r\n".join(todas) + "\r\n").encode("latin-1", errors="replace")
