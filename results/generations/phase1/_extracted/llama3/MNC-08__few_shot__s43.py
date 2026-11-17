import os
from types import SimpleNamespace


class Choice:
    def __init__(self, text):
        self.text = text


class Completion:
    requests_made = []
    prepared_choices = []

    @classmethod
    def create(cls, prompt):
        cls.requests_made.append(prompt)
        return {"choices": [cls._choice(prompt)]}

    @staticmethod
    def _choice(text):
        return Choice(text)


openai = SimpleNamespace(api_key=None, Completion=Completion)


def submit_question(text):
    """This submits a question to the OpenAI API"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = text
    result = openai.Completion.create(prompt=prompt, model="text-davinci-003")["choices"][0].text.strip(" \n")
    return result


def run(text, choices):
    """Submits the question; returns the answer and the requests made. Public entry point of this unit."""
    Completion.requests_made = []
    Completion.prepared_choices = choices
    answer = submit_question(text)
    return answer, Completion.requests_made
