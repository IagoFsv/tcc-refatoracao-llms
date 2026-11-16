import os
from types import SimpleNamespace

class Completion:
    """Mesma interface de openai.Completion (biblioteca openai anterior a 1.0).

    create registra a chave e os parametros de cada pedido e devolve as
    escolhas preparadas em `escolhas`.
    """

    _pedidos = []
    _escolhas = []

    @classmethod
    def create(cls, **kwargs):
        cls._pedidos.append((openai.api_key, kwargs))
        return {"choices": [cls._escolha(texto) for texto in cls._escolhas]}

    @classmethod
    def _escolha(cls, texto):
        return {"text": texto}

openai = SimpleNamespace(api_key=None, Completion=Completion)

class Summarizer:
    """Resumo de texto por um servico de completar texto."""

    def __init__(self, api_key):
        self.api_key = api_key

    def summarize(self, texto):
        """Summarize a text string and return a summary of the text"""
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=texto,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response["choices"][0]["text"].strip(" \n")

def executar(texto, escolhas):
    """Resume texto; devolve o resumo e os pedidos feitos. Ponto de entrada publico desta unidade."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    summarizer = Summarizer(openai.api_key)
    Completion._escolhas = list(escolhas)
    resumo = summarizer.summarize(texto)
    return resumo, Completion._pedidos
