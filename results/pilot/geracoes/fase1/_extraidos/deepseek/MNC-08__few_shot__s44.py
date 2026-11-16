import os
from types import SimpleNamespace


class Completion:
    pedidos = []
    escolhas = []

    @classmethod
    def create(cls, texto):
        cls.pedidos.append((openai.api_key, texto))
        return cls._escolha(texto)

    @staticmethod
    def _escolha(texto):
        return {"choices": [{"text": texto}]}


openai = SimpleNamespace(api_key=None, Completion=Completion)


def submit_question(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = text

    result = openai.Completion.create(prompt)
    return result["choices"][0]["text"].strip(" \n")


def executar(texto, escolhas):
    Completion.escolhas = list(escolhas)
    resposta = submit_question(texto)
    return resposta, Completion.pedidos
