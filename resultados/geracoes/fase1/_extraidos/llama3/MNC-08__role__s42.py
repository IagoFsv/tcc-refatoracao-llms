import os
from types import SimpleNamespace

class Completion:
    """Mesma interface de openai.Completion (biblioteca openai anterior a 1.0)."""

    def __init__(self, escolhas):
        self.escolhas = escolhas
        self.pedidos = []

    def create(self, **kwargs):
        self.pedidos.append((openai.api_key, kwargs))
        return {"choices": [self._escolha(texto) for texto in self.escolhas]}

    @staticmethod
    def _escolha(texto):
        return {"text": texto}

openai = SimpleNamespace(api_key=None, Completion=Completion)

class QuestionSubmission:
    """This submits a question to the OpenAI API"""

    def __init__(self, api_key):
        self.api_key = api_key

    def submit_question(self, texto):
        prompt = texto
        result = openai.Completion(self.api_key).create(
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
    completion = Completion(escolhas)
    submission = QuestionSubmission(openai.api_key)
    resposta = submission.submit_question(texto)
    return resposta, completion.pedidos
