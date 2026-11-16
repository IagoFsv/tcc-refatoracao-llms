from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class DisplayProperties:
    name: str
    description: str

@dataclass
class Children:
    presentationNodes: List[str] = field(default_factory=list)
    records: List[str] = field(default_factory=list)

@dataclass
class Node:
    hash: str
    displayProperties: DisplayProperties
    children: Children
    completionRecordHash: str = None

@dataclass
class Record:
    hash: str
    displayProperties: DisplayProperties

@dataclass
class BungieData:
    """Base comum dos coletores de dados da API."""

@dataclass
class SharkBot:
    Destiny: Dict[str, Dict[str, Dict[str, Node]]]
    Utils: Dict[str, Dict[str, Dict[str, str]]]

@dataclass
class GuardianRank:
    number: int
    name: str
    description: str
    record_sets: List[Node]
    completion_record_hash: str

@dataclass
class GuardianRanks(BungieData):
    _COMPONENTS: List[int] = field(default_factory=list)
    _THUMBNAIL_URL: str = None

@dataclass
class Objective:
    name: str
    description: str
    hash: str

@dataclass
class RecordSet:
    name: str
    description: str
    objectives: List[Objective]
    hash: str

@dataclass
class VariableData:
    hash: str
    value: int

def executar(data):
    """Processa a resposta da API. Ponto de entrada publico desta unidade."""
    pass
