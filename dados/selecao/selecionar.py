"""Selecao das instancias da fase 1: os trechos do dataset de Zhang et al. (2024).

O universo NAO e tudo o que o Pysmell acha nos 311 arquivos do Zhang (isso
daria 333 trechos dos 4 smells). E o recorte que o proprio artigo manteve:
das 687 deteccoes, so 102 sao codigo gerado pelo Copilot, e sao essas que
estao em `results of RQ1.xlsx`. Nos 4 smells do estudo, sao 89 ocorrencias em
83 trechos distintos. Usar as 333 misturaria codigo escrito por humano e
quebraria a proveniencia que a monografia afirma.

A instancia e a FUNCAO que contem o smell, nao a linha (decisao de
29/09/2026). Para LM e LPL da no mesmo, porque o Pysmell mede a funcao
inteira. Para MNC nao: a metrica e da expressao, e uma funcao cheia de JSON
aninhado dispara varias linhas (o _process_data de GuardianRanks.py tem 8).
Contar por linha mandaria o mesmo codigo varias vezes ao modelo e contaria
como observacoes independentes. Codigo de modulo, fora de qualquer funcao,
agrupa como "<modulo>".

A funcao envolvente e a MAIS EXTERNA (funcao de modulo ou metodo de classe),
nao a mais interna (decisao de 01/10/2026). Funcao aninhada nao sai sozinha
sem mudar o recuo, o que quebra o trecho verbatim, e a funcao que a contem ja
a leva junto: contar as duas mandaria o mesmo arquivo duas vezes. So acontece
no LPL de first_pygame.py (heapify dentro de simulate_heapsort; partition e
quicksort dentro de simulate_quicksort). Agrupando assim, os 83 trechos viram
65 instancias: MNC de 36 para 21, LPL de 22 para 19.

Nao ha sorteio: sem teto de amostra (decisao de 22/09/2026), entram todas.
A planilha diz QUAIS trechos; o Pysmell portado diz as METRICAS de cada um e
serve de conferencia: se algum trecho da planilha nao for reproduzido pelo
porte, o script falha em vez de emitir uma lista pela metade.

Uso:
    python -m dados.selecao.selecionar              # grava o CSV padrao
    python -m dados.selecao.selecionar --conferir   # so confere, nao grava
"""

import argparse
import ast
import csv
import os
import sys
import warnings
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

# linhas e metricas sao listas quando a funcao tem mais de um trecho:
#   linhas   = "60;61;62"
#   metricas = "60:LEC=4|61:LEC=3|62:LEC=3"
CAMPOS = ["id", "smell", "arquivo", "funcao", "linha_funcao", "linhas",
          "metricas", "ocorrencias"]


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


def funcao_envolvente(caminho, linha, _cache={}):
    """Devolve (linha_de_inicio, nome) da funcao mais externa que contem a linha.

    Funcao aninhada conta como parte da funcao que a contem (ver o cabecalho).

    Identifica a funcao pela linha de inicio, nao pelo nome: ha metodos
    homonimos em classes diferentes do mesmo arquivo (my_image.py tem dois
    draw_line; cryptocurrency.py e network.py tem dois __init__ cada).
    Fora de qualquer funcao devolve (0, "<modulo>").
    """
    if caminho not in _cache:
        with open(caminho, encoding="utf-8", errors="replace") as fh:
            codigo = fh.read()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            _cache[caminho] = ast.parse(codigo)
    melhor = None
    for no in ast.walk(_cache[caminho]):
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if no.lineno <= linha <= no.end_lineno:
                if melhor is None or no.lineno < melhor.lineno:
                    melhor = no
    return (melhor.lineno, melhor.name) if melhor else (0, "<modulo>")


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

    # (smell, caminho, linha_funcao) -> lista de trechos daquela funcao
    grupos = defaultdict(list)
    nomes = {}
    for chave in ocorrencias:
        caminho, linha, smell = chave
        inicio, nome = funcao_envolvente(caminho, linha)
        grupos[(smell, caminho, inicio)].append(chave)
        nomes[(caminho, inicio)] = nome

    instancias = []
    for smell in ORDEM:
        # Ordena pelo arquivo e pela primeira linha detectada, para que o id
        # seja sempre o mesmo, rodando quantas vezes for. E a mesma chave da
        # versao por linha, entao LM e LLF (que nao colapsam) mantem os ids
        # que ja tinham; no LPL, os ids a partir do 04 andam (01/10/2026).
        chaves = sorted(
            (k for k in grupos if k[0] == smell),
            key=lambda k: (k[1], min(linha for _, linha, _ in grupos[k])),
        )
        for n, chave in enumerate(chaves, start=1):
            _, caminho, inicio = chave
            trechos = sorted(grupos[chave])
            instancias.append({
                "id": "%s-%02d" % (smell, n),
                "smell": smell,
                "arquivo": caminho.split("/files/")[1],
                "funcao": nomes[(caminho, inicio)],
                "linha_funcao": inicio,
                "linhas": ";".join(str(linha) for _, linha, _ in trechos),
                "metricas": "|".join("%d:%s" % (t[1], medidas[t]) for t in trechos),
                "ocorrencias": sum(ocorrencias[t] for t in trechos),
            })
    return instancias


def main(argv=None):
    p = argparse.ArgumentParser(description="Seleciona as instancias da fase 1 (Zhang).")
    p.add_argument("--conferir", action="store_true",
                   help="so confere e resume, sem gravar o CSV")
    p.add_argument("--saida", default=SAIDA, help="caminho do CSV de saida")
    args = p.parse_args(argv)

    instancias = montar()
    n_trechos = Counter()
    for i in instancias:
        n_trechos[i["smell"]] += len(i["linhas"].split(";"))
    contagem = Counter(i["smell"] for i in instancias)
    print("%-5s %8s %11s" % ("smell", "trechos", "instancias"))
    for smell in ORDEM:
        print("%-5s %8d %11d" % (smell, n_trechos[smell], contagem[smell]))
    print("%-5s %8d %11d" % ("total", sum(n_trechos.values()), len(instancias)))
    print("ocorrencias na planilha: %d" % sum(i["ocorrencias"] for i in instancias))

    agrupadas = [i for i in instancias if ";" in i["linhas"]]
    print()
    print("instancias com mais de um trecho na mesma funcao: %d" % len(agrupadas))
    for i in agrupadas:
        print("  %-6s %s  %s:%d  linhas %s"
              % (i["id"], i["arquivo"], i["funcao"], i["linha_funcao"], i["linhas"]))

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
