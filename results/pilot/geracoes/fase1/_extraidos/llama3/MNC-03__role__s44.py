import os
from types import SimpleNamespace

class Completion:
    """Mesma interface de openai.Completion (biblioteca openai anterior a 1.0).

    create registra a chave e os parametros de cada pedido e devolve as
    escolhas preparadas em `escolhas`.
    """

    def __init__(self, escolhas):
        self.pedidos = []
        self.escolhas = escolhas

    @classmethod
    def create(cls, **kwargs):
        return cls(kwargs.get("escolhas", []))

    @staticmethod
    def _escolha(texto):
        return {"text": texto}

openai = SimpleNamespace(api_key=None, Completion=Completion)


def summarize(text, escolhas):
    """Summarize a text string and return a summary of the text"""
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.Completion(**{"escolhas": escolhas})
    response = completion.create(
        model="text-davinci-002",
        prompt=text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"].strip(" \n")


def executar(texto, escolhas):
    """Resume texto; devolve o resumo e os pedidos feitos. Ponto de entrada publico desta unidade."""
    completion = openai.Completion(escolhas)
    resumo = summarize(texto, escolhas)
    return resumo, completion.pedidos
