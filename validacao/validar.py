"""
Loop da validacao (etapa 5) sobre o codigo extraido de uma fase.

Le o `_extraidos/extracao.csv` da fase e, para cada geracao, responde:
  preservou   os 3 testes da instancia passam sobre o codigo extraido;
  removeu     o Pysmell nao detecta mais o smell da instancia.

Regras (fixadas pelo Iago em 27/10/2026, antes de ver qualquer resultado):
  - "sem codigo" na extracao: nao preservou, removeu fica vazio;
  - codigo que o ast.parse recusa: nao preservou, motivo "sintaxe", removeu
    fica vazio (o Pysmell nao mede o que nao parseia);
  - pytest que passa de TIMEOUT segundos: nao preservou, motivo "timeout";
  - removeu e medido em todo codigo que parseia, preservando ou nao; a
    analise filtra pelos que preservaram.

Os testes e as unidades sao os da etapa 3, sem nenhuma alteracao. Retomavel:
geracao ja validada no csv nao roda de novo. No fim, lista as instancias
suspeitas (nenhuma geracao preservou, ou nenhuma removeu o smell).

Saida, em resultados/validacao/<fase>/:
    validacao.csv   uma linha por geracao
    suspeitas.csv   instancias sinalizadas
    sessoes.jsonl   commit, timeout e versoes de cada rodada

Uso:
    python -m validacao.validar --amostra 30   # testa, so imprime
    python -m validacao.validar                # fase 1 inteira
"""

import argparse
import ast
import csv
import datetime
import json
import sys
import time
import warnings
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from adaptacao.checklist import _ambiente, _selecao
from geracao.gerar import _commit
from validacao.conferir import conferir

RAIZ = Path(__file__).resolve().parents[1]
FASE = "fase1"
EXTRAIDOS = RAIZ / "resultados" / "geracoes" / FASE / "_extraidos"
SAIDA = RAIZ / "resultados" / "validacao" / FASE

TIMEOUT = 60  # segundos por geracao (os 3 testes juntos)

COLUNAS = ["identificador", "modelo", "instancia", "smell", "tecnica", "execucao",
           "seed", "extracao", "preservou", "motivo", "testes", "removeu",
           "restantes", "outros", "segundos"]


def _compila(caminho):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            ast.parse(caminho.read_text(encoding="utf-8"))
        except (SyntaxError, ValueError):
            return False
    return True


def validar(linha, inst):
    """Linha do validacao.csv para uma linha do extracao.csv."""
    base = {c: linha[c] for c in ("identificador", "modelo", "instancia", "smell",
                                  "tecnica", "execucao", "seed")}
    base.update(extracao=linha["situacao"], testes="", removeu="",
                restantes="", outros="", segundos=0)
    if not linha["arquivo"]:
        return {**base, "preservou": 0, "motivo": "sem codigo"}
    caminho = EXTRAIDOS.parent / linha["arquivo"]
    if not _compila(caminho):
        return {**base, "preservou": 0, "motivo": "sintaxe"}
    inicio = time.perf_counter()
    res = conferir(inst, caminho, timeout=TIMEOUT)
    if res["preservou"]:
        motivo = ""
    elif res["testes"] == "timeout":
        motivo = "timeout"
    else:
        motivo = "testes"
    return {**base, "preservou": int(res["preservou"]), "motivo": motivo,
            "testes": res["testes"], "removeu": int(res["removeu"]),
            "restantes": " | ".join(res["restantes"]), "outros": " | ".join(res["outros"]),
            "segundos": round(time.perf_counter() - inicio, 1)}


def _suspeitas(linhas):
    por_inst = defaultdict(list)
    for l in linhas:
        por_inst[l["instancia"]].append(l)
    saida = []
    for ident, ls in sorted(por_inst.items()):
        preservaram = sum(int(l["preservou"]) for l in ls)
        removeram = sum(l["removeu"] == "1" or l["removeu"] == 1 for l in ls)
        motivos = [m for m, n in (("nenhuma preservou", preservaram),
                                  ("nenhuma removeu", removeram)) if n == 0]
        if motivos:
            saida.append({"instancia": ident, "smell": ls[0]["smell"], "geracoes": len(ls),
                          "preservaram": preservaram, "removeram": removeram,
                          "motivo": "; ".join(motivos)})
    return saida


def main(argv=None):
    p = argparse.ArgumentParser(description="Valida o codigo extraido de uma fase.")
    p.add_argument("--amostra", type=int, metavar="N",
                   help="valida N geracoes espalhadas e so imprime, sem gravar nada")
    p.add_argument("--jobs", type=int, default=4, help="pytest em paralelo (padrao 4)")
    args = p.parse_args(argv)

    with open(EXTRAIDOS / "extracao.csv", encoding="utf-8", newline="") as fh:
        extracao = list(csv.DictReader(fh))
    selecao = _selecao()
    tabela = SAIDA / "validacao.csv"

    if args.amostra:
        passo = max(1, len(extracao) // args.amostra)
        pendentes = extracao[::passo][:args.amostra]
        feitas = []
    else:
        commit = _commit(exigir_limpa=True)
        SAIDA.mkdir(parents=True, exist_ok=True)
        feitas = []
        if tabela.exists():
            with open(tabela, encoding="utf-8", newline="") as fh:
                feitas = list(csv.DictReader(fh))
        ja = {(l["modelo"], l["identificador"]) for l in feitas}
        pendentes = [l for l in extracao if (l["modelo"], l["identificador"]) not in ja]
        with open(SAIDA / "sessoes.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "inicio_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "commit": commit, "timeout_s": TIMEOUT, "jobs": args.jobs,
                "pendentes": len(pendentes), "ambiente": _ambiente()},
                ensure_ascii=False) + "\n")

    print(f"{len(extracao)} geracoes, {len(feitas)} ja validadas, {len(pendentes)} a validar")
    novo = not tabela.exists()
    fh = None if args.amostra else open(tabela, "a", encoding="utf-8", newline="")
    try:
        w = csv.DictWriter(fh, fieldnames=COLUNAS) if fh else None
        if w and novo:
            w.writeheader()
        with ThreadPoolExecutor(max_workers=args.jobs) as ex:
            futuros = [ex.submit(validar, l, selecao[l["instancia"]]) for l in pendentes]
            for i, f in enumerate(as_completed(futuros), start=1):
                linha = f.result()
                feitas.append(linha)
                if w:
                    w.writerow(linha)
                    fh.flush()
                if args.amostra or i % 50 == 0 or i == len(pendentes):
                    print(f"  [{i}/{len(pendentes)}] {linha['modelo']:9} {linha['identificador']:32}"
                          f" preservou {linha['preservou']} removeu {'-' if linha['removeu'] == '' else linha['removeu']}"
                          f" {linha['motivo'] or ''} {linha['testes']}")
    finally:
        if fh:
            fh.close()

    if not args.amostra:
        # Reordena o csv final, para ficar estavel entre rodadas.
        feitas.sort(key=lambda l: (l["modelo"], l["identificador"]))
        with open(tabela, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=COLUNAS)
            w.writeheader()
            w.writerows(feitas)

    total = len(feitas)
    pres = sum(int(l["preservou"]) for l in feitas)
    print(f"\npreservaram {pres}/{total}")
    if len(feitas) == len(extracao):
        susp = _suspeitas(feitas)
        if not args.amostra:
            with open(SAIDA / "suspeitas.csv", "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=["instancia", "smell", "geracoes",
                                                   "preservaram", "removeram", "motivo"])
                w.writeheader()
                w.writerows(susp)
        print(f"instancias suspeitas: {len(susp)}")
        for s in susp:
            print(f"  {s['instancia']}: {s['motivo']} ({s['preservaram']} preservaram,"
                  f" {s['removeram']} removeram, de {s['geracoes']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
