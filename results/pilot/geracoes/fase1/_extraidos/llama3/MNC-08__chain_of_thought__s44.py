class CompletionService:
    """Serviço de completar texto"""
    def __init__(self):
        self.pedidos = []

    def create(self, **kwargs):
        self.pedidos.append((openai.api_key, kwargs))
        return {"choices": [self._escolha(texto) for texto in self.get_escolhas()]}

    def get_escolhas(self):
        return []

    def _escolha(self, texto):
        return {"text": texto}


class OpenAiService:
    """Serviço de OpenAI"""
    def __init__(self):
        self.api_key = None

    def submit_question(self, text):
        """Submete uma pergunta ao OpenAI API"""
        self.api_key = os.getenv("OPENAI_API_KEY")
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
    """Envia a pergunta; devolve a resposta e os pedidos feitos"""
    completion_service = CompletionService()
    open_ai_service = OpenAiService()
    completion_service.pedidos = []
    completion_service.escolhas = list(escolhas)
    resposta = open_ai_service.submit_question(texto)
    return resposta, completion_service.pedidos
