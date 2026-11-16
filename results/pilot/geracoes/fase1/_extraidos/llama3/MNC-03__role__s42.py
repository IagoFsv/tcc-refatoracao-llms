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

class TextCompletion:
    def __init__(self, texto, escolhas):
        self.texto = texto
        self.escolhas = escolhas

    def summarize(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion(self.escolhas).create(
            model="text-davinci-002",
            prompt=self.texto,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response["choices"][0]["text"].strip(" \n")

    def execute(self):
        return self.summarize(), self.escolhas

def executar(texto, escolhas):
    return TextCompletion(texto, list(escolhas)).execute()
