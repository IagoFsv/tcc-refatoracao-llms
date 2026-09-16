"""
Smoke test: faz UMA chamada a cada modelo do config e registra o resultado.

Objetivo: confirmar que chaves, endpoints, model ids e o registro funcionam
antes de construir qualquer loop de geracao. E o primeiro passo de codigo.

Uso:
    python -m geracao.smoke_test            # chama os tres modelos de verdade
    python -m geracao.smoke_test --dry-run  # nao acessa a rede, so valida o wiring
"""

import argparse
import os
import sys
from pathlib import Path

# Console do Windows por padrao usa um codepage (ex.: cp1252) que nao cobre
# todo Unicode; se a resposta de um modelo vier com emoji ou outro caractere
# fora dessa tabela, o print() quebra com UnicodeEncodeError mesmo com a
# chamada de API e o registro em disco (sempre UTF-8) tendo funcionado.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import yaml

from geracao import cliente

RAIZ = Path(__file__).resolve().parents[1]

PROMPT_TESTE = [
    {"role": "system", "content": "Voce e um assistente conciso."},
    {"role": "user", "content": "Responda apenas com a palavra: OK"},
]


def carregar_config():
    with open(RAIZ / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Smoke test dos tres modelos.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Nao chama a rede; so valida config e presenca das chaves.")
    args = parser.parse_args()

    cfg = carregar_config()
    provedores = cfg["provedores"]
    parametros = cfg["parametros"]
    dir_log = RAIZ / "resultados" / "geracoes" / "_smoke_test"

    print(f"Testando {len(provedores)} provedor(es). dry-run={args.dry_run}\n")
    houve_falha = False

    for p in provedores:
        rotulo = f"{p['nome']} ({p['modelo']})"

        if args.dry_run:
            tem_chave = bool(os.environ.get(p["api_key_env"]))
            status = "definida" if tem_chave else "NAO definida"
            print(f"[dry-run] {rotulo}")
            print(f"          base_url: {p['base_url']}")
            print(f"          chave {p['api_key_env']}: {status}\n")
            continue

        try:
            texto, bruta, lat = cliente.chamar_modelo(p, PROMPT_TESTE, parametros)
            caminho = cliente.registrar(
                dir_log, p["nome"], p, PROMPT_TESTE, parametros, bruta, texto, lat
            )
            print(f"[ok] {rotulo}  ({lat:.1f}s)")
            print(f"     resposta: {texto!r}")
            print(f"     registro: {caminho.relative_to(RAIZ)}\n")
        except Exception as e:  # noqa: BLE001 - queremos ver qualquer falha aqui
            houve_falha = True
            print(f"[FALHA] {rotulo}")
            print(f"        {type(e).__name__}: {e}\n")

    if houve_falha:
        print("Um ou mais provedores falharam. Confira o .env e o config.yaml.")
        sys.exit(1)

    if not args.dry_run:
        print("Todos os provedores responderam. Wiring das APIs confirmado.")


if __name__ == "__main__":
    main()
