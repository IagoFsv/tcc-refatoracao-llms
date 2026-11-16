import os
from types import SimpleNamespace


class OpenAIConfig:
    """Configuration for OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    model = "text-davinci-002"
    temperature = 0.7
    max_tokens = 256
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0


class Completion:
    """Same interface as openai.Completion (previous version of the openai library).

    create registers the key and parameters of each request and returns the prepared choices in 'escolhas'.
    """

    pedidos = []
    escolhas = []

    @classmethod
    def create(cls, **kwargs):
        cls.pedidos.append((OpenAIConfig.api_key, kwargs))
        return {"choices": [cls._escolha(texto) for texto in cls.escolhas]}

    @staticmethod
    def _escolha(texto):
        return {"text": texto}


openai = SimpleNamespace(api_key=None, Completion=Completion)


def summarize(text):
    """Summarize a text string and return a summary of the text."""
    response = openai.Completion.create(
        model=OpenAIConfig.model,
        prompt=text,
        temperature=OpenAIConfig.temperature,
        max_tokens=OpenAIConfig.max_tokens,
        top_p=OpenAIConfig.top_p,
        frequency_penalty=OpenAIConfig.frequency_penalty,
        presence_penalty=OpenAIConfig.presence_penalty,
    )
    return response["choices"][0]["text"].strip(" \n")


def executar(texto, escolhas):
    """Resume texto; devolve o resumo e os pedidos feitos. Ponto de entrada público desta unidade."""
    Completion.pedidos = []
    Completion.escolhas = list(escolhas)
    resumo = summarize(texto)
    return resumo, Completion.pedidos
