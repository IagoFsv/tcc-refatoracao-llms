import os
from types import SimpleNamespace

class APICompletion:
    """Classe para lidar com as chamadas à API (OpenAI)"""

    pedidos = []

    @classmethod
    def create(cls,  **kwargs):
        cls.pedidos.append((openai.api_key, kwargs))
        return openai.Completion.create(**kwargs)


class TextChoices:
    """Classe para lidar com as escolhas de texto"""

    escolhas = []

    @classmethod
    def create(cls, response):
        cls.escolhas = [cls._escolha(choice["text"]) for choice in response["choices"]]
        return cls.escolhas

    @staticmethod
    def _escolha(texto):
        return {"text": texto}


openai = SimpleNamespace(api_key=None, Completion=APICompletion)


def summarize(text):
    """Summarize a text string and return a summary of the text"""
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = APICompletion.create(
        model="text-davinci-002",
        prompt=text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    TextChoices.create(response)


def executar(texto, escolhas):
    """Resume texto; devolve o resumo e os pedidos feitos. Ponto de entrada publico desta unidade."""
    APICompletion.pedidos = []
    TextChoices.escolhas = list(escolhas)
    resumo = summarize(texto)
    return resumo, APICompletion.pedidos
