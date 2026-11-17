"""Text summary by a text completion service.

Public entry point: run(text, choices). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import os
from types import SimpleNamespace
from dataclasses import dataclass, field
from typing import List

class Request:
    """Same interface as openai.Completion (openai library before 1.0).

    create records the key and the parameters of each request and returns the
    choices prepared in `prepared_choices`.
    """

    requests_made  : List[str] = field(default_factory=list)
    prepared_choices : List[str] = field(default_factory=list)

    @classmethod
    def create(cls, **kwargs):
        cls.requests_made.append((openai.api_key, kwargs))
        return {"choices": [cls._choice(text) for text in cls.prepared_choices]}

    @staticmethod
    def _choice(text):
        return {"text": text}


openai = SimpleNamespace(api_key=None, Completion=Request)


def summarize(text):
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
    return response["choices"][0]["text"].strip(" \n")


def run(text, choices):
    """Summarizes text; returns the summary and the requests made. Public entry point of this unit."""
    openai.Completion.requests_made = []
    openai.Completion.prepared_choices = list(choices)
    summary = summarize(text)
    return summary, openai.Completion.requests_made
