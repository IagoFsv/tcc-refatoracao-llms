from dataclasses import dataclass, field
from typing import List

@dataclass
class RecordSet:
    name: str
    description: str
    objectives: List[Objective]
    hash: str

@dataclass
class Objective:
    name: str
    description: str
    hash: str

@dataclass
class GuardianRank:
    number: int
    name: str
    description: str
    record_sets: List[RecordSet]
    completion_record_hash: str

@dataclass
class PresentationNode:
    hash: str
    name: str
    description: str
    children: List['PresentationNode']
    records: List[Record]

@dataclass
class Record:
    hash: str
    name: str
    description: str
    children: List[Objective]

_NOS = {
    "3741753466": PresentationNode(
        "3741753466", "Guardian Ranks", "", [PresentationNode("11", "Novato", "Primeiro rank", [PresentationNode("501", "Combate", "Registros de combate", [], ["1001", "1002"])], ["1001", "1002"]), PresentationNode("12", "Veterano", "Segundo rank", [PresentationNode("502", "Colecao", "Registros de colecao", [], ["1003"])], ["1003"])], "9001"),
    "11": PresentationNode("11", "Novato", "Primeiro rank", [PresentationNode("501", "Combate", "Registros de combate", [], ["1001", "1002"])], ["9001"]),
    "12": PresentationNode("12", "Veterano", "Segundo rank", [PresentationNode("502", "Colecao", "Registros de colecao", [], ["1003"])], ["9002"]),
    "501": PresentationNode("501", "Combate", "Registros de combate", [], ["1001", "1002"]),
    "502": PresentationNode("502", "Colecao", "Registros de colecao", [], ["1003"]),
}

_REGISTROS = {
    "1001": Record("1001", "Vitorias", "Venca 10 partidas"),
    "1002": Record("1002", "Pontos", "Junte {var:111} pontos"),
    "1003": Record("1003", "Itens", "Colete {var:111} de {var:222} itens"),
}

GUARDIAN_RANKS = [GuardianRank(i + 1, _NOS.get(f"rank_{i+1}")) for i in range(len(_NOS))]

class GuardianRanks:
    _COMPONENTS = [200,900,1200]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data):
        # ... restante do código ...

def executar(data):
    return GuardianRanks._process_data(data)
