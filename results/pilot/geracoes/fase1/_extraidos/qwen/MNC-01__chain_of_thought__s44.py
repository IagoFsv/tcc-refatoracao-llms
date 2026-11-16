import json
from types import SimpleNamespace
from datetime import datetime


class Definition:
    def __init__(self, data):
        self.data = data

    def get(self, hash_):
        return self.data[hash_]


class Objective:
    def __init__(self, definition):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.hash = str(definition["hash"])

    def __repr__(self):
        return f"Objective[\n  {self.name}\n  {self.description}\n  {self.hash}\n]"


class Record:
    def __init__(self, definition):
        self.hash = str(definition["hash"])

    def __repr__(self):
        return f"Record[\n  {self.hash}\n]"


class RecordSet:
    def __init__(self, definition, objectives):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.objectives = objectives
        self.hash = str(definition["hash"])

    def __repr__(self):
        return f"RecordSet[\n  {self.name}\n  {self.description}\n  {self.objectives}\n]"


class GuardianRank:
    def __init__(self, number, definition, record_sets):
        self.number = number
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.record_sets = record_sets
        self.completion_record_hash = str(definition["completionRecordHash"])

    def __repr__(self):
        return f"GuardianRank[\n  {self.number}\n  {self.name}\n  {self.description}\n  {self.record_sets}\n  {self.completion_record_hash}\n]"


class GuardianRanks:
    _COMPONENTS = [200, 900, 1200]
    _THUMBNAIL_URL = None

    def __init__(self, definitions):
        self.definitions = definitions

    @staticmethod
    def _process_data(data, definitions):
        characters = list(data["characters"]["data"].values())
        characters.sort(key=lambda c: datetime.fromisoformat(c["dateLastPlayed"]), reverse=True)
        character_hash = str(characters[0]["characterId"])
        character_records = data["characterRecords"]["data"][character_hash]["records"]
        character_records |= data["profileRecords"]["data"]["records"]
        variable_data = data["profileStringVariables"]["data"]["integerValuesByHash"]
        variable_data |= data["characterStringVariables"]["data"][character_hash]["integerValuesByHash"]

        output = {}
        for rank in definitions.guardian_ranks:
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


class BungieData:
    """Base comum dos coletores de dados da API."""


root_node = Definition(_NOS).get("3741753466")

child_nodes = [Definition(_NOS).get(d["presentationNodeHash"]) for d in root_node["children"]["presentationNodes"]]


def executar(data):
    """Processa a resposta da API. Ponto de entrada publico desta unidade."""
    definitions = Definition({
        "guardian_ranks": [
            GuardianRank(i + 1, child_nodes[i], [
                RecordSet(child_nodes[i], [
                    Objective(child_nodes[i])
                ])
            ])
            for i in range(len(child_nodes))
        ]
    })
    return GuardianRanks(definitions).process_data(data)
