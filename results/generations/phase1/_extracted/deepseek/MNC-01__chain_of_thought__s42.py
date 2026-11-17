import json
from types import SimpleNamespace
from datetime import datetime


def create_display_properties(name, description):
    """Creates a display properties dictionary."""
    return {"name": name, "description": description}


def create_children(children=(), records=(), completion=None):
    """Creates children dictionary."""
    children = [{"presentationNodeHash": h} for h in children]
    records = [{"recordHash": h} for h in records]
    return {"presentationNodes": children, "records": records}


def create_node(hash_, name, description, children=(), records=(), completion=None):
    """Builds a presentation node definition in the manifest format."""
    return {
        "hash": hash_,
        "displayProperties": create_display_properties(name, description),
        "children": create_children(children, records, completion),
        "completionRecordHash": completion,
    }


def create_record(hash_, name, description):
    """Builds a record definition in the manifest format."""
    return {"hash": hash_, "displayProperties": create_display_properties(name, description)}


# Rest of the code remains the same...

class GuardianRanks(BungieData):
    # Rest of the code remains the same...

    @staticmethod
    def _process_data(data):
        # Rest of the code remains the same...


def run(data):
    """Processes the API response. Public entry point of this unit."""
    return GuardianRanks._process_data(data)
