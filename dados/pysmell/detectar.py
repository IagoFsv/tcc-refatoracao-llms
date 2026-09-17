"""Detector de code smells Python (Pysmell portado), estrategia Tuning Machine.

Limiares e regras de combinacao copiados de pysmell/detection/detector.py do
repositorio original (commit 233afeb). O original nao tinha linha de comando:
era um script que lia CSVs de metricas ja gerados. Aqui as duas etapas
(extrair metricas com o astChecker e aplicar limiares) ficam juntas.

Uso:
    python -m dados.pysmell.detectar <arquivo_ou_pasta> [...] [opcoes]

    --estrategia {tuning,experience,statistics}  padrao: tuning
    --todos       detecta os 10 smells do Chen et al. (padrao: so os 4 do estudo)
    --metricas    inclui tambem as medidas abaixo do limiar (para comparar
                  original e refatorado na etapa de metricas)
    --saida CSV   grava em arquivo em vez da saida padrao

Como biblioteca:
    from dados.pysmell.detectar import detectar_arquivo, medir_arquivo
"""

import argparse
import ast
import csv
import os
import sys
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import astChecker  # noqa: E402

# Ordem dos limiares no detector.py original:
# [experience-based, statistics-based, tuning machine]
ESTRATEGIAS = {"experience": 0, "statistics": 1, "tuning": 2}

PAR = [5, 4, 5]
MLOC = [38, 28, 52]
DOC = [3, 4, 4]
CLOC = [29, 59, 37]
LMC = [5, 4, 4]
NBC = [3, 2, 3]
NOC, LPAR, NOO = [48, 82, 73], [3, 3, 4], [7, 13, 15]
TNOC, TNOL = [54, 102, 101], [3, 3, 3]
CNOC, NOFF, CNOO = [62, 131, 92], [3, 3, 3], [8, 24, 22]
LEC, DNC, NCT = [3, 3, 3], [3, 4, 3], [3, 2, 2]

# Codigos que o astChecker usa em result[0], com a sigla do smell.
SMELLS = {
    1: ("LPL", "Long Parameter List"),
    2: ("LM", "Long Method"),
    3: ("LSC", "Long Scope Chaining"),
    4: ("LBCL", "Long Base Class List"),
    5: ("LC", "Large Class"),
    6: ("MNC", "Multiply-Nested Container"),
    9: ("LLF", "Long Lambda Function"),
    10: ("LTCE", "Long Ternary Conditional Expression"),
    11: ("CCC", "Complex Container Comprehension"),
    13: ("LMC", "Long Message Chain"),
}
DO_ESTUDO = ("LM", "LPL", "LLF", "MNC")


def _avaliar(item, k):
    """Devolve (sigla, metricas, passou_no_limiar) para um item do astChecker."""
    codigo = item[0]
    if codigo not in SMELLS:
        return None
    sigla = SMELLS[codigo][0]
    if codigo == 1:
        return sigla, {"PAR": item[3]}, item[3] >= PAR[k]
    if codigo == 2:
        return sigla, {"MLOC": item[3]}, item[3] >= MLOC[k]
    if codigo == 3:
        return sigla, {"DOC": item[3]}, item[3] >= DOC[k]
    if codigo == 4:
        return sigla, {"NBC": item[3]}, item[3] >= NBC[k]
    if codigo == 5:
        return sigla, {"CLOC": item[3]}, item[3] >= CLOC[k]
    if codigo == 13:
        return sigla, {"LMC": item[3]}, item[3] >= LMC[k]
    if codigo == 9:
        m = {"NOC": item[3], "PAR": item[4], "NOO": item[5]}
        return sigla, m, item[3] >= NOC[k] and (item[4] >= LPAR[k] or item[5] >= NOO[k])
    if codigo == 10:
        m = {"NOC": item[3], "NOL": item[4]}
        return sigla, m, item[3] >= TNOC[k] or item[4] >= TNOL[k]
    if codigo == 11:
        m = {"NOC": item[3], "NOFF": item[4], "NOO": item[5]}
        return sigla, m, (item[3] >= CNOC[k] and item[5] >= CNOO[k]) or item[4] >= NOFF[k]
    if codigo == 6:
        # O astChecker emite MNC de duas formas: LEC (encadeamento de indices)
        # ou DNC+NCT (aninhamento de containers).
        if len(item) == 4:
            return sigla, {"LEC": item[3]}, item[3] >= LEC[k]
        m = {"DNC": item[3], "NCT": item[4]}
        return sigla, m, item[3] >= DNC[k] and item[4] >= NCT[k]
    return None


def medir_arquivo(caminho):
    """Roda o astChecker e devolve todas as medidas, com ou sem smell."""
    with open(caminho, encoding="utf-8", errors="replace") as fh:
        codigo = fh.read()
    with warnings.catch_warnings():
        # Codigo de terceiros costuma ter escapes invalidos ("\d" fora de raw
        # string). Isso vira SyntaxWarning no parse e nao interessa aqui.
        warnings.simplefilter("ignore", SyntaxWarning)
        arvore = ast.parse(codigo)
    checker = astChecker.MyAst()
    checker.fileName = caminho
    checker.visit(arvore)
    return checker.result


def detectar_arquivo(caminho, estrategia="tuning", smells=DO_ESTUDO, incluir_abaixo=False):
    """Lista os smells de um arquivo. Levanta SyntaxError se o arquivo nao parseia."""
    k = ESTRATEGIAS[estrategia]
    saida = []
    for item in medir_arquivo(caminho):
        avaliado = _avaliar(item, k)
        if avaliado is None:
            continue
        sigla, metricas, detectado = avaliado
        if smells is not None and sigla not in smells:
            continue
        if not detectado and not incluir_abaixo:
            continue
        saida.append({
            "arquivo": caminho,
            "linha": item[2],
            "smell": sigla,
            "detectado": int(detectado),
            "metricas": ";".join("%s=%s" % (n, v) for n, v in metricas.items()),
        })
    return saida


def _arquivos(alvos):
    for alvo in alvos:
        if os.path.isdir(alvo):
            for raiz, _, nomes in os.walk(alvo):
                for nome in sorted(nomes):
                    if nome.endswith(".py"):
                        yield os.path.join(raiz, nome).replace(os.sep, "/")
        else:
            yield alvo.replace(os.sep, "/")


def main(argv=None):
    p = argparse.ArgumentParser(description="Pysmell portado (Chen et al.), Python 3.")
    p.add_argument("alvos", nargs="+", help="arquivos .py ou pastas")
    p.add_argument("--estrategia", choices=sorted(ESTRATEGIAS), default="tuning")
    p.add_argument("--todos", action="store_true", help="os 10 smells, nao so os 4 do estudo")
    p.add_argument("--metricas", action="store_true", help="inclui medidas abaixo do limiar")
    p.add_argument("--saida", help="arquivo CSV de saida")
    args = p.parse_args(argv)

    smells = None if args.todos else DO_ESTUDO
    linhas, falhas = [], []
    for caminho in _arquivos(args.alvos):
        try:
            linhas.extend(detectar_arquivo(caminho, args.estrategia, smells, args.metricas))
        except SyntaxError as erro:
            falhas.append((caminho, erro))

    destino = open(args.saida, "w", newline="", encoding="utf-8") if args.saida else sys.stdout
    escritor = csv.DictWriter(destino, fieldnames=["arquivo", "linha", "smell", "detectado", "metricas"])
    escritor.writeheader()
    escritor.writerows(linhas)
    if args.saida:
        destino.close()
        print("%d linhas em %s" % (len(linhas), args.saida))

    for caminho, erro in falhas:
        print("nao parseia (%s): %s" % (erro.msg, caminho), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
