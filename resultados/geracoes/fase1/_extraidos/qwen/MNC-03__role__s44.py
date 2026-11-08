import os
from types import SimpleNamespace


class Completion:
    """Mesma interface de openai.Completion (biblioteca openai anterior a 1.0).

    create registra a chave e os parametros de cada pedido e devolve as
    escolhas preparadas em `escolhas`.
    """

    pedidos = []
    escolhas = []

    @classmethod
    def create(cls, **kwargs):
        cls.pedidos.append((openai.api_key, kwargs))
        return {"choices": [cls._escolha(texto) for texto in cls.escolhas]}

    @staticmethod
    def _escolha(texto):
        return {"text": texto}


openai = SimpleNamespace(api_key=None, Completion=Completion)


def set_openai_api_key():
    openai.api_key = os.getenv("OPENAI_API_KEY")


def create_completion_request(**kwargs):
    return openai.Completion.create(
        model="text-davinci-002",
        prompt=kwargs["prompt"],
        temperature=kwargs["temperature"],
        max_tokens=kwargs["max_tokens"],
        top_p=kwargs["top_p"],
        frequency_penalty=kwargs["frequency_penalty"],
        presence_penalty=kwargs["presence_penalty"],
    )


def summarize(text):
    """Summarize a text string and return a summary of the text"""
    set_openai_api_key()
    response = create_completion_request(prompt=text, temperature=0.7, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)
    return response["choices"][0]["text"].strip(" \n")


def executar(texto, escolhas):
    """Resume texto; devolve o resumo e os pedidos feitos. Ponto de entrada publico desta unidade."""
    Completion.pedidos = []
    Completion.escolhas = list(escolhas)
    resumo = summarize(texto)
    return resumo, Completion.pedidos
