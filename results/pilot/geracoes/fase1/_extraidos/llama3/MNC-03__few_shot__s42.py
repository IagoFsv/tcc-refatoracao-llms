from dataclasses import dataclass, field
from typing import List

@dataclass
class Escolha:
    texto: str

@dataclass
class Pedido:
    api_key: str
    prompt: str
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float

@dataclass
class Resposta:
    texto: str

openai = SimpleNamespace(api_key=None, Completion=None)

def summarize(text: str) -> Resposta:
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
    return Resposta(texto=response["choices"][0]["text"].strip(" \n"))

def executar(texto: str, escolhas: List[str]) -> tuple:
    Completion = openai.Completion
    Completion.pedidos = []
    Completion.escolhas = escolhas
    resumo = summarize(texto)
    return resumo.texto, Completion.pedidos
