from dataclasses import dataclass
from typing import List

@dataclass
class Record:
    name: str
    description: str
    objectives: List['Objective']

@dataclass
class Objective:
    name: str
    description: str
    hash: str

@dataclass
class RecordSet:
    name: str
    description: str
    record: 'Record'

@dataclass
class GuardianRank:
    number: int
    name: str
    description: str
    record_set: 'RecordSet'

@dataclass
class GuardianRanks:
    _COMPONENTS: List[int]
    _THUMBNAIL_URL: str

    @staticmethod
    def _process_data(data):
        # ...

def executar(data):
    """Processa a resposta da API. Ponto de entrada publico desta unidade."""
    return GuardianRanks._process_data(data)

_NOS = {
    "3741753466": {"hash": "3741753466", "displayProperties": {"name": "Guardian Ranks", "description": ""}, "children": {"presentationNodes": ["11", "12"]}},
    "11": {"hash": "11", "displayProperties": {"name": "Novato", "description": "Primeiro rank"}, "children": {"presentationNodes": ["501"], "records": ["1001", "1002"]}},
    "12": {"hash": "12", "displayProperties": {"name": "Veterano", "description": "Segundo rank"}, "children": {"presentationNodes": ["502"], "records": []}},
    "501": {"hash": "501", "displayProperties": {"name": "Combate", "description": "Registros de combate"}, "children": {"presentationNodes": [], "records": ["1001", "1002"]}},
    "502": {"hash": "502", "displayProperties": {"name": "Colecao", "description": "Registros de colecao"}, "children": {"presentationNodes": [], "records": ["1003"]}},
}
_REGISTROS = {
    "1001": {"hash": "1001", "displayProperties": {"name": "Vitorias", "description": "Venca 10 partidas"}},
    "1002": {"hash": "1002", "displayProperties": {"name": "Pontos", "description": "Junte {var:111} pontos"}},
    "1003": {"hash": "1003", "displayProperties": {"name": "Itens", "description": "Colete {var:111} de {var:222} itens"}},
}

_GUARDIAN_RANKS = [GuardianRank(i + 1, _NOS.get(f"child_nodes_{i}")) for i, node in enumerate(child_nodes)]

GUARDIAN_RANKS = GuardianRanks(_COMPONENTS=[200, 900, 1200], _THUMBNAIL_URL=None)
