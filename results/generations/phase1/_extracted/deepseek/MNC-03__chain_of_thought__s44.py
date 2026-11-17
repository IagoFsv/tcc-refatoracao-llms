"""Text summary by a text completion service.

Public entry point: run(text, choices). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import os
from types import SimpleNamespace


class RequestsMade:
    """Encapsulates the functionality related to requests made."""

    requests_made = []

    @classmethod
    def create(cls, api_key, kwargs):
        cls.requests_made.append((api_key, kwargs))


class PreparedChoices:
    """Encapsulates the functionality related to prepared choices."""

    prepared_choices = []

    @classmethod
    def create(cls, choices):
        cls.prepared_choices = list(choices)
        return [cls._choice(text) for text in cls.prepared_choices]

    @staticmethod
    def _choice(text):
        return {"text": text}


class Completion:
    """Same interface as openai.Completion 
    (openai library before 1.0).
    """

    @classmethod
    def create(cls, **kwargs):
        api_key = os.getenv("OPENAI_API_KEY")
        RequestsMade.create(api_key, kwargs)
        choices = PreparedChoices.create(RequestsMade.requests_made)
        return {"choices": choices}


openai = SimpleNamespace(api_key=None, Completion=Completion)


def summarize(text):
    """Summarize a text string and return a summary of the text"""
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"].strip(" \n")


def run(text, choices):
    """Summarizes text; returns the summary and the requests made. Public 
    entry point of this unit."""
    PreparedChoices.create(choices)
    summary = summarize(text)
    return summary, RequestsMade.requests_made
