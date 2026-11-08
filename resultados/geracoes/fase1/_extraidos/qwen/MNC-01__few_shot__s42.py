from dataclasses import dataclass, field
from datetime import datetime
import json
from types import SimpleNamespace


@dataclass
class Objective:
    definition: dict
    name: str = field(init=False)
    description: str = field(init=False)
    hash: str = field(init=False)

    def __post_init__(self):
        self.name = self.definition["displayProperties"]["name"]
        self.description = self.definition["displayProperties"]["description"]
        self.hash = str(self.definition["hash"])


@dataclass
class RecordSet:
    definition: dict
    name: str = field(init=False)
    description: str = field(init=False)
    objectives: list = field(init=False)
    hash: str = field(init=False)

    def __post_init__(self):
        self.name = self.definition["displayProperties"]["name"]
        self.description = self.definition["displayProperties"]["description"]
        self.objectives = [Objective(SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(d["recordHash"])) for d in self.definition["children"]["records"]]
        self.hash = str(self.definition["hash"])


@dataclass
class GuardianRank:
    number: int
    definition: dict
    name: str = field(init=False)
    description: str = field(init=False)
    record_sets: list = field(init=False)
    completion_record_hash: str = field(init=False)

    def __post_init__(self):
        self.name = self.definition["displayProperties"]["name"]
        self.description = self.definition["displayProperties"]["description"]
        self.record_sets = [RecordSet(SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"])) for d in self.definition["children"]["presentationNodes"]]
        self.completion_record_hash = str(self.definition["completionRecordHash"])


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


def executar(data):
    """Processa a resposta da API. Ponto de entrada publico desta unidade."""
    return GuardianRanks._process_data(data)
