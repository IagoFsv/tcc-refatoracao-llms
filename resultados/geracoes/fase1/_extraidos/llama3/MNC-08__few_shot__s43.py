import os
from types import SimpleNamespace

class OpenAiApi:
    def __init__(self, api_key):
        self.api_key = api_key

    def complete_text(self, prompt, **kwargs):
        return {"choices": [{"text": self._escolha_texto(prompt)}]}

    def _escolha_texto(self, texto):
        return texto

def submit_question(text, api):
    api.api_key = os.getenv("OPENAI_API_KEY")
    prompt = text
    return api.complete_text(prompt)["choices"][0]["text"].strip(" \n")

class QuestionSubmitter:
    def __init__(self, api):
        self.api = api

    def executar(self, texto, escolhas):
        self.api.pedidos = []
        self.api.escolhas = list(escolhas)
        resposta = submit_question(texto, self.api)
        return resposta, self.api.pedidos

openai = SimpleNamespace(api_key=None, api=OpenAiApi(None))
submit = QuestionSubmitter(openai)
