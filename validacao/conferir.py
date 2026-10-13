"""Validacao de uma refatoracao gerada por LLM (etapa 5).

Para uma instancia e um arquivo refatorado, confere:
  preservacao   os 3 testes da instancia passam sobre o arquivo;
  remocao       o Pysmell nao detecta mais o smell da instancia no arquivo.

As duas respostas sao independentes: a analise mede a remocao so nas
refatoracoes que preservam o comportamento.

Uso:
    python -m validacao.conferir LLF-01 caminho.py
"""

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

from adaptacao.checklist import _caminhos, _pytest, _selecao
from dados.pysmell.detectar import detectar_arquivo


def conferir(inst, caminho):
    """{testes, preservou, restantes, outros, removeu} de um arquivo refatorado."""
    _, unidade, teste, _ = _caminhos(inst)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        shutil.copy(caminho, Path(tmp, unidade.name))
        shutil.copy(teste, tmp)
        r = _pytest(Path(tmp))
    ultima = (r.stdout.strip().splitlines() or ["(sem saida)"])[-1]
    deteccoes = detectar_arquivo(str(caminho))
    restantes = [f"{d['smell']} L{d['linha']} {d['metricas']}"
                 for d in deteccoes if d["smell"] == inst["smell"]]
    outros = [f"{d['smell']} L{d['linha']} {d['metricas']}"
              for d in deteccoes if d["smell"] != inst["smell"]]
    return {
        "testes": ultima,
        "preservou": r.returncode == 0 and "3 passed" in ultima,
        "restantes": restantes,
        "outros": outros,
        "removeu": not restantes,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Valida uma refatoracao de uma instancia.")
    p.add_argument("id", help="id da instancia (ex.: LLF-01)")
    p.add_argument("arquivo", help="arquivo refatorado")
    args = p.parse_args(argv)

    selecao = _selecao()
    if args.id not in selecao:
        p.error(f"id fora da selecao: {args.id}")
    inst = selecao[args.id]
    res = conferir(inst, args.arquivo)
    print(f"{inst['id']}: {args.arquivo}")
    print(f"  pytest: {res['testes']}")
    print(f"  {inst['smell']} restante: {', '.join(res['restantes']) or 'nenhum'}")
    if res["outros"]:
        print(f"  outros smells: {', '.join(res['outros'])}")
    print(f"  preservou: {'sim' if res['preservou'] else 'nao'}"
          f" | removeu: {'sim' if res['removeu'] else 'nao'}")
    return 0 if res["preservou"] else 1


if __name__ == "__main__":
    sys.exit(main())
