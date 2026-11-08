import os
from types import SimpleNamespace

class CompletionRequest:
    """Mesma interface de openai.Completion (biblioteca openai anterior a 1.0).

    create registra a chave e os parametros de cada pedido e devolve as
    escolhas preparadas em `escolhas`.
    """

    pedidos = []
    escolhas = []

    @classmethod
    def create(cls, **kwargs):
        cls.pedidos.append((openai.api_key, kwargs))
        return cls._escolha(cls.escolhas)

    @staticmethod
    def _escolha(escolhas):
        return {"choices": [{"text": texto} for texto in escolhas]}


class CompletionResponse:
    """Classe para lidar com a resposta da Completion"""

    @staticmethod
    def process(response):
        return response["choices"][0]["text"].strip(" \n")


openai = SimpleNamespace(api_key=None, Completion=CompletionRequest)


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
    )
    return CompletionResponse.process(result)


def executar(texto, escolhas):
    """Envia a pergunta; devolve a resposta e os pedidos feitos. Ponto de entrada publico desta unidade."""
    CompletionRequest.pedidos = []
    CompletionRequest.escolhas = list(escolhas)
    resposta = submit_question(texto)
    return resposta, CompletionRequest.pedidos
