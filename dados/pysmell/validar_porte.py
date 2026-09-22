"""Confere o porte do Pysmell contra o dataset de Zhang et al. (2024).

O artigo (secao 3.1) diz que o Pysmell foi rodado nos 311 arquivos com a
estrategia Tuning Machine, produzindo 687 deteccoes, das quais 102 foram
mantidas por serem codigo gerado pelo Copilot (57 em Repositories, 45 em Code).
As 102 estao em `results of RQ1.xlsx`.

Este script roda o porte sobre os mesmos arquivos e compara. Serve de
evidencia de que o porte reproduz o detector original, e deve ser rodado de
novo se alguem mexer em astChecker.py, compat.py ou detectar.py.

Uso:
    python -m dados.pysmell.validar_porte
"""

import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _xlsx import read  # noqa: E402
from detectar import DO_ESTUDO, detectar_arquivo  # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dataset_zhang", "dataset")
RAIZ = os.path.normpath(RAIZ).replace(os.sep, "/")
ARQUIVOS = RAIZ + "/files"

# Nomes como aparecem na planilha -> siglas usadas no porte.
NOMES = {
    "Long Method": "LM",
    "Long Parameter List": "LPL",
    "Long Lambda Function": "LLF",
    "Multiply Nested Container": "MNC",
}

# O que o artigo reporta, para comparacao.
ARTIGO = {"total": 687, "Repositories": 57, "Code": 630}


def todos_py():
    """Publica porque dados/selecao/selecionar.py reusa (uma so implementacao)."""
    for raiz, _, nomes in os.walk(ARQUIVOS):
        for nome in sorted(nomes):
            if nome.endswith(".py"):
                yield os.path.join(raiz, nome).replace(os.sep, "/")


def localizar(origem, caminho_planilha, todos):
    """Publica porque dados/selecao/selecionar.py reusa.

    A planilha usa 'code/x.py' e 'repo/a/b.py'; no disco sao Code/ e Repositories/."""
    prefixo = "/Code/" if origem == "code" else "/Repositories/"
    base = os.path.basename(caminho_planilha)
    candidatos = [p for p in todos if prefixo in p and os.path.basename(p) == base]
    if len(candidatos) > 1:
        cauda = caminho_planilha.split("/", 1)[1]
        candidatos = [p for p in candidatos if p.endswith(cauda)] or candidatos
    return candidatos[0] if candidatos else None


def main():
    todos = list(todos_py())
    print("arquivos .py encontrados: %d (artigo: 311)" % len(todos))

    esperado, ocorrencias, sem_arquivo = set(), Counter(), []
    linhas = read(RAIZ + "/results of RQ1.xlsx")["Detected Code Smells"][1:]
    for linha in linhas:
        if len(linha) < 4 or linha[3] not in NOMES:
            continue
        caminho = localizar(linha[0], linha[1], todos)
        if caminho is None:
            sem_arquivo.append(linha[1])
            continue
        sigla = NOMES[linha[3]]
        ocorrencias[sigla] += 1
        esperado.add((caminho, int(linha[2]), sigla))
    print("planilha RQ1: %d ocorrencias dos 4 smells, %d trechos distintos"
          % (sum(ocorrencias.values()), len(esperado)))
    print("  ocorrencias:", dict(ocorrencias))
    print("  trechos distintos:", dict(Counter(s for _, _, s in esperado)))
    if sem_arquivo:
        print("  SEM ARQUIVO NO DISCO:", sem_arquivo)

    detectado, por_pasta, falhas = set(), Counter(), []
    for caminho in todos:
        try:
            linhas_det = detectar_arquivo(caminho, "tuning", smells=None)
        except SyntaxError as erro:
            falhas.append((caminho, erro.msg))
            continue
        for linha in linhas_det:
            por_pasta["Repositories" if "/Repositories/" in caminho else "Code"] += 1
            if linha["smell"] in DO_ESTUDO:
                detectado.add((caminho, linha["linha"], linha["smell"]))

    print("\nporte, estrategia tuning, 10 smells:")
    print("  total: %d (artigo: %d)" % (sum(por_pasta.values()), ARTIGO["total"]))
    for pasta in ("Repositories", "Code"):
        print("  %s: %d (artigo: %d)" % (pasta, por_pasta[pasta], ARTIGO[pasta]))
    if falhas:
        print("  nao parseiam: %d" % len(falhas))
        for caminho, msg in falhas:
            print("    %s (%s)" % (caminho.split("/files/")[1], msg))

    faltando = esperado - detectado
    print("\nreproducao dos trechos do Zhang: %d/%d" % (len(esperado & detectado), len(esperado)))
    for caminho, linha, sigla in sorted(faltando):
        print("  NAO REPRODUZIDO: %s:%d %s" % (caminho.split("/files/")[1], linha, sigla))
    return 0 if not faltando else 1


if __name__ == "__main__":
    sys.exit(main())
