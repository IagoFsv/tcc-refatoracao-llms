import os
from types import SimpleNamespace


class Order:
    def __init__(self, model, prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
        self.model = model
        self.prompt = prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty


class Choice:
    def __init__(self, text):
        self.text = text


class Completion:
    pedidos = []
    escolhas = []

    @classmethod
    def create(cls, model, prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
        pedido = Order(model, prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty)
        cls.pedidos.append((openai.api_key, pedido))
        cls.escolhas = [Choice(texto) for texto in cls.escolhas]
        return {"choices": [choice.text for choice in cls.escolhas]}

    @staticmethod
    def _escolha(texto):
        return Choice(texto)


openai = SimpleNamespace(api_key=None, Completion=Completion)


def summarize(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")

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
    Completion.pedidos = []
    Completion.escolhas = [Choice(texto) for texto in escolhas]
    resumo = summarize(texto)
    return resumo, Completion.pedidos
