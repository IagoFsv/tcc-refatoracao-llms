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
class PresentationNode:
    hash: str
    displayProperties: DisplayProperties
    children: Children
    completionRecordHash: str = None

@dataclass
class Record:
    hash: str
    displayProperties: DisplayProperties

@dataclass
class Manifest:
    presentationNodes: Dict[str, PresentationNode] = field(default_factory=dict)
    records: Dict[str, Record] = field(default_factory=dict)

@dataclass
class BungieData:
    """Base comum dos coletores de dados da API."""

@dataclass
class Objective:
    name: str
    description: str
    hash: str

@dataclass
class RecordSet:
    name: str
    description: str
    objectives: List[Objective] = field(default_factory=list)
    hash: str = None

@dataclass
class GuardianRank:
    number: int
    name: str
    description: str
    record_sets: List[RecordSet] = field(default_factory=list)
    completion_record_hash: str = None

def executar(data: BungieData):
    """Processa a resposta da API. Ponto de entrada publico desta unidade."""
    return GuardianRanks._process_data(data)

class GuardianRanks(BungieData):
    _COMPONENTS = [200, 900, 1200]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data):
        characters = list(data["characters"]["data"].values())
        characters.sort(key=lambda c: datetime.fromisoformat(c["dateLastPlayed"]), reverse=True)
        character_hash = str(characters[0]["characterId"])
        character_records = data["characterRecords"]["data"][character_hash]["records"]
        character_records |= data["profileRecords"]["data"]["records"]
        variable_data = data["profileStringVariables"]["data"]["integerValuesByHash"]
        variable_data |= data["characterStringVariables"]["data"][character_hash]["integerValuesByHash"]

        output = {}
        for rank in GUARDIAN_RANKS:
            rank_data = {
                "completed": character_records[rank.completion_record_hash]["objectives"][0]["complete"],
                "record_sets": {}
            }
            for record_set in rank.record_sets:
                record_set_data = {}
                for objective in record_set.objectives:
                    record_set_data[objective.hash] = {
                        "completed": character_records[objective.hash]["objectives"][0]["complete"],
                        "completionValue": character_records[objective.hash]["objectives"][0]["completionValue"],
                        "progress": character_records[objective.hash]["objectives"][0]["progress"]
                    }
                    if "{var:" in objective.description:
                        relevant_variable_hashes = [s.split("}")[0] for s in objective.description.split("{var:") if "}" in s]
                        record_set_data[objective.hash]["variables"] = {
                            variable_hash: variable_data[variable_hash] for variable_hash in relevant_variable_hashes
                        }

                rank_data["record_sets"][record_set.hash] = {
                    "completed": all(r["completed"] for r in record_set_data.values()),
                    "records": record_set_data
                }
            output[rank.completion_record_hash] = rank_data
        print(SharkBot.Utils.JSON.dumps(output, indent=2))
        return output
