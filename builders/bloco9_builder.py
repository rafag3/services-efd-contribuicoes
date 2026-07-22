"""bloco9_builder.py — Monta 9001, 9900, 9990, 9999 (automático)"""

from collections import Counter


def build_bloco9(linhas_anteriores: list[str]) -> list[str]:
    contagem: Counter = Counter()
    for linha in linhas_anteriores:
        s = linha.strip().strip("|")
        tipo = s.split("|")[0]
        if tipo:
            contagem[tipo] += 1

    contagem["9001"] = 1
    contagem["9990"] = 1
    contagem["9999"] = 1
    n_9900 = len(contagem) + 1
    contagem["9900"] = n_9900

    linhas9 = ["|9001|0|"]
    for tipo in sorted(contagem.keys()):
        linhas9.append(f"|9900|{tipo}|{contagem[tipo]}|")

    n_bloco9 = 1 + n_9900 + 1 + 1
    linhas9.append(f"|9990|{n_bloco9}|")
    total = len(linhas_anteriores) + n_bloco9
    linhas9.append(f"|9999|{total}|")
    return linhas9
