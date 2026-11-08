from dataclasses import dataclass

@dataclass
class Clima:
    nome: str
    descricao: str

def print_clima(clima: Clima):
    if clima is not None:
        print(f"The weather in {clima.nome} is {clima.descricao}")
    else:
        print("Error: Could not get weather")


def executar(clima):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_clima(Clima(clima["name"], clima["weather"][0]["description"]))
