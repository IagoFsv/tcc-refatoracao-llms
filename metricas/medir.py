"""
Metricas de qualidade (etapa 6) do original e das refatoracoes que preservaram.

Mede, com as mesmas ferramentas, as unidades originais da fase e o codigo
extraido de toda geracao com preservou = 1 no validacao.csv.

Decisoes do Iago (09/11/2026, antes de medir qualquer saida):
  - escopo: o arquivo inteiro (trecho + andaime), em todas as metricas;
  - cc_max: a maior CC do Radon entre as funcoes do arquivo (de modulo,
    metodos e aninhadas). Classe nao conta: a CC dela e a soma dos metodos;
  - LLF e MNC: metricas do Pysmell do maior caso no arquivo; vazio quando
    nao ha o que medir ("nao se aplica", nunca 0).

Colunas medidas:
  cc_max        Radon, maior CC entre as funcoes
  mi, faixa_mi  Radon, indice de manutenibilidade (0 a 100) e faixa A/B/C,
                com o padrao do Radon (string de varias linhas conta como
                comentario)
  volume        Radon, volume de Halstead do arquivo. O Radon so conta
                operadores aritmeticos, unarios, logicos, de comparacao e
                `+=`; sem nenhum, o volume e 0 e o MI vem 100 por convencao,
                sem calculo. O que fazer com esses casos esta pendente
                (conversa com a Carla); a coluna permite aplicar a decisao
                na analise sem medir de novo
  pylint        nota do Pylint (0 a 10), configuracao padrao
  noc/par/noo   so LLF: a lambda de maior NOC
  lec           so MNC: o maior encadeamento de indices
  dnc/nct       so MNC: o container de maior DNC (empate: maior NCT)

O Pylint roda numa pasta temporaria, com o arquivo copiado com o nome da
unidade original (LM_01.py etc.), para o nome do modulo ser o mesmo no
original e no refatorado, e com um arquivo de configuracao vazio, para
nenhuma configuracao do computador entrar.

A variacao percentual e as medias ficam para a etapa 7 (analise/).

Saida, em resultados/metricas/<fase>/:
    metricas.csv    uma linha por arquivo medido (originais e refatorados)
    sessoes.jsonl   commit e versoes das ferramentas de cada rodada

Uso:
    python -m metricas.medir --amostra 10   # testa, so imprime
    python -m metricas.medir                # fase 1 inteira
"""

import argparse
import csv
import datetime
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from radon.complexity import cc_visit
from radon.metrics import h_visit, mi_rank, mi_visit

from adaptacao.checklist import _caminhos, _selecao
from dados.pysmell.detectar import detectar_arquivo
from geracao.gerar import _commit
from validacao.validar import EXTRAIDOS, FASE, SAIDA as VALIDACAO

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "resultados" / "metricas" / FASE

PACOTES = ("radon", "pylint", "astroid", "astunparse")
TIMEOUT_PYLINT = 120  # segundos por arquivo

COLUNAS = ["tipo", "identificador", "modelo", "instancia", "smell", "tecnica",
           "execucao", "seed", "cc_max", "mi", "faixa_mi", "volume", "pylint",
           "noc", "par", "noo", "lec", "dnc", "nct"]


def _ambiente():
    versoes = [f"Python {platform.python_version()}"]
    for pacote in PACOTES:
        versoes.append(f"{pacote} {importlib.metadata.version(pacote)}")
    return "; ".join(versoes)


# ---------------------------------------------------------------- Radon

def _funcoes(blocos):
    """Funcoes, metodos e funcoes aninhadas (o Radon guarda estas em closures)."""
    for b in blocos:
        if hasattr(b, "methods"):  # classe
            yield from _funcoes(b.methods)
        else:
            yield b
            yield from _funcoes(b.closures)


def _radon(codigo):
    complexidades = [f.complexity for f in _funcoes(cc_visit(codigo))]
    mi = mi_visit(codigo, multi=True)
    return {"cc_max": max(complexidades) if complexidades else "",
            "mi": round(mi, 2), "faixa_mi": mi_rank(mi),
            "volume": round(h_visit(codigo).total.volume, 2)}


# ---------------------------------------------------------------- Pylint

def _pylint(caminho, nome):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        shutil.copy(caminho, Path(tmp, nome))
        rc = Path(tmp, "vazio.rc")
        rc.write_text("", encoding="utf-8")
        env = {k: v for k, v in os.environ.items() if k != "PYLINTRC"}
        r = subprocess.run(
            [sys.executable, "-m", "pylint", f"--rcfile={rc}", "--persistent=n",
             "--output-format=json2", nome],
            cwd=tmp, capture_output=True, text=True, timeout=TIMEOUT_PYLINT, env=env)
    try:
        return round(json.loads(r.stdout)["statistics"]["score"], 2)
    except (ValueError, KeyError) as erro:
        raise RuntimeError(f"Pylint sem nota para {caminho}: {r.stderr[-500:]}") from erro


# ---------------------------------------------------------------- Pysmell

def _valores(deteccao):
    return {k.lower(): int(v) for k, v in
            (par.split("=") for par in deteccao["metricas"].split(";"))}


def _pysmell(caminho, smell):
    vazio = {c: "" for c in ("noc", "par", "noo", "lec", "dnc", "nct")}
    if smell not in ("LLF", "MNC"):
        return vazio
    medidas = [_valores(d) for d in
               detectar_arquivo(str(caminho), smells=(smell,), incluir_abaixo=True)]
    if smell == "LLF":
        if medidas:
            maior = max(medidas, key=lambda m: m["noc"])
            vazio.update(noc=maior["noc"], par=maior["par"], noo=maior["noo"])
        return vazio
    lecs = [m["lec"] for m in medidas if "lec" in m]
    conts = [m for m in medidas if "dnc" in m]
    if lecs:
        vazio["lec"] = max(lecs)
    if conts:
        maior = max(conts, key=lambda m: (m["dnc"], m["nct"]))
        vazio.update(dnc=maior["dnc"], nct=maior["nct"])
    return vazio


# ---------------------------------------------------------------- medicao

def medir(base, caminho, inst):
    codigo = Path(caminho).read_text(encoding="utf-8")
    _, unidade, _, _ = _caminhos(inst)
    return {**base, **_radon(codigo), "pylint": _pylint(caminho, unidade.name),
            **_pysmell(caminho, inst["smell"])}


def _tarefas(selecao):
    """(base, caminho, inst) dos originais e das refatoracoes que preservaram."""
    with open(VALIDACAO / "validacao.csv", encoding="utf-8", newline="") as fh:
        validacao = list(csv.DictReader(fh))
    ids = sorted({l["instancia"] for l in validacao})
    tarefas = []
    for ident in ids:
        inst = selecao[ident]
        base = {c: "" for c in COLUNAS}
        base.update(tipo="original", identificador=ident, instancia=ident, smell=inst["smell"])
        tarefas.append((base, _caminhos(inst)[1], inst))
    for l in validacao:
        if l["preservou"] != "1":
            continue
        base = {c: "" for c in COLUNAS}
        base.update({c: l[c] for c in ("identificador", "modelo", "instancia", "smell",
                                       "tecnica", "execucao", "seed")}, tipo="refatorado")
        tarefas.append((base, EXTRAIDOS / l["modelo"] / f"{l['identificador']}.py",
                        selecao[l["instancia"]]))
    return tarefas


def main(argv=None):
    p = argparse.ArgumentParser(description="Metricas do original e das refatoracoes que preservaram.")
    p.add_argument("--amostra", type=int, metavar="N",
                   help="mede N arquivos espalhados e so imprime, sem gravar nada")
    p.add_argument("--jobs", type=int, default=4, help="arquivos em paralelo (padrao 4)")
    args = p.parse_args(argv)

    tarefas = _tarefas(_selecao())
    tabela = SAIDA / "metricas.csv"
    if args.amostra:
        tarefas = tarefas[::max(1, len(tarefas) // args.amostra)][:args.amostra]
    else:
        if tabela.exists():
            sys.exit(f"{tabela} ja existe. Resultado medido nao e sobrescrito; "
                     "apague a mao se for mesmo medir de novo.")
        commit = _commit(exigir_limpa=True)
        SAIDA.mkdir(parents=True, exist_ok=True)
        with open(SAIDA / "sessoes.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "inicio_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "commit": commit, "arquivos": len(tarefas), "ambiente": _ambiente()},
                ensure_ascii=False) + "\n")

    print(f"{len(tarefas)} arquivos a medir")
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        linhas = list(ex.map(lambda t: medir(*t), tarefas))

    if args.amostra:
        for l in linhas:
            print(f"  {l['tipo']:10} {l['modelo'] or '-':8} {l['identificador']:32} "
                  f"cc_max {l['cc_max']} mi {l['mi']} ({l['faixa_mi']}) vol {l['volume']} pylint {l['pylint']} "
                  + " ".join(f"{c}={l[c]}" for c in ("noc", "par", "noo", "lec", "dnc", "nct")
                             if l[c] != ""))
        return 0

    linhas.sort(key=lambda l: (l["tipo"] != "original", l["modelo"], l["identificador"]))
    with open(tabela, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUNAS)
        w.writeheader()
        w.writerows(linhas)
    n_orig = sum(l["tipo"] == "original" for l in linhas)
    print(f"{n_orig} originais e {len(linhas) - n_orig} refatorados em {tabela}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
