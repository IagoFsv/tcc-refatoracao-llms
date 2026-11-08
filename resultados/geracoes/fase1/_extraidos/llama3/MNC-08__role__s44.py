import os
from types import SimpleNamespace

class Completion:
    """Mesma interface de openai.Completion (biblioteca openai anterior a 1.0).

    create registra a chave e os parametros de cada pedido e devolve as
    escolhas preparadas em `escolhas`.
    """

    def __init__(self, escolhas):
        self.pedidos = []
        self.escolhas = escolhas

    @classmethod
    def create(cls, **kwargs):
        return cls(kwargs.get("escolhas", []))

    @staticmethod
    def _escolha(texto):
        return {"text": texto}

openai = SimpleNamespace(api_key=None, Completion=Completion)


def submit_question(text, escolhas):
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


def executar(text, escolhas):
    """Envia a pergunta; devolve a resposta e os pedidos feitos. Ponto de entrada publico desta unidade."""
    completion = openai.Completion.create(escolhas=list(escolhas))
    resposta = submit_question(text, completion.escolhas)
    return resposta, completion.pedidos
