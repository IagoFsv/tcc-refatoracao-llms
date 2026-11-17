"""Text summary by a text completion service.

Public entry point: run(text, choices). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import os
from types import SimpleNamespace


class Completion:
    """Same interface as openai.Completion (openai library before 1.0).

    create records the key and the parameters of each request and returns the
    choices prepared in `prepared_choices`.
    """

    requests_made = []
    prepared_choices = []

    @classmethod
    def create(cls, **kwargs):
        cls.requests_made.append((openai.api_key, kwargs))
        return {"choices": [cls._choice(text) for text in cls.prepared_choices]}

    @staticmethod
    def _choice(text):
        return {"text": text}


openai = SimpleNamespace(api_key=None, Completion=Completion)


def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")


def create_completion_request(**kwargs):
    return openai.Completion.create(
        model="text-davinci-002",
        prompt=kwargs["text"],
        temperature=kwargs["temperature"],
        max_tokens=kwargs["max_tokens"],
        top_p=kwargs["top_p"],
        frequency_penalty=kwargs["frequency_penalty"],
        presence_penalty=kwargs["presence_penalty"],
    )


def summarize(text):
    """Summarize a text string and return a summary of the text"""
    openai.api_key = get_openai_api_key()

    response = create_completion_request(text=text, temperature=0.7, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)
    return response["choices"][0]["text"].strip(" \n")


def run(text, choices):
    """Summarizes text; returns the summary and the requests made. Public entry point of this unit."""
    Completion.requests_made = []
    Completion.prepared_choices = list(choices)
    summary = summarize(text)
    return summary, Completion.requests_made
