"""Text summary by a text completion service.

Public entry point: run(text, choices). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import os
from types import SimpleNamespace
from dataclasses import dataclass, field
from typing import List

class Request:
    """Same interface as openai.Completion 
    (openai library before 1.0).

    create records the key and the parameters of each request and returns the
    choices prepared in `prepared_choices`.
    """

    requests_made  : List = field(default_factory=list)
    prepared_choices : List = field(default_factory=list)


@dataclass
class Choice:
    text: str

@dataclass
class Completion:
    """Same interface as openai.Completion 
    (openai library before 1.0).

    create records the key and the parameters of each request and returns the
    choices prepared in `prepared_choices`.
    """

    requests_made: List[Request] = field(default_factory=list)
    prepared_choices: List[Choice] = field(default_factory=list)

    @classmethod
    def create(cls, **kwargs):
        cls.requests_made.append(Request(openai.api_key, kwargs))
        return {"choices": [cls._choice(text) for text in cls.prepared_choices]}

    @staticmethod
    def _choice(text):
        return Choice(text)


openai = SimpleNamespace(api_key=None, Completion=Completion())


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
    Completion.requests_made = []
    Completion.prepared_choices = [Choice(text) for text in choices]
    summary = summarize(text)
    return summary, Completion.requests_made
