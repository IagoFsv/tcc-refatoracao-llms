import os
from types import SimpleNamespace

class Pedido:
    def __init__(self, api_key, kwargs):
        self.api_key = api_key
        self.kwargs = kwargs

class Escolha:
    def __init__(self, texto):
        self.texto = texto

class Completion:
    """Mesma interface de openai.Completion (biblioteca openai anterior a 1.0)."""

    @classmethod
    def create(cls, **kwargs):
        pedido = Pedido(openai.api_key, kwargs)
        return {"choices": [cls._escolha(texto) for texto in cls.escolhas]}

    @staticmethod
    def _escolha(texto):
        return Escolha(texto)

openai = SimpleNamespace(api_key=None, Completion=Completion)

def submit_question(text):
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

def executar(texto, escolhas):
    """Envia a pergunta; devolve a resposta e os pedidos feitos. Ponto de entrada publico desta unidade."""
    pedidos = []
    escolhas = list(escolhas)
    resposta = submit_question(texto)
    return resposta, pedidos
