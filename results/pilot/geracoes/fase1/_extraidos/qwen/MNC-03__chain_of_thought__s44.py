import os
from types import SimpleNamespace


class RequestManager:
    """Gerencia os pedidos de resumo."""

    pedidos = []

    @classmethod
    def create_request(cls, **kwargs):
        cls.pedidos.append((os.getenv("OPENAI_API_KEY"), kwargs))
        return cls.pedidos


class Summarizer:
    """Lida com a lógica de resumo."""

    @staticmethod
    def summarize(text):
        openai = SimpleNamespace(api_key=None, Completion=None)
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.Completion = RequestManager

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
    """Resume texto; devolve o resumo e os pedidos feitos. Ponto de entrada publico desta unidade."""
    RequestManager.pedidos = []
    Summarizer.escolhas = list(escolhas)
    resumo = Summarizer.summarize(texto)
    return resumo, RequestManager.pedidos
