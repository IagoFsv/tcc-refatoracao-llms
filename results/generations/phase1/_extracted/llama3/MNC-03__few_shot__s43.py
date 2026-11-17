import os
from types import SimpleNamespace


class Choice:
    def __init__(self, text):
        self.text = text


class Completion:
    requests_made = []
    prepared_choices = []

    @classmethod
    def create(cls, **kwargs):
        cls.requests_made.append((openai.api_key, kwargs))
        return {"choices": [cls._choice(text) for text in cls.prepared_choices]}

    @staticmethod
    def _choice(text):
        return Choice(text)


openai = SimpleNamespace(api_key=None, Completion=Completion)


class Summary:
    def __init__(self, text, choices):
        self.text = text
        self.choices = choices


def summarize(text, choices):
    """Summarize a text string and return a summary of the text"""
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return Summary(response["choices"][0]["text"].strip(" \n"), choices)


def run(text, choices):
    """Summarizes text; returns the summary and the requests made. Public entry point of this unit."""
    Completion.requests_made = []
    Completion.prepared_choices = list(choices)
    summary = summarize(text, choices)
    return summary.text, summary.choices
