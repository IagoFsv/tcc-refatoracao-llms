class Completion:
    """Mesma interface de openai.Completion (biblioteca openai anterior a 1.0).

    create registra a chave e os parametros de cada pedido e devolve as
    escolhas preparadas em `escolhas`.
    """

    @classmethod
    def create(cls, **kwargs):
        cls._register_pedido(openai.api_key, kwargs)
        return {"choices": [cls._escolha(texto) for texto in cls._get_escolhas()]}

    @classmethod
    def _register_pedido(cls, api_key, kwargs):
        cls.pedidos.append((api_key, kwargs))

    @classmethod
    def _get_escolhas(cls):
        return cls.escolhas

    @staticmethod
    def _escolha(texto):
        return {"text": texto}


class Pedido:
    """Representa um pedido ao OpenAI API"""

    def __init__(self, api_key, kwargs):
        self.api_key = api_key
        self.kwargs = kwargs

    def __repr__(self):
        return f"Pedido({self.api_key}, {self.kwargs})"


class Escolhas:
    """Representa as escolhas para um pedido ao OpenAI API"""

    def __init__(self, escolhas):
        self.escolhas = escolhas

    def __repr__(self):
        return f"Escolhas({self.escolhas})"


def submit_question(text):
    """This submits a question to the OpenAI API"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = text

    result = openai.Completion.create(
        prompt=prompt,
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-003",
    )["choices"][0]["text"].strip(" \n")
    return result


def executar(texto, escolhas):
    """Envia a pergunta; devolve a resposta e os pedidos feitos. Ponto de entrada publico desta unidade."""
    pedido = Pedido(openai.api_key, escolhas)
    Completion.pedidos.append(pedido)
    Completion.escolhas = Escolhas(escolhas)
    resposta = submit_question(texto)
    return resposta, [str(p) for p in Completion.pedidos]
