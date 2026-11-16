import os
from types import SimpleNamespace

class OpenAiService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.requests = []

    def create_completion(self, prompt, **kwargs):
        self.requests.append((self.api_key, kwargs))
        return {"choices": [self._process_choice(prompt)]}

    def _process_choice(self, prompt):
        return {"text": prompt}

def submit_question(text, open_ai_service):
    open_ai_service.api_key = os.getenv("OPENAI_API_KEY")
    prompt = text

    result = open_ai_service.create_completion(prompt, temperature=0, max_tokens=300, top_p=1, frequency_penalty=0, presence_penalty=0, model="text-davinci-003")["choices"][0]["text"].strip(" \n")
    return result

def executar(texto, escolhas):
    open_ai_service = OpenAiService(None)
    open_ai_service.requests = []
    open_ai_service.choices = list(escolhas)
    resposta = submit_question(texto, open_ai_service)
    return resposta, open_ai_service.requests
