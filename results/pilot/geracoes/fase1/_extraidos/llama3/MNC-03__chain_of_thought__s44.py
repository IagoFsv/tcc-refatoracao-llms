class Pedido:
    def __init__(self, api_key, kwargs):
        self.api_key = api_key
        self.kwargs = kwargs

class Escolha:
    def __init__(self, texto):
        self.texto = texto

class Completion:
    def __init__(self):
        self.pedidos = []

    def create(self, **kwargs):
        self.pedidos.append(Pedido(openai.api_key, kwargs))
        return {"choices": [self._escolha(texto) for texto in self.escolhas]}

    def _escolha(self, texto):
        return Escolha(texto)

openai = SimpleNamespace(api_key=None, Completion=Completion())

def summarize(text):
    # ...

def executar(texto, escolhas):
    completion = openai.Completion()
    completion.pedidos = []
    completion.escolhas = list(escolhas)
    resumo = summarize(texto)
    return resumo, completion.pedidos
