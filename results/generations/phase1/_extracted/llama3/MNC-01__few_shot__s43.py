"""Destiny 2 Guardian Ranks from the Bungie API response.

Public entry point: run(data). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

import json
from types import SimpleNamespace
from datetime import datetime


def _node(hash_, name, description, children=(), records=(), completion=None):
    """Builds a presentation node definition in the manifest format."""
    children = [{"presentationNodeHash": h} for h in children]
    records = [{"recordHash": h} for h in records]
    return {
        "hash": hash_,
        "displayProperties": {"name": name, "description": description},
        "children": {"presentationNodes": children, "records": records},
        "completionRecordHash": completion,
    }


def _record(hash_, name, description):
    """Builds a record definition in the manifest format."""
    return {"hash": hash_, "displayProperties": {"name": name, "description": description}}


# Fixed excerpt of the Destiny manifest: two ranks, one record set in each.
_NODES = {
    "3741753466": _node("3741753466", "Guardian Ranks", "", children=("11", "12")),
    "11": _node("11", "Rookie", "First rank", children=("501",), completion="9001"),
    "12": _node("12", "Veteran", "Second rank", children=("502",), completion="9002"),
    "501": _node("501", "Combat", "Combat records", records=("1001", "1002")),
    "502": _node("502", "Collection", "Collection records", records=("1003",)),
}
_RECORDS = {
    "1001": _record("1001", "Victories", "Win 10 matches"),
    "1002": _record("1002", "Points", "Earn {var:111} points"),
    "1003": _record("1003", "Items", "Collect {var:111} of {var:222} items"),
}

_DEFINITIONS = SimpleNamespace(
    DestinyPresentationNodeDefinition=SimpleNamespace(get=_NODES.__getitem__),
    DestinyRecordDefinition=SimpleNamespace(get=_RECORDS.__getitem__),
)
SharkBot = SimpleNamespace(
    Destiny=SimpleNamespace(Definitions=_DEFINITIONS),
    Utils=SimpleNamespace(JSON=SimpleNamespace(dumps=json.dumps)),
)


class BungieData:
    """Common base of the API data collectors."""


class GuardianRank:
    def __init__(self, number, node):
        self.number = number
        self.name = node["displayProperties"]["name"]
        self.description = node["displayProperties"]["description"]
        self.record_sets = [self._get_record_set(child_node) for child_node in node["children"]["presentationNodes"]]
        self.completion_record_hash = node["completionRecordHash"]

    def _get_record_set(self, node):
        return {
            "name": node["displayProperties"]["name"],
            "description": node["displayProperties"]["description"],
            "objectives": [self._get_objective(record_hash) for record_hash in node["children"]["records"]]
        }

    def _get_objective(self, record_hash):
        record = SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(record_hash)
        return {
            "name": record["displayProperties"]["name"],
            "description": record["displayProperties"]["description"],
            "hash": record_hash
        }

    def __repr__(self):
        return f"GuardianRank[\n  {self.number}\n  {self.name}\n  {self.description}\n  {self.record_sets}\n {self.completion_record_hash}\n]"


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
        for rank in GuardianRanks._get_guardian_ranks():
            rank_data = {
                "completed": character_records[rank.completion_record_hash]["objectives"][0]["complete"],
                "record_sets": {}
            }
            for record_set in rank.record_sets:
                record_set_data = {}
                for objective in record_set["objectives"]:
                    record_set_data[objective["hash"]] = {
                        "completed": character_records[objective["hash"]]["objectives"][0]["complete"],
                        "completionValue": character_records[objective["hash"]]["objectives"][0]["completionValue"],
                        "progress": character_records[objective["hash"]]["objectives"][0]["progress"]
                    }
                    if "{var:" in objective["description"]:
                        relevant_variable_hashes = [s.split("}")[0] for s in objective["description"].split("{var:") if "}" in s]
                        record_set_data[objective["hash"]]["variables"] = {
                            variable_hash: variable_data[variable_hash] for variable_hash in relevant_variable_hashes
                        }

                rank_data["record_sets"][record_set["name"]] = {
                    "completed": all(r["completed"] for r in record_set_data.values()),
                    "records": record_set_data
                }
            output[rank.completion_record_hash] = rank_data
        print(SharkBot.Utils.JSON.dumps(output, indent=2))
        return output


def run(data):
    """Processes the API response. Public entry point of this unit."""
    return GuardianRanks._process_data(data)


def _get_guardian_ranks():
    root_node = SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get("3741753466")
    return [GuardianRank(i + 1, node) for i, node in enumerate(root_node["children"]["presentationNodes"])]
