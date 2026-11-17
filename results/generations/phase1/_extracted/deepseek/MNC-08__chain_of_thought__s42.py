"""Question answered by a text completion service.

Public entry point: run(text, choices). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import os
from types import SimpleNamespace


class Requests:
    """Records the key and the parameters of each request."""

    requests_made = []

    @classmethod
    def create(cls, api_key, kwargs):
        cls.requests_made.append((api_key, kwargs))


class Choices:
    """Prepares the choices for the completion."""

    prepared_choices = []

    @classmethod
    def create(cls, prompt):
        return {"choices": [cls._choice(text) for text in cls.prepared_choices]}

    @staticmethod
    def _choice(text):
        return {"text": text}


openai = SimpleNamespace(api_key=None, Requests=Requests, Choices=Choices)


def submit_question(text):
    """This submits a question to the OpenAI API"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = text

    result = openai.Choices.create(prompt)["choices"][0]["text"].strip(" \n")
    return result


def run(text, choices):
    """Submits the question; returns the answer and the requests made. Public entry point of this unit."""
    openai.Requests.requests_made = []
    openai.Choices.prepared_choices = list(choices)
    answer = submit_question(text)
    return answer, openai.Requests.requests_made
