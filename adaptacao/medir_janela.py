"""Mede o prompt de cada instancia em cada modelo, para o criterio da janela.

Criterio (decisao do Iago, 21/10/2026): o prompt tem que caber em
num_ctx - num_predict tokens em TODOS os modelos, senao prompt + saida passa
da janela. Instancia que nao cabe sai para todos, antes da geracao.

Metodo: o prompt montado por geracao/prompts.py vai ao /api/chat do Ollama
com num_predict 1 e keep_alive 0, e a contagem e o prompt_eval_count da
resposta (template do modelo incluso). keep_alive 0 descarrega o modelo a
cada chamada, para o cache de prefixo nao reduzir a contagem. Por padrao so
o Few-Shot e medido: com o mesmo nucleo e um exemplo a mais, e sempre o
maior dos tres prompts.

Uso:
    python -m adaptacao.medir_janela                 # todas as instancias
    python -m adaptacao.medir_janela LM-04 MNC-01    # so essas
    --tecnica role|few_shot|chain_of_thought

Grava instancias/janela.csv, uma linha por instancia, com a contagem em cada
modelo. Linhas de instancias que nao foram medidas agora sao mantidas.
"""

import argparse
import csv
import datetime
import sys
from pathlib import Path

import yaml

from geracao import cliente, prompts

RAIZ = Path(__file__).resolve().parent.parent
INSTANCIAS = RAIZ / "instancias"
TABELA = INSTANCIAS / "janela.csv"


def _unidades(ids):
    """{id: caminho da unidade} das instancias com pasta (ou so das pedidas)."""
    todas = {p.parent.name: p for p in sorted(INSTANCIAS.glob("*/*/*.py"))
             if p.stem == p.parent.name.replace("-", "_")}
    desconhecidos = [i for i in ids if i not in todas]
    if desconhecidos:
        sys.exit(f"sem unidade em instancias/: {', '.join(desconhecidos)}")
    return {i: todas[i] for i in ids} if ids else todas


def _contar(cfg, modelo, mensagens):
    corpo = cliente.montar_corpo(cfg, modelo, mensagens, cfg["seeds"][0])
    corpo["options"]["num_predict"] = 1
    corpo["keep_alive"] = 0
    return cliente._post(cfg, "/api/chat", corpo, timeout=cliente.TIMEOUT_S)["prompt_eval_count"]


def _gravar(linhas_novas, colunas):
    existentes = {}
    if TABELA.exists():
        with open(TABELA, encoding="utf-8", newline="") as fh:
            existentes = {l["id"]: l for l in csv.DictReader(fh)}
    existentes.update({l["id"]: l for l in linhas_novas})
    with open(TABELA, "w", encoding="utf-8", newline="") as fh:
        escritor = csv.DictWriter(fh, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(existentes[i] for i in sorted(existentes))


def main(argv=None):
    p = argparse.ArgumentParser(description="Mede o prompt de cada instancia em cada modelo.")
    p.add_argument("ids", nargs="*", help="ids das instancias (padrao: todas as que tem pasta)")
    p.add_argument("--tecnica", default="few_shot", choices=prompts.TECNICAS)
    args = p.parse_args(argv)

    with open(RAIZ / "config.yaml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    limite = cfg["parametros"]["num_ctx"] - cfg["parametros"]["num_predict"]
    modelos = cfg["modelos"]
    unidades = _unidades(args.ids)

    versao = None
    for m in modelos:
        versao = cliente.ambiente(cfg, m)["ollama_versao"]  # aborta se o digest mudou

    colunas = ["id", "smell", "tecnica", *(m["nome"] for m in modelos),
               "maior", "limite", "cabe", "data", "ollama"]
    linhas = []
    for ident, unidade in unidades.items():
        smell = unidade.parent.parent.name
        mensagens = prompts.montar(args.tecnica, smell, unidade.read_text(encoding="utf-8"))
        contagens = {m["nome"]: _contar(cfg, m, mensagens) for m in modelos}
        maior = max(contagens.values())
        linha = {"id": ident, "smell": smell, "tecnica": args.tecnica, **contagens,
                 "maior": maior, "limite": limite, "cabe": "sim" if maior <= limite else "nao",
                 "data": datetime.date.today().isoformat(), "ollama": versao}
        linhas.append(linha)
        # Grava a cada instancia: uma rodada interrompida nao perde o que ja mediu.
        _gravar([linha], colunas)
        print(f"{ident:8} {contagens}  => {'cabe' if maior <= limite else 'NAO CABE'}", flush=True)

    nao_cabem = [l["id"] for l in linhas if l["cabe"] == "nao"]
    print(f"\ntabela: {TABELA.relative_to(RAIZ)}  (limite {limite} tokens)")
    if nao_cabem:
        print(f"nao cabem: {', '.join(nao_cabem)}")
    return 1 if nao_cabem else 0


if __name__ == "__main__":
    sys.exit(main())
