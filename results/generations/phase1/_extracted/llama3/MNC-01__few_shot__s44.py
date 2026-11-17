"""Destiny 2 Guardian Ranks from the Bungie API response.

Public entry point: run(data). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

import json
from types import SimpleNamespace
from datetime import datetime

import dataclasses
from typing import List

@dataclasses.dataclass
class PresentationNode:
    """Presentation node definition in the manifest format."""
    hash: str
    display_properties: dict
    children: List['PresentationNode']
    records: List['Record']
    completion_record_hash: str

@dataclasses.dataclass
class Record:
    """Record definition in the manifest format."""
    hash: str
    display_properties: dict

@dataclasses.dataclass
class GuardianRank:
    """Guardian rank definition."""
    number: int
    name: str
    description: str
    record_sets: List['RecordSet']
    completion_record_hash: str

@dataclasses.dataclass
class RecordSet:
    """Record set definition."""
    name: str
    description: str
    objectives: List['Objective']

@dataclasses.dataclass
class Objective:
    """Objective definition."""
    name: str
    description: str
    hash: str

_NODES = {
    "3741753466": PresentationNode("3741753466", {"name": "Guardian Ranks", "description": ""}, children=["11", "12"], records=[], completion="9001"),
    "11": PresentationNode("11", {"name": "Rookie", "description": "First rank"}, children=["501"], records=[], completion="9002"),
    "12": PresentationNode("12", {"name": "Veteran", "description": "Second rank"}, children=["502"], records=[], completion="9003"),
    "501": PresentationNode("501", {"name": "Combat", "description": "Combat records"}, records=["1001", "1002"]),
    "502": PresentationNode("502", {"name": "Collection", "description": "Collection records"}, records=["1003"],),
}

_RECORDS = {
    "1001": Record("1001", {"name": "Victories", "description": "Win 10 matches"}),
    "1002": Record("1002", {"name": "Points", "description": "Earn {var:111} points"}),
    "1003": Record("1003", {"name": "Items", "description": "Collect {var:111} of {var:222} items"}),
}

_DEFINITIONS = SimpleNamespace(
    DestinyPresentationNodeDefinition=SimpleNamespace(get=lambda hash: _NODES.get(hash)),
    DestinyRecordDefinition=SimpleNamespace(get=lambda hash: _RECORDS.get(hash)),
)

SharkBot = SimpleNamespace(
    Destiny=SimpleNamespace(Definitions=_DEFINITIONS),
    Utils=SimpleNamespace(JSON=SimpleNamespace(dumps=json.dumps)),
)

GUARDIAN_RANKS = [GuardianRank(i + 1, node) for i, node in enumerate([SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"]) for d in _NODES["3741753466"]["children"]["presentationNodes"]])]

class GuardianRanks:
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


def run(data):
    """Processes the API response. Public entry point of this unit."""
    return GuardianRanks._process_data(data)
