"""Guardian Ranks do Destiny 2 a partir da resposta da API da Bungie.

Ponto de entrada publico: executar(data). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import json
from types import SimpleNamespace
from datetime import datetime


def _no(hash_, nome, descricao, filhos=(), registros=(), conclusao=None):
    """Monta uma definicao de no de apresentacao no formato do manifesto."""
    filhos = [{"presentationNodeHash": h} for h in filhos]
    registros = [{"recordHash": h} for h in registros]
    return {
        "hash": hash_,
        "displayProperties": {"name": nome, "description": descricao},
        "children": {"presentationNodes": filhos, "records": registros},
        "completionRecordHash": conclusao,
    }


def _registro(hash_, nome, descricao):
    """Monta uma definicao de registro no formato do manifesto."""
    return {"hash": hash_, "displayProperties": {"name": nome, "description": descricao}}


# Recorte fixo do manifesto do Destiny: dois ranks, um conjunto de registros
# em cada.
_NOS = {
    "3741753466": _no("3741753466", "Guardian Ranks", "", filhos=("11", "12")),
    "11": _no("11", "Novato", "Primeiro rank", filhos=("501",), conclusao="9001"),
    "12": _no("12", "Veterano", "Segundo rank", filhos=("502",), conclusao="9002"),
    "501": _no("501", "Combate", "Registros de combate", registros=("1001", "1002")),
    "502": _no("502", "Colecao", "Registros de colecao", registros=("1003",)),
}
_REGISTROS = {
    "1001": _registro("1001", "Vitorias", "Venca 10 partidas"),
    "1002": _registro("1002", "Pontos", "Junte {var:111} pontos"),
    "1003": _registro("1003", "Itens", "Colete {var:111} de {var:222} itens"),
}

_DEFINICOES = SimpleNamespace(
    DestinyPresentationNodeDefinition=SimpleNamespace(get=_NOS.__getitem__),
    DestinyRecordDefinition=SimpleNamespace(get=_REGISTROS.__getitem__),
)
SharkBot = SimpleNamespace(
    Destiny=SimpleNamespace(Definitions=_DEFINICOES),
    Utils=SimpleNamespace(JSON=SimpleNamespace(dumps=json.dumps)),
)


class BungieData:
    """Base comum dos coletores de dados da API."""


root_node = SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get("3741753466")

child_nodes = [SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"]) for d in root_node["children"]["presentationNodes"]]


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

GUARDIAN_RANKS = [GuardianRank(i + 1, node) for i, node in enumerate(child_nodes)]


class GuardianRanks(BungieData):
    _COMPONENTS = [200,900,1200]
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
