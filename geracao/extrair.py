"""
Extracao do codigo refatorado das respostas brutas (entre as etapas 4 e 5).

A resposta bruta (o JSON da geracao) nunca e alterada: a extracao le o JSON
e grava o codigo num arquivo a parte, entao pode ser refeita a qualquer
momento com o mesmo resultado. Regra fixada antes da rodada principal, a
partir do formato das respostas do piloto (Llama 3 usa cerca sem linguagem;
o DeepSeek as vezes responde so com codigo, sem cerca):

  1. Blocos cercados (```), da linguagem python (python, python3 ou py, sem
     diferenciar maiusculas) ou sem linguagem: vale o ULTIMO. Bloco de outra
     linguagem (bash, text...) e ignorado.
  2. Cerca aberta e nunca fechada: o bloco vai da abertura ao fim da resposta.
  3. Resposta sem cerca nenhuma: vale a resposta inteira, se o ast.parse a
     aceitar como Python.
  4. Fora disso: "sem codigo", nada e gravado e a geracao conta como nao
     preservou.

O codigo extraido nao e conferido aqui (nem se compila): isso e a etapa 5.

Saida, dentro da pasta da fase:
    _extraidos/<modelo>/<ID>__<tecnica>__s<seed>.py
    _extraidos/extracao.csv   uma linha por geracao, com a situacao

Uso:
    python -m geracao.extrair                                   # fase 1
    python -m geracao.extrair resultados/geracoes/_piloto/<sessao>
"""

import argparse
import ast
import csv
import json
import re
import sys
import warnings
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FASE1 = RAIZ / "resultados" / "geracoes" / "fase1"

LINGUAGENS = {"", "python", "python3", "py"}

# Cerca no comeco da linha, com linguagem opcional. A de fechamento nao tem
# nada depois das crases.
ABRE = re.compile(r"^```\s*([^\s`]*)")
FECHA = re.compile(r"^```\s*$")

COLUNAS = ["identificador", "modelo", "instancia", "smell", "tecnica", "execucao",
           "seed", "done_reason", "situacao", "linguagem", "blocos", "linhas", "arquivo"]


def blocos(texto):
    """[(linguagem, codigo, fechado)] dos blocos cercados, em ordem."""
    achados, atual = [], None
    for linha in texto.splitlines():
        if atual is None:
            m = ABRE.match(linha)
            if m:
                atual = (m.group(1).lower(), [])
        elif FECHA.match(linha):
            achados.append((atual[0], "\n".join(atual[1]), True))
            atual = None
        else:
            atual[1].append(linha)
    if atual is not None:
        achados.append((atual[0], "\n".join(atual[1]), False))
    return achados


def _e_python(texto):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            ast.parse(texto)
        except (SyntaxError, ValueError):
            return False
    return True


def extrair(texto):
    """(codigo ou None, situacao, linguagem, numero de blocos)."""
    todos = blocos(texto)
    if not todos:
        if texto.strip() and _e_python(texto):
            return texto.strip("\n"), "sem cerca", "", 0
        return None, "sem codigo", "", 0
    candidatos = [b for b in todos if b[0] in LINGUAGENS]
    if not candidatos:
        return None, "sem codigo", "", len(todos)
    linguagem, codigo, fechado = candidatos[-1]
    return codigo, "bloco" if fechado else "cerca aberta", linguagem, len(todos)


def main(argv=None):
    p = argparse.ArgumentParser(description="Extrai o codigo das respostas brutas.")
    p.add_argument("pasta", nargs="?", default=str(FASE1),
                   help="pasta da fase (padrao: resultados/geracoes/fase1)")
    args = p.parse_args(argv)

    pasta = Path(args.pasta).resolve()
    registros = sorted(f for f in pasta.glob("*/*.json")
                       if not f.parent.name.startswith("_"))
    if not registros:
        sys.exit(f"nenhuma geracao em {pasta}")
    saida = pasta / "_extraidos"

    linhas, contagem = [], Counter()
    for f in registros:
        d = json.loads(f.read_text(encoding="utf-8"))
        codigo, situacao, linguagem, n = extrair(d["resposta_texto"])
        arquivo = ""
        if codigo is not None:
            destino = saida / d["modelo"] / f"{f.stem}.py"
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(codigo + "\n", encoding="utf-8", newline="\n")
            arquivo = destino.relative_to(pasta).as_posix()
        linhas.append({"identificador": f.stem, "modelo": d["modelo"],
                       "instancia": d["instancia"], "smell": d["smell"],
                       "tecnica": d["tecnica"], "execucao": d["execucao"],
                       "seed": d["seed"], "done_reason": d["done_reason"],
                       "situacao": situacao, "linguagem": linguagem, "blocos": n,
                       "linhas": len(codigo.splitlines()) if codigo else 0,
                       "arquivo": arquivo})
        contagem[d["modelo"], situacao] += 1

    saida.mkdir(exist_ok=True)
    with open(saida / "extracao.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUNAS)
        w.writeheader()
        w.writerows(linhas)

    print(f"{len(registros)} geracoes em {pasta}")
    for modelo in sorted({m for m, _ in contagem}):
        partes = ", ".join(f"{s} {c}" for (m, s), c in sorted(contagem.items()) if m == modelo)
        print(f"  {modelo:9} {partes}")
    print(f"saida em {saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
