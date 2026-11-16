import os
from types import SimpleNamespace

class APIRequest:
    """Classe para lidar com os pedidos da API"""

    pedidos = []

    @classmethod
    def create(cls, **kwargs):
        cls.pedidos.append((openai.api_key, kwargs))

class APIResponse:
    """Classe para lidar com as escolhas"""

    escolhas = []

    @classmethod
    def create(cls, escolhas):
        cls.escolhas = list(escolhas)
        return [cls._escolha(texto) for texto in cls.escolhas]

    @staticmethod
    def _escolha(texto):
        return {"text": texto}

openai = SimpleNamespace(api_key=None, Request=APIRequest, Response=APIResponse)

def submit_question(text):
    """This submits a question to the OpenAI API"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = text

    result = openai.Request.create(
        prompt=prompt,
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-003",
    )

    result = openai.Completion.create(**result)["choices"][0]["text"].strip(" \n")
    return result

def executar(texto, escolhas):
    """Envia a pergunta; devolve a resposta e os pedidos feitos. Ponto de entrada publico desta unidade."""
    APIRequest.pedidos = []
    APIResponse.escolhas = list(escolhas)
    resposta = submit_question(texto)
    return resposta, APIRequest.pedidos
