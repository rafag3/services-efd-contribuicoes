"""
bloco9_builder.py — Monta o Bloco 9 (contadores 9900, 9990, 9999)
"""

from collections import Counter


def build_bloco9(linhas_anteriores: list[str]) -> list[str]:
    """
    Recebe todas as linhas geradas antes do Bloco 9 e retorna as linhas
    do Bloco 9, incluindo 9001, todos os 9900, 9990 e 9999.
    """
    # Contagem por tipo de registro
    contagem: Counter = Counter()
    for linha in linhas_anteriores:
        s = linha.strip().strip("|")
        tipo = s.split("|")[0]
        if tipo:
            contagem[tipo] += 1

    # Adiciona os tipos que vão aparecer no próprio bloco 9
    contagem["9001"] = 1
    contagem["9990"] = 1
    contagem["9999"] = 1

    # O número de linhas 9900 = total de tipos únicos + 1 (para o 9900 si mesmo)
    n_9900 = len(contagem) + 1
    contagem["9900"] = n_9900

    # Monta as linhas do bloco 9
    linhas9 = ["|9001|0|"]

    for tipo in sorted(contagem.keys()):
        linhas9.append(f"|9900|{tipo}|{contagem[tipo]}|")

    # 9990 — total de linhas do bloco 9
    n_bloco9 = 1 + n_9900 + 1 + 1  # 9001 + n_9900 + 9990 + 9999
    linhas9.append(f"|9990|{n_bloco9}|")

    # 9999 — total de linhas do arquivo inteiro
    total = len(linhas_anteriores) + n_bloco9
    linhas9.append(f"|9999|{total}|")

    return linhas9
