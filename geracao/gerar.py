"""
Loop de geracao (etapa 4): cada instancia -> 3 modelos -> 3 tecnicas -> 3
execucoes, uma chamada independente (contexto novo) por combinacao.

Ordem em camadas, uma por seed (execucao 1, 2 e 3). Cada camada cobre todas
as instancias, modelos e tecnicas, entao uma parada no meio da rodada deixa
camadas completas e equilibradas, e nunca um modelo inteiro sem saida.
Dentro da camada, um modelo de cada vez (com 8 GB de VRAM so cabe um
carregado, e alternar faria o Ollama recarregar a cada chamada); dentro
dele, instancia e tecnica. Cada chamada vira um JSON imutavel em
resultados/geracoes/fase1/<modelo>/<ID>__<tecnica>__s<seed>.json.

Retomavel: o que ja tem registro e pulado, entao basta rodar de novo depois
de uma interrupcao. Nada e gerado de novo porque a saida ficou ruim: saida
ruim e dado. Chamada que falha por infraestrutura (HTTP, timeout, Ollama
fora do ar) nao gera registro, vai para o erros.jsonl da sessao e e refeita
na proxima vez. done_reason "length" (saida cortada) e registrada como
qualquer outra e so contada a parte.

Travas, para todas as geracoes verem o mesmo instrumento:
  - arvore do git limpa fora de resultados/, e o commit vai em cada registro;
  - versao do Ollama igual a do config.yaml e digest do modelo igual ao do
    config, conferidos antes de cada chamada;
  - uma rodada por vez (arquivo _rodando.lock na pasta da fase).

O codigo refatorado NAO e extraido aqui: a resposta bruta fica intocada e a
extracao e uma etapa separada.

Uso:
    python -m geracao.gerar --dry-run       # confere tudo e conta o que falta
    python -m geracao.gerar --piloto        # LM-01, LPL-01, LLF-01, MNC-01, seed 42,
                                            # em _piloto/ (descartavel, fora do git)
    python -m geracao.gerar                 # fase 1 inteira, retoma de onde parou
    python -m geracao.gerar --modelo qwen   # so um modelo
"""

import argparse
import datetime
import json
import os
import statistics
import subprocess
import sys
from pathlib import Path

# Mesmo motivo do smoke_test: o console do Windows quebra com caractere fora
# do codepage.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import yaml
from tqdm import tqdm

from geracao import cliente, prompts

RAIZ = Path(__file__).resolve().parents[1]
INSTANCIAS = RAIZ / "instancias"
GERACOES = RAIZ / "resultados" / "geracoes"
FASE = "fase1"

# Piloto: so mede tempo e testa o pipeline. As instancias do piloto da etapa 2.
PILOTO_IDS = ("LM-01", "LPL-01", "LLF-01", "MNC-01")

# Falhas de infraestrutura seguidas antes de desistir (Ollama fora do ar).
MAX_FALHAS_SEGUIDAS = 3


def _unidades(ids=None):
    """{id: caminho da unidade} das instancias com pasta (ou so das pedidas)."""
    todas = {p.parent.name: p for p in sorted(INSTANCIAS.glob("*/*/*.py"))
             if p.stem == p.parent.name.replace("-", "_")}
    if not ids:
        return todas
    desconhecidos = [i for i in ids if i not in todas]
    if desconhecidos:
        sys.exit(f"sem unidade em instancias/: {', '.join(desconhecidos)}")
    return {i: todas[i] for i in ids}


def _git(*args):
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True,
                          text=True, check=True).stdout.strip()


def _commit(exigir_limpa):
    """Hash do HEAD. Aborta se houver mudanca fora de resultados/ (e exigir)."""
    sujos = _git("status", "--porcelain", "--", ".", ":(exclude)resultados")
    if sujos and exigir_limpa:
        sys.exit("Ha mudancas fora de resultados/ sem commit. Commite antes de "
                 "gerar, para cada registro apontar a versao exata do que "
                 "entrou no prompt:\n" + sujos)
    return _git("rev-parse", "HEAD") + ("-sujo" if sujos else "")


def _conferir_instrumento(cfg, modelo):
    """Aborta se a versao do Ollama ou o digest do modelo mudaram.

    Chamado antes de cada geracao: o app do Ollama pode se atualizar e um
    `ollama pull` pode trocar o modelo no meio da rodada. Erro de conexao
    sobe como requests.RequestException (falha de infraestrutura).
    """
    versao = cliente._get(cfg, "/api/version")["version"]
    if versao != cfg["ollama"]["versao"]:
        sys.exit(f"Ollama {versao} instalado, config.yaml espera "
                 f"{cfg['ollama']['versao']}. Rodada interrompida.")
    instalados = {m["name"]: m["digest"] for m in cliente._get(cfg, "/api/tags")["models"]}
    if instalados.get(modelo["tag"]) != modelo["digest"]:
        sys.exit(f"Digest de {modelo['tag']} mudou (instalado "
                 f"{instalados.get(modelo['tag'])}). Rodada interrompida.")


def _tarefas(modelos, unidades, seeds, dir_fase):
    """Todas as combinacoes, na ordem de execucao, com o destino do registro."""
    for execucao, seed in enumerate(seeds, start=1):
        for m in modelos:
            for ident, unidade in unidades.items():
                for tecnica in prompts.TECNICAS:
                    destino = dir_fase / m["nome"] / f"{ident}__{tecnica}__s{seed}.json"
                    yield m, ident, unidade, tecnica, execucao, seed, destino


def _registrar_falha(dir_sessao, tarefa, erro):
    m, ident, _, tecnica, _, seed, _ = tarefa
    linha = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "modelo": m["nome"], "instancia": ident, "tecnica": tecnica,
             "seed": seed, "erro": f"{type(erro).__name__}: {erro}"}
    with open(dir_sessao / "erros.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(linha, ensure_ascii=False) + "\n")


def main(argv=None):
    p = argparse.ArgumentParser(description="Loop de geracao da fase 1.")
    p.add_argument("--piloto", action="store_true",
                   help=f"so {', '.join(PILOTO_IDS)} com a primeira seed, em _piloto/")
    p.add_argument("--modelo", action="append",
                   help="so este modelo (nome do config.yaml); pode repetir")
    p.add_argument("--dry-run", action="store_true",
                   help="confere ambiente e conta o que falta, sem gerar")
    args = p.parse_args(argv)

    with open(RAIZ / "config.yaml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    modelos = cfg["modelos"]
    if args.modelo:
        desconhecidos = set(args.modelo) - {m["nome"] for m in modelos}
        if desconhecidos:
            sys.exit(f"modelo fora do config.yaml: {', '.join(sorted(desconhecidos))}")
        modelos = [m for m in modelos if m["nome"] in args.modelo]

    sessao = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    if args.piloto:
        unidades = _unidades(PILOTO_IDS)
        seeds = cfg["seeds"][:1]
        dir_fase = GERACOES / "_piloto" / sessao
    else:
        unidades = _unidades()
        seeds = cfg["seeds"]
        dir_fase = GERACOES / FASE
    commit = _commit(exigir_limpa=not (args.piloto or args.dry_run))

    # Ambiente completo de todos os modelos no inicio: se algum digest nao
    # bate, para antes de gerar qualquer coisa.
    ambientes = {}
    try:
        for m in modelos:
            _conferir_instrumento(cfg, m)
            ambientes[m["nome"]] = cliente.ambiente(cfg, m)
    except requests.RequestException:
        sys.exit(f"Ollama fora do ar em {cfg['ollama']['base_url']}. Abra o Ollama e rode de novo.")

    tarefas = list(_tarefas(modelos, unidades, seeds, dir_fase))
    pendentes = [t for t in tarefas if not t[-1].exists()]
    print(f"{len(unidades)} instancias x {len(modelos)} modelos x "
          f"{len(prompts.TECNICAS)} tecnicas x {len(seeds)} seeds = {len(tarefas)} chamadas")
    for execucao, seed in enumerate(seeds, start=1):
        por_modelo = ", ".join(f"{m['nome']} {sum(t[0] is m and t[5] == seed for t in pendentes)}"
                               for m in modelos)
        print(f"  camada {execucao} (seed {seed}) pendentes: {por_modelo}")
    print(f"commit {commit}, Ollama {cfg['ollama']['versao']}, destino "
          f"{dir_fase.relative_to(RAIZ)}")
    if commit.endswith("-sujo") and not args.piloto:
        print("ATENCAO: ha mudancas sem commit; a rodada de verdade vai recusar.")
    if args.dry_run or not pendentes:
        return 0

    dir_fase.mkdir(parents=True, exist_ok=True)
    trava = dir_fase / "_rodando.lock"
    try:
        with open(trava, "x", encoding="utf-8") as fh:
            fh.write(f"pid {os.getpid()}, sessao {sessao}\n")
    except FileExistsError:
        sys.exit(f"Ja existe {trava.relative_to(RAIZ)}: outra rodada em andamento? "
                 "Se nenhuma estiver rodando (a anterior foi morta), apague o "
                 "arquivo e rode de novo.")

    dir_sessao = dir_fase / "_sessoes" / sessao
    feitas, cortadas, falhas, seguidas = 0, [], 0, 0
    latencias = {m["nome"]: [] for m in modelos}
    try:
        dir_sessao.mkdir(parents=True)
        with open(dir_sessao / "_ambiente.json", "x", encoding="utf-8") as fh:
            json.dump({"sessao": sessao, "commit": commit, "piloto": args.piloto,
                       "python": sys.version, "argv": sys.argv[1:],
                       "modelos": list(ambientes.values())}, fh, ensure_ascii=False, indent=2)

        for tarefa in tqdm(pendentes, unit="chamada", dynamic_ncols=True):
            m, ident, unidade, tecnica, execucao, seed, destino = tarefa
            smell = unidade.parent.parent.name
            mensagens = prompts.montar(tecnica, smell, unidade.read_text(encoding="utf-8"))
            try:
                _conferir_instrumento(cfg, m)
                texto, corpo, bruta, lat = cliente.chamar_modelo(cfg, m, mensagens, seed)
                gpu = cliente.uso_gpu(cfg, m)
            except (requests.RequestException, RuntimeError) as e:
                falhas += 1
                seguidas += 1
                _registrar_falha(dir_sessao, tarefa, e)
                tqdm.write(f"[falha] {m['nome']} {destino.stem}: {type(e).__name__}: {e}")
                if seguidas >= MAX_FALHAS_SEGUIDAS:
                    sys.exit(f"{seguidas} falhas seguidas: o Ollama esta no ar? "
                             "Rode de novo para retomar.")
                continue
            seguidas = 0
            cliente.registrar(destino.parent, destino.stem, cfg, m, ambientes[m["nome"]],
                              corpo, bruta, texto, lat, gpu,
                              extra={"instancia": ident, "smell": smell, "tecnica": tecnica,
                                     "execucao": execucao, "seed": seed,
                                     "commit": commit, "sessao": sessao})
            feitas += 1
            latencias[m["nome"]].append(lat)
            if bruta.get("done_reason") != "stop":
                cortadas.append(destino.stem)
                tqdm.write(f"[aviso] {m['nome']} {destino.stem}: "
                           f"done_reason={bruta.get('done_reason')}")
    finally:
        trava.unlink(missing_ok=True)

    print(f"\nfeitas {feitas}, falhas {falhas} (em {dir_sessao.relative_to(RAIZ)}/erros.jsonl), "
          f"done_reason != stop: {len(cortadas)}")
    # Estimativa para a fase 1 inteira, util sobretudo no piloto.
    por_modelo = len(_unidades()) * len(prompts.TECNICAS) * len(cfg["seeds"])
    for nome, lats in latencias.items():
        if lats:
            media = statistics.mean(lats)
            print(f"  {nome:9} media {media:.1f} s/chamada; fase 1 ({por_modelo} "
                  f"chamadas) ~ {media * por_modelo / 3600:.1f} h")
    restantes = sum(not t[-1].exists() for t in tarefas)
    if restantes:
        print(f"faltam {restantes}: rode de novo para retomar.")
    return 1 if restantes else 0


if __name__ == "__main__":
    sys.exit(main())
