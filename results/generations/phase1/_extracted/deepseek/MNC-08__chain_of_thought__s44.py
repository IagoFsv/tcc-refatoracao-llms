"""Question answered by a text completion service.

Public entry point: run(text, choices). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import os
from types import SimpleNamespace


class Completion:
    """Same interface as openai.Completion  (openai library before 1.0).

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


class OpenAI:
    """Wrapper for openai library."""

    def __init__(self):
        self.api_key = None
        self.Completion = Completion

    def submit_question(self, text):
        """This submits a question to the OpenAI API"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        prompt = text

        result = self.Completion.create(
            prompt=prompt,
            temperature=0,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model="text-davinci-003",
        )["choices"][0]["text"].strip(" \n")
        return result

    def run(self, text, choices):
        """Submits the question; returns the answer and the requests made. Public entry point of this unit."""
        self.Completion.requests_made = []
        self.Completion.prepared_choices = list(choices)
        answer = self.submit_question(text)
        return answer, self.Completion.requests_made


openai = OpenAI()
