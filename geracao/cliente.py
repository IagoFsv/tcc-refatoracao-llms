"""
Cliente dos modelos locais (Ollama) e funcao de registro das geracoes.

Usa o endpoint nativo POST /api/chat, e nao o /v1 OpenAI-compativel, porque
so o nativo aceita num_ctx e os demais "options" do llama.cpp. Nenhuma
mensagem de system e enviada: cada modelo recebe o SYSTEM padrao do seu
Modelfile, registrado por ambiente().

A funcao registrar() grava a saida bruta de forma completa e imutavel. Esse
registro e o que sustenta a reprodutibilidade e a rastreabilidade exigidas
pelo estudo: cada numero na analise deve poder ser rastreado ate a chamada
exata que o gerou.
"""

import datetime
import json
import os
import time
from pathlib import Path

import requests

# Geracao longa em GPU modesta (e o DeepSeek parte na CPU) pode levar
# minutos; o limite so existe para a rodada nao travar para sempre.
TIMEOUT_S = 1800


def _url(cfg, caminho):
    return cfg["ollama"]["base_url"].rstrip("/") + caminho


def _get(cfg, caminho):
    r = requests.get(_url(cfg, caminho), timeout=30)
    r.raise_for_status()
    return r.json()


def _post(cfg, caminho, corpo, timeout=30):
    r = requests.post(_url(cfg, caminho), json=corpo, timeout=timeout)
    if not r.ok:
        # O Ollama explica o erro no corpo (ex.: prompt maior que o num_ctx).
        raise RuntimeError(f"HTTP {r.status_code} em {caminho}: {r.text}")
    return r.json()


def ambiente(cfg, modelo):
    """Descreve o modelo instalado e confere o digest contra o config.

    Chamar uma vez por rodada, antes de gerar. Devolve versao do Ollama,
    digest, detalhes, Modelfile, template, SYSTEM e parametros do Modelfile.
    Levanta RuntimeError se a tag nao estiver instalada ou se o digest
    instalado for diferente do config.yaml.
    """
    versao = _get(cfg, "/api/version")["version"]
    instalados = {m["name"]: m for m in _get(cfg, "/api/tags")["models"]}
    if modelo["tag"] not in instalados:
        raise RuntimeError(
            f"{modelo['tag']} nao esta instalado no Ollama "
            f"(ollama pull {modelo['tag']})."
        )
    digest = instalados[modelo["tag"]]["digest"]
    if digest != modelo["digest"]:
        raise RuntimeError(
            f"Digest de {modelo['tag']} diferente do config.yaml: "
            f"instalado {digest}, esperado {modelo['digest']}."
        )
    show = _post(cfg, "/api/show", {"model": modelo["tag"]})
    return {
        "ollama_versao": versao,
        "tag": modelo["tag"],
        "digest": digest,
        "detalhes": show.get("details"),
        "modelfile": show.get("modelfile"),
        "template": show.get("template"),
        "system": show.get("system"),
        "parametros_modelfile": show.get("parameters"),
    }


def montar_corpo(cfg, modelo, mensagens, seed):
    """Corpo do POST /api/chat: options do config mais a seed da execucao."""
    return {
        "model": modelo["tag"],
        "messages": mensagens,
        "stream": False,
        "options": {**cfg["parametros"], "seed": seed},
        **cfg["requisicao"],
    }


def uso_gpu(cfg, modelo):
    """Fracao do modelo carregada na GPU, lida do GET /api/ps.

    Chamar logo depois de uma geracao, com o modelo ainda carregado. So
    afeta a velocidade, nao o resultado; fica registrado para documentar
    quando parte do modelo roda na CPU.
    """
    for m in _get(cfg, "/api/ps")["models"]:
        if m["name"] == modelo["tag"]:
            return {
                "size": m.get("size"),
                "size_vram": m.get("size_vram"),
                "fracao_gpu": round(m["size_vram"] / m["size"], 3)
                if m.get("size") else None,
                "context_length": m.get("context_length"),
            }
    return None


def chamar_modelo(cfg, modelo, mensagens, seed):
    """Faz uma chamada de chat e devolve (texto, corpo, resposta_bruta, latencia_s)."""
    corpo = montar_corpo(cfg, modelo, mensagens, seed)
    inicio = time.time()
    resposta = _post(cfg, "/api/chat", corpo, timeout=TIMEOUT_S)
    latencia = time.time() - inicio
    return resposta["message"]["content"], corpo, resposta, latencia


def registrar(dir_saida, identificador, cfg, modelo, amb, corpo,
              resposta_bruta, texto, latencia, gpu=None, extra=None):
    """Grava um JSON com todos os metadados da chamada, de forma completa.

    Guarda: tag e digest, versao do Ollama, endpoint, corpo enviado (prompt
    completo, options com seed, truncate/shift), timestamp UTC, latencia,
    done_reason, contagem de tokens, uso da GPU, texto e a resposta bruta
    inteira, mais os campos de `extra` (instancia, tecnica, seed, commit...).
    Nunca sobrescreve: se o arquivo ja existe, levanta FileExistsError.
    Escreve primeiro num .tmp e so entao renomeia, para uma interrupcao no
    meio da escrita nao deixar um JSON pela metade com o nome final.
    """
    Path(dir_saida).mkdir(parents=True, exist_ok=True)
    registro = {
        "identificador": identificador,
        **(extra or {}),
        "timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "modelo": modelo["nome"],
        "tag": modelo["tag"],
        "digest": amb["digest"],
        "ollama_versao": amb["ollama_versao"],
        "endpoint": _url(cfg, "/api/chat"),
        "requisicao": corpo,
        "latencia_s": round(latencia, 3),
        "done_reason": resposta_bruta.get("done_reason"),
        "prompt_eval_count": resposta_bruta.get("prompt_eval_count"),
        "eval_count": resposta_bruta.get("eval_count"),
        "uso_gpu": gpu,
        "resposta_texto": texto,
        "resposta_bruta": resposta_bruta,
    }
    destino = Path(dir_saida) / f"{identificador}.json"
    if destino.exists():
        raise FileExistsError(destino)
    tmp = destino.with_name(destino.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(registro, f, ensure_ascii=False, indent=2)
    os.replace(tmp, destino)
    return destino


def registrar_ambiente(dir_saida, ambientes):
    """Grava o ambiente da rodada (um item por modelo), sem sobrescrever."""
    Path(dir_saida).mkdir(parents=True, exist_ok=True)
    destino = Path(dir_saida) / "_ambiente.json"
    with open(destino, "x", encoding="utf-8") as f:
        json.dump(ambientes, f, ensure_ascii=False, indent=2)
    return destino
