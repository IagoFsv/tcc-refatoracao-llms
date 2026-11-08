from dataclasses import dataclass

@dataclass
class Pedido:
    texto: str
    escolhas: list

@dataclass
class Resposta:
    texto: str

def submit_question(texto):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    result = openai.Completion.create(
        prompt=texto,
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-003",
    )["choices"][0]["text"].strip(" \n")
    return Resposta(texto=result)

def executar(texto, escolhas):
    pedido = Pedido(texto=texto, escolhas=list(escolhas))
    resposta = submit_question(texto)
    return resposta, [pedido]
