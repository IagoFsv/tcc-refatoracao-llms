import json
from types import SimpleNamespace
from datetime import datetime

class Node:
    def __init__(self, hash_, name, description, children=(), records=(), completion=None):
        self.hash = hash_
        self.name = name
        self.description = description
        self.children = children
        self.records = records
        self.completion = completion

class Record:
    def __init__(self, hash_, name, description):
        self.hash = hash_
        self.name = name
        self.description = description

class Objective:
    def __init__(self, definition: dict):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.hash = str(definition["hash"])

    def __repr__(self):
        return f"Objective[\n   {self.name}\n   {self.description}\n  {self.hash}\n]"

class RecordSet:
    def __init__(self, definition: dict):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.objectives = [Objective(SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(d["recordHash"])) for d in definition["children"]["records"]]
        self.hash = str(definition["hash"])

    def __repr__(self):
        return f"RecordSet[\n   {self.name}\n   {self.description}\n   {self.objectives}\n]"

# Rest of the code remains the same
