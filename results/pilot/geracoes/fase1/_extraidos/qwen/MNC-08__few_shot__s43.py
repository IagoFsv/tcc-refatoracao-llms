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
    def _escolha(texto: str) -> dict:
        return {"text": texto}


openai = SimpleNamespace(api_key=None, Completion=Completion)


def submit_question(text: str) -> str:
    """This submits a question to the OpenAI API"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = text

    result = openai.Completion.create(
        prompt=prompt,
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-003",
    )["choices"][0]["text"].strip(" \n")
    return result


def executar(texto: str, escolhas: List[str]) -> Tuple[str, List[Tuple[str, dict]]]:
    """Envia a pergunta; devolve a resposta e os pedidos feitos. Ponto de entrada publico desta unidade."""
    Completion.pedidos = []
    Completion.escolhas = escolhas
    resposta = submit_question(texto)
    return resposta, Completion.pedidos
