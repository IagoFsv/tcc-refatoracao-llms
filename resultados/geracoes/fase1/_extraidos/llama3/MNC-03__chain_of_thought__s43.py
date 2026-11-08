import os
from types import SimpleNamespace


class Summary:
    def __init__(self, api_key):
        self.api_key = api_key

    def summarize(self, text, model, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
        response = openai.Completion.create(
            model=model,
            prompt=text,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response["choices"][0]["text"].strip(" \n")


class Completion:
    def __init__(self):
        self.pedidos = []
        self.escolhas = []

    def create(self, **kwargs):
        self.pedidos.append((openai.api_key, kwargs))
        return {"choices": [self._escolha(texto) for texto in self.escolhas]}

    def _escolha(self, texto):
        return {"text": texto}


def executar(texto, escolhas):
    """Resume texto; devolve o resumo e os pedidos feitos. Ponto de entrada publico desta unidade."""
    summary = Summary(os.getenv("OPENAI_API_KEY"))
    resumo = summary.summarize(texto, "text-davinci-002", 0.7, 256, 1, 0, 0)
    return resumo, Completion().pedidos
