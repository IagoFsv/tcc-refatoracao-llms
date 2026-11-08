import os
from types import SimpleNamespace


class OpenAI:
    """Mesma interface de openai.Completion 
    (biblioteca openai anterior a 1.0).
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.Completion = self.Completion()

    class Completion:
        """Mesma interface de openai.Completion 
        (biblioteca openai anterior a 1.0).
        """

        def __init__(self):
            self.pedidos = []
            self.escolhas = []

        def create(self, **kwargs):
            self.pedidos.append((self.api_key, kwargs))
            return {"choices": [self._escolha(texto) for texto in self.escolhas]}

        @staticmethod
        def _escolha(texto):
            return {"text": texto}


openai = SimpleNamespace(api_key=None, OpenAI=OpenAI)


def submit_question(text):
    """This submits a question to the OpenAI API"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.OpenAI(openai.api_key)
    prompt = text

    result = openai.OpenAI.Completion.create(
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
    """Envia a pergunta; devolve a resposta e os pedidos feitos. 
    Ponto de entrada publico desta unidade."""
    openai.OpenAI.Completion.pedidos = []
    openai.OpenAI.Completion.escolhas = list(escolhas)
    resposta = submit_question(texto)
    return resposta, openai.OpenAI.Completion.pedidos
