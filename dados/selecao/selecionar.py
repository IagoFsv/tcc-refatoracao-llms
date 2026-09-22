"""Selecao das instancias da fase 1: os trechos do dataset de Zhang et al. (2024).

O universo NAO e tudo o que o Pysmell acha nos 311 arquivos do Zhang (isso
daria 333 trechos dos 4 smells). E o recorte que o proprio artigo manteve:
das 687 deteccoes, so 102 sao codigo gerado pelo Copilot, e sao essas que
estao em `results of RQ1.xlsx`. Nos 4 smells do estudo, sao 89 ocorrencias em
83 trechos distintos. Usar as 333 misturaria codigo escrito por humano e
quebraria a proveniencia que a monografia afirma.

Nao ha sorteio: sem teto de amostra (decisao de 22/09/2026), entram os 83.
A planilha diz QUAIS trechos; o Pysmell portado diz as METRICAS de cada um e
serve de conferencia: se algum trecho da planilha nao for reproduzido pelo
porte, o script falha em vez de emitir uma lista pela metade.

Uso:
    python -m dados.selecao.selecionar              # grava o CSV padrao
    python -m dados.selecao.selecionar --conferir   # so confere, nao grava
"""

import argparse
import csv
import os
import sys
from collections import Counter, defaultdict

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, RAIZ)

from dados.pysmell import validar_porte  # noqa: E402
from dados.pysmell._xlsx import read  # noqa: E402
from dados.pysmell.detectar import detectar_arquivo  # noqa: E402

PLANILHA = os.path.join(validar_porte.RAIZ, "results of RQ1.xlsx")
SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_zhang.csv")

# Ordem fixa dos smells na numeracao dos ids. Nao alfabetica: e a ordem em que
# os smells aparecem na monografia. Mudar isso renumera todas as instancias.
ORDEM = ("LM", "LPL", "LLF", "MNC")

CAMPOS = ["id", "smell", "arquivo", "linha", "metricas", "ocorrencias"]


def trechos_da_planilha(todos):
    """Le a planilha RQ1 e devolve {(caminho, linha, smell): n_ocorrencias}.

    Agrupa por (arquivo, linha, smell) porque a unidade deste estudo e o trecho
    a refatorar, e o proprio artigo (secao 3.2.2) diz que um mesmo trecho pode
    apresentar o mesmo smell mais de uma vez. O caso concreto e a linha 1473 de
    argos_ai_adventure.py, que aparece duas vezes em LLF.
    """
    ocorrencias = Counter()
    sem_arquivo = []
    for linha in read(PLANILHA)["Detected Code Smells"][1:]:
        if len(linha) < 4 or linha[3] not in validar_porte.NOMES:
            continue
        caminho = validar_porte.localizar(linha[0], linha[1], todos)
        if caminho is None:
            sem_arquivo.append(linha[1])
            continue
        ocorrencias[(caminho, int(linha[2]), validar_porte.NOMES[linha[3]])] += 1
    if sem_arquivo:
        raise SystemExit(
            "arquivos da planilha que nao existem no disco: %s\n"
            "Baixe o dataset do Zenodo (ver dados/pysmell/README.md)." % sem_arquivo
        )
    return ocorrencias


def metricas_dos_arquivos(caminhos):
    """Roda o porte so nos arquivos que interessam e indexa por (caminho, linha, smell)."""
    medidas = {}
    for caminho in sorted(caminhos):
        for item in detectar_arquivo(caminho, "tuning"):
            medidas[(caminho, item["linha"], item["smell"])] = item["metricas"]
    return medidas


def montar():
    """Devolve a lista de instancias, ja com id, ou aborta se o porte divergir."""
    todos = list(validar_porte.todos_py())
    ocorrencias = trechos_da_planilha(todos)
    medidas = metricas_dos_arquivos({c for c, _, _ in ocorrencias})

    faltando = sorted(set(ocorrencias) - set(medidas))
    if faltando:
        for caminho, linha, smell in faltando:
            print("NAO REPRODUZIDO: %s:%d %s" % (caminho.split("/files/")[1], linha, smell))
        raise SystemExit(
            "\n%d trecho(s) da planilha nao sairam do Pysmell portado. A lista nao "
            "foi gravada: rode dados/pysmell/validar_porte.py e resolva a divergencia "
            "antes de seguir." % len(faltando)
        )

    por_smell = defaultdict(list)
    for chave in ocorrencias:
        por_smell[chave[2]].append(chave)

    instancias = []
    for smell in ORDEM:
        # Ordena por arquivo e linha para que o id de cada instancia seja
        # sempre o mesmo, rodando quantas vezes for.
        for n, chave in enumerate(sorted(por_smell[smell]), start=1):
            caminho, linha, _ = chave
            instancias.append({
                "id": "%s-%02d" % (smell, n),
                "smell": smell,
                "arquivo": caminho.split("/files/")[1],
                "linha": linha,
                "metricas": medidas[chave],
                "ocorrencias": ocorrencias[chave],
            })
    return instancias


def main(argv=None):
    p = argparse.ArgumentParser(description="Seleciona as instancias da fase 1 (Zhang).")
    p.add_argument("--conferir", action="store_true",
                   help="so confere e resume, sem gravar o CSV")
    p.add_argument("--saida", default=SAIDA, help="caminho do CSV de saida")
    args = p.parse_args(argv)

    instancias = montar()
    contagem = Counter(i["smell"] for i in instancias)
    print("trechos selecionados: %d" % len(instancias))
    for smell in ORDEM:
        print("  %-4s %2d" % (smell, contagem[smell]))
    repetidos = [i for i in instancias if i["ocorrencias"] > 1]
    print("ocorrencias na planilha: %d (%d trecho(s) com o smell repetido)"
          % (sum(i["ocorrencias"] for i in instancias), len(repetidos)))
    for i in repetidos:
        print("  %s %s:%d (%dx)" % (i["id"], i["arquivo"], i["linha"], i["ocorrencias"]))

    if args.conferir:
        return 0
    with open(args.saida, "w", newline="", encoding="utf-8") as fh:
        escritor = csv.DictWriter(fh, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(instancias)
    print("\ngravado: %s" % args.saida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
