import os
from types import SimpleNamespace


class Completion:
    pedidos = []
    escolhas = []

    @classmethod
    def create(cls, texto, **kwargs):
        cls.pedidos.append((openai.api_key, kwargs, texto))
        return {"choices": [{"text": escolha} for escolha in cls.escolhas]}

    @staticmethod
    def _escolha(texto):
        return {"text": texto}


openai = SimpleNamespace(api_key=None, Completion=Completion)


def summarize(text):
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


def executar(texto, escolhas):
    Completion.escolhas = list(escolhas)
    resumo = summarize(texto)
    pedidos = Completion.pedidos
    return resumo, pedidos
