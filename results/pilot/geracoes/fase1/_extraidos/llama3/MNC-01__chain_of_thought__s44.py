class PresentationNode:
    def __init__(self, hash, name, description, children=None, records=None, completion_record_hash=None):
        self.hash = hash
        self.name = name
        self.description = description
        self.children = children or []
        self.records = records or []
        self.completion_record_hash = completion_record_hash

    def __repr__(self):
        return f"PresentationNode[\n  {self.name}\n  {self.description}\n  {self.children}\n  {self.records}\n]"


class Record:
    def __init__(self, hash, name, description):
        self.hash = hash
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Record[\n  {self.name}\n  {self.description}\n]"


_NOS = {
    "3741753466": PresentationNode("3741753466", "Guardian Ranks", "", children=["11", "12"]),
    "11": PresentationNode("11", "Novato", "Primeiro rank", children=["501"], completion_record_hash="9001"),
    "12": PresentationNode("12", "Veterano", "Segundo rank", children=["502"], completion_record_hash="9002"),
    "501": PresentationNode("501", "Combate", "Registros de combate", records=["1001", "1002"]),
    "502": PresentationNode("502", "Colecao", "Registros de colecao", records=["1003"]),
}

_REGISTROS = {
    "1001": Record("1001", "Vitorias", "Venca 10 partidas"),
    "1002": Record("1002", "Pontos", "Junte {var:111} pontos"),
    "1003": Record("1003", "Itens", "Colete {var:111} de {var:222} itens"),
}

_DEFINICOES = SimpleNamespace(
    DestinyPresentationNodeDefinition=SimpleNamespace(get=lambda hash: _NOS.get(hash)),
    DestinyRecordDefinition=SimpleNamespace(get=lambda hash: _REGISTROS.get(hash)),
)
