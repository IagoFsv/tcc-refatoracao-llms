import os
from types import SimpleNamespace
import openai

class Completion:
    """Mesma interface de openai.Completion (biblioteca openai anterior a 1.0).

    create registra a chave e os parametros de cada pedido e devolve as
    escolhas preparadas em `escolhas`.
    """

    def __init__(self):
        self.pedidos = []

    def create(self, **kwargs):
        self.pedidos.append((openai.api_key, kwargs))
        return {"choices": [self._escolha(texto) for texto in self.escolhas]}

    def _escolha(self, texto):
        return {"text": texto}

openai = SimpleNamespace(api_key=None, Completion=Completion())

class Summarizer:
    """Summarize a text string and return a summary of the text"""
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    def summarize(self, text):
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
    completion = Completion()
    completion.escolhas = list(escolhas)
    resumo = Summarizer().summarize(texto)
    return resumo, completion.pedidos
