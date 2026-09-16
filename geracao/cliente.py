"""
Cliente unico para os tres modelos e funcao de registro das geracoes.

Os tres provedores (Gemini via endpoint OpenAI-compativel, GPT via OpenAI
direto e Qwen via Groq) expoem APIs compativeis com a do OpenAI, entao
o mesmo cliente atende os tres, mudando apenas base_url, chave e model id.

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

from dotenv import load_dotenv
from openai import OpenAI

# Carrega o .env no processo assim que este modulo e importado. Isso torna
# a leitura das chaves independente de qualquer configuracao de terminal/IDE
# (ex.: "python.terminal.useEnvFile" do VS Code), o que importa para
# reproducibilidade: qualquer pessoa que clonar o repo e rodar o codigo
# tem o mesmo comportamento, sem depender de ajustes locais de editor.
load_dotenv()


def _cliente(provedor):
    """Instancia um cliente OpenAI-compativel para o provedor informado."""
    api_key = os.environ.get(provedor["api_key_env"])
    if not api_key:
        raise RuntimeError(
            f"Variavel de ambiente {provedor['api_key_env']} nao definida. "
            f"Copie .env.example para .env e preencha as chaves."
        )
    return OpenAI(api_key=api_key, base_url=provedor["base_url"])


def chamar_modelo(provedor, mensagens, parametros):
    """Faz uma chamada de chat e devolve (texto, resposta_bruta, latencia_s)."""
    client = _cliente(provedor)
    inicio = time.time()
    resposta = client.chat.completions.create(
        model=provedor["modelo"],
        messages=mensagens,
        **parametros,
    )
    latencia = time.time() - inicio
    texto = resposta.choices[0].message.content
    return texto, resposta, latencia


def registrar(dir_saida, identificador, provedor, mensagens, parametros,
              resposta_bruta, texto, latencia):
    """Grava um JSON com todos os metadados da chamada, de forma completa.

    Guarda: modelo pedido e modelo efetivamente servido, endpoint, parametros,
    prompt completo, timestamp UTC, latencia, texto e a resposta bruta inteira.
    """
    Path(dir_saida).mkdir(parents=True, exist_ok=True)
    bruta = (
        resposta_bruta.model_dump()
        if hasattr(resposta_bruta, "model_dump")
        else str(resposta_bruta)
    )
    registro = {
        "identificador": identificador,
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "provedor": provedor["nome"],
        "modelo_pedido": provedor["modelo"],
        "modelo_servido": bruta.get("model") if isinstance(bruta, dict) else None,
        "base_url": provedor["base_url"],
        "parametros": parametros,
        "prompt": mensagens,
        "latencia_s": round(latencia, 3),
        "resposta_texto": texto,
        "resposta_bruta": bruta,
    }
    destino = Path(dir_saida) / f"{identificador}.json"
    destino.write_text(
        json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return destino