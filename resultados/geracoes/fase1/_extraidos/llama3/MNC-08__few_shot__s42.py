from dataclasses import dataclass, field
from typing import List

@dataclass
class Pedidos:
    pedidos: List[tuple]
    escolhas: List[str]

@dataclass
class Escolha:
    texto: str

openai = SimpleNamespace(api_key=None)

def submit_question(text: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    result = openai.Completion.create(
        prompt=text,
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-003",
    )["choices"][0]["text"].strip(" \n")
    return result

def executar(texto: str, escolhas: List[str]) -> tuple:
    pedidos = []
    escolhas = list(escolhas)
    resposta = submit_question(texto)
    return resposta, pedidos
