import os
from types import SimpleNamespace
from typing import List, Tuple


class Completion:
    """Mesma interface de openai.Completion (biblioteca openai anterior a 1.0).

    create registra a chave e os parametros de cada pedido e devolve as
    escolhas preparadas em `escolhas`.
    """

    pedidos: List[Tuple[str, dict]] = []
    escolhas: List[str] = []

    @classmethod
    def create(cls, **kwargs):
        cls.pedidos.append((os.getenv("OPENAI_API_KEY"), kwargs))
        return {"choices": [cls._escolha(texto) for texto in cls.escolhas]}

    @staticmethod
    def _escolha(texto):
        return {"text": texto}


openai = SimpleNamespace(api_key=None, Completion=Completion)


def summarize(text: str) -> str:
    """Summarize a text string and return a summary of the text"""
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"].strip(" \n")


def executar(texto: str, escolhas: List[str]) -> Tuple[str, List[Tuple[str, dict]]]:
    """Resume texto; devolve o resumo e os pedidos feitos. Ponto de entrada publico desta unidade."""
    Completion.pedidos = []
    Completion.escolhas = list(escolhas)
    resumo = summarize(texto)
    return resumo, Completion.pedidos
