# ...
class GuardianRank:
    def __init__(self, number: int, definition: dict):
        self.number = number
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.record_sets = [RecordSet(definition["children"]["presentationNodes"][i]) for i in range(len(definition["children"]["presentationNodes"]))]
        self.completion_record_hash = str(definition["completionRecordHash"])

    def __repr__(self):
        return f"GuardianRank[\n  {self.number}\n  {self.name}\n  {self.description}\n  {self.record_sets}\n {self.completion_record_hash}\n]"

# ...
GUARDIAN_RANKS = [GuardianRank(i + 1, node) for i, node in enumerate(child_nodes)]
