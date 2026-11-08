from dataclasses import dataclass, field
from typing import List

@dataclass
class DisplayProperties:
    name: str
    description: str

@dataclass
class PresentationNode:
    hash: str
    displayProperties: DisplayProperties
    children: List[str]
    completionRecordHash: str = None

@dataclass
class Record:
    hash: str
    displayProperties: DisplayProperties
    children: List[str]

@dataclass
class GuardianRank:
    number: int
    displayProperties: DisplayProperties
    record_sets: List[Record]
    completionRecordHash: str

@dataclass
class GuardianRanks:
    _COMPONENTS: List[int]
    _THUMBNAIL_URL: str = None

    @staticmethod
    def _process_data(data):
        # ...

def executar(data):
    """Processa a resposta da API. Ponto de entrada publico desta unidade."""
    return GuardianRanks._process_data(data)

_NOS = {
    PresentationNode("3741753466", "Guardian Ranks", [], "9001"),
    PresentationNode("11", "Novato", ["501"], "9002"),
    PresentationNode("12", "Veterano", ["502"], "9002"),
    PresentationNode("501", "Combate", ["1001", "1002"]),
    PresentationNode("502", "Colecao", ["1003"]),
}

_REGISTROS = {
    Record("1001", "Vitorias", ["Venca 10 partidas"]),
    Record("1002", "Pontos", ["Junte {var:111} pontos"]),
    Record("1003", "Itens", ["Colete {var:111} de {var:222} itens"]),
}

GUARDIAN_RANKS = [GuardianRank(i + 1, node) for i, node in enumerate(_NOS.values())]

root_node = _NOS["3741753466"]
child_nodes = [node for node in _NOS.values() if node in root_node.children]

print(SharkBot.Utils.JSON.dumps(GuardianRanks._process_data(data), indent=2))
