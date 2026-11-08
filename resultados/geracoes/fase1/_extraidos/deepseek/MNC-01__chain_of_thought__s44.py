class Objective:
    ...

class RecordSet:
    ...

GUARDIAN_RANKS = [
    {
        "number": i + 1,
        "name": node["displayProperties"]["name"],
        "description": node["displayProperties"]["description"],
        "record_sets": [
            {
                "name": record_set_node["displayProperties"]["name"],
                "description": record_set_node["displayProperties"]["description"],
                "objectives": [
                    {
                        "name": objective["displayProperties"]["name"],
                        "description": objective["displayProperties"]["description"],
                        "hash": str(objective["hash"]),
                    }
                    for objective in [
                        Objective(SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(d["recordHash"]))
                        for d in SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(record_set_node["children"]["records"][0]["presentationNodeHash"])["children"]["records"]
                    ]
                ],
                "hash": str(record_set_node["hash"]),
            }
            for record_set_node in child_nodes
        ],
        "completion_record_hash": str(node["completionRecordHash"]),
    }
    for i, node in enumerate(child_nodes)
]

class GuardianRanks(BungieData):
    ...

def executar(data):
    ...
