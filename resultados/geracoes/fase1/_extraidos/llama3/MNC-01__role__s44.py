import json
from types import SimpleNamespace
from datetime import datetime

_NOS = {
    "3741753466": {"hash": "3741753466", "displayProperties": {"name": "Guardian Ranks", "description": ""}, "children": [{"presentationNodeHash": "11"}, {"presentationNodeHash": "12"}], "completionRecordHash": "9001"},
    "11": {"hash": "11", "displayProperties": {"name": "Novato", "description": "Primeiro rank"}, "children": [{"presentationNodeHash": "501"}], "completionRecordHash": "9001"},
    "12": {"hash": "12", "displayProperties": {"name": "Veterano", "description": "Segundo rank"}, "children": [{"presentationNodeHash": "502"}], "completionRecordHash": "9002"},
    "501": {"hash": "501", "displayProperties": {"name": "Combate", "description": "Registros de combate"}, "children": [], "records": [{"recordHash": "1001"}, {"recordHash": "1002"}]},
    "502": {"hash": "502", "displayProperties": {"name": "Colecao", "description": "Registros de colecao"}, "children": [], "records": [{"recordHash": "1003"}]},
}

_REGISTROS = {
    "1001": {"hash": "1001", "displayProperties": {"name": "Vitorias", "description": "Venca 10 partidas"}},
    "1002": {"hash": "1002", "displayProperties": {"name": "Pontos", "description": "Junte {var:111} pontos"}},
    "1003": {"hash": "1003", "displayProperties": {"name": "Itens", "description": "Colete {var:111} de {var:222} itens"}},
}

_DEFINICOES = SimpleNamespace(
    DestinyPresentationNodeDefinition=SimpleNamespace(get=lambda hash_: _NOS.get(hash_)),
    DestinyRecordDefinition=SimpleNamespace(get=lambda hash_: _REGISTROS.get(hash_)),
)

SharkBot = SimpleNamespace(
    Destiny=SimpleNamespace(Definitions=_DEFINICOES),
    Utils=SimpleNamespace(JSON=SimpleNamespace(dumps=json.dumps)),
)

class BungieData:
    """Base comum dos coletores de dados da API."""

class Objective:
    def __init__(self, definition: dict):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.hash = str(definition["hash"])

    def __repr__(self):
        return f"Objective[\n  {self.name}\n  {self.description}\n {self.hash}\n]"

class RecordSet:
    def __init__(self, definition: dict):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.objectives = [Objective(SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(d["recordHash"])) for d in definition["children"]["records"]]
        self.hash = str(definition["hash"])

    def __repr__(self):
        return f"RecordSet[\n  {self.name}\n  {self.description}\n  {self.objectives}\n]"

class GuardianRank:
    def __init__(self, number: int, definition: dict):
        self.number = number
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.record_sets = [RecordSet(SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"])) for d in definition["children"]["presentationNodes"]]
        self.completion_record_hash = str(definition["completionRecordHash"])

    def __repr__(self):
        return f"GuardianRank[\n  {self.number}\n  {self.name}\n  {self.description}\n  {self.record_sets}\n {self.completion_record_hash}\n]"

GUARDIAN_RANKS = [GuardianRank(i + 1, SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(f"node{i+1}")) for i in range(2)]

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
