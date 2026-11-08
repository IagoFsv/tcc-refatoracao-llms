from dataclasses import dataclass

@dataclass
class Pedido:
    texto: str
    escolhas: list

def summarize(texto):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=texto,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"].strip(" \n")

def executar(texto, escolhas):
    resumo = summarize(texto)
    return resumo, [Pedido(texto, escolhas)]

openai = SimpleNamespace(api_key=None, Completion=None)
