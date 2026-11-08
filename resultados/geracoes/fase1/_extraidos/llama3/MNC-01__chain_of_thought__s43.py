class GuardianRank:
    def __init__(self, number: int, definition: dict):
        self.number = number
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.presentation_nodes = [SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"]) for d in definition["children"]["presentationNodes"]]
        self.completion_record_hash = str(definition["completionRecordHash"])

    def __repr__(self):
        return f"GuardianRank[\n  {self.number}\n  {self.name}\n  {self.description}\n  {self.presentation_nodes}\n {self.completion_record_hash}\n]"


class RecordSet:
    def __init__(self, definition: dict):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.objectives = [Objective(SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(d["recordHash"])) for d in definition["children"]["records"]]
        self.hash = str(definition["hash"])

    def __repr__(self):
        return f"RecordSet[\n  {self.name}\n  {self.description}\n  {self.objectives}\n]"


def _process_guardian_rank(rank: GuardianRank):
    rank_data = {
        "completed": False,
        "record_sets": {}
    }
    for presentation_node in rank.presentation_nodes:
        record_set_data = {}
        for record in presentation_node["children"]["records"]:
            objective = Objective(SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(record["recordHash"]))
            record_set_data[objective.hash] = {
                "completed": False,
                "completionValue": None,
                "progress": None,
                "variables": {}
            }
            if "{var:" in objective.description:
                relevant_variable_hashes = [s.split("}")[0] for s in objective.description.split("{var:") if "}" in s]
                record_set_data[objective.hash]["variables"] = {
                    variable_hash: None for variable_hash in relevant_variable_hashes
                }
        rank_data["record_sets"][presentation_node["presentationNodeHash"]] = {
            "completed": all(r["completed"] for r in record_set_data.values()),
            "records": record_set_data
        }
    return rank_data


def executar(data):
    """Processa a resposta da API. Ponto de entrada publico desta unidade."""
    output = {}
    for rank in GUARDIAN_RANKS:
        rank_data = _process_guardian_rank(rank)
        output[rank.completion_record_hash] = rank_data
    print(SharkBot.Utils.JSON.dumps(output, indent=2))
    return output
