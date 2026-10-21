"""
Smoke test: faz UMA chamada curta a cada modelo do config e registra o resultado.

Objetivo: confirmar que o Ollama responde, que tags e digests batem com o
config e que o registro funciona, antes de construir o loop de geracao.

Uso:
    python -m geracao.smoke_test            # chama os modelos de verdade
    python -m geracao.smoke_test --dry-run  # nao gera texto: so confere
                                            # config, Ollama no ar e digests

Cada rodada grava em resultados/geracoes/_smoke_test/<timestamp>/ (fora do
controle de versao), com o ambiente em _ambiente.json.
"""

import argparse
import datetime
import sys
from pathlib import Path

# Console do Windows por padrao usa um codepage (ex.: cp1252) que nao cobre
# todo Unicode; se a resposta de um modelo vier com emoji ou outro caractere
# fora dessa tabela, o print() quebra com UnicodeEncodeError mesmo com a
# chamada e o registro em disco (sempre UTF-8) tendo funcionado.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import yaml

from geracao import cliente

RAIZ = Path(__file__).resolve().parents[1]

# Sem mensagem de system, como no estudo: vale o SYSTEM padrao do Modelfile.
PROMPT_TESTE = [
    {"role": "user", "content": "Responda apenas com a palavra: OK"},
]


def carregar_config():
    with open(RAIZ / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Smoke test dos modelos locais.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Nao gera texto; so confere config, Ollama e digests.")
    args = parser.parse_args()

    cfg = carregar_config()
    modelos = cfg["modelos"]
    seed = cfg["seeds"][0]
    rodada = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    dir_log = RAIZ / "resultados" / "geracoes" / "_smoke_test" / rodada

    print(f"Testando {len(modelos)} modelo(s). dry-run={args.dry_run}")
    print(f"options: {cfg['parametros']} seed={seed}\n")
    houve_falha = False
    ambientes = []

    for m in modelos:
        rotulo = f"{m['nome']} ({m['tag']})"
        try:
            amb = cliente.ambiente(cfg, m)
        except Exception as e:  # noqa: BLE001 - queremos ver qualquer falha aqui
            houve_falha = True
            print(f"[FALHA] {rotulo}\n        {type(e).__name__}: {e}\n")
            continue
        ambientes.append(amb)

        if args.dry_run:
            print(f"[dry-run] {rotulo}")
            print(f"          Ollama {amb['ollama_versao']}, digest confere "
                  f"({amb['digest'][:12]}), "
                  f"{amb['detalhes']['quantization_level']}\n")
            continue

        try:
            texto, corpo, bruta, lat = cliente.chamar_modelo(
                cfg, m, PROMPT_TESTE, seed
            )
            gpu = cliente.uso_gpu(cfg, m)
            caminho = cliente.registrar(
                dir_log, m["nome"], cfg, m, amb, corpo, bruta, texto, lat, gpu
            )
            print(f"[ok] {rotulo}  ({lat:.1f}s)")
            print(f"     resposta: {texto!r}")
            print(f"     done_reason={bruta.get('done_reason')} "
                  f"prompt={bruta.get('prompt_eval_count')} "
                  f"saida={bruta.get('eval_count')} tokens")
            if gpu:
                print(f"     GPU: {gpu['fracao_gpu']:.0%} "
                      f"(context_length={gpu['context_length']})")
            print(f"     registro: {caminho.relative_to(RAIZ)}\n")
        except Exception as e:  # noqa: BLE001
            houve_falha = True
            print(f"[FALHA] {rotulo}\n        {type(e).__name__}: {e}\n")

    if ambientes and not args.dry_run:
        cliente.registrar_ambiente(dir_log, ambientes)

    if houve_falha:
        print("Um ou mais modelos falharam. Confira o Ollama e o config.yaml.")
        sys.exit(1)

    if not args.dry_run:
        print("Todos os modelos responderam. Wiring do Ollama confirmado.")


if __name__ == "__main__":
    main()
