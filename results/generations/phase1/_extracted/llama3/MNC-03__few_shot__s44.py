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

    def __init__(self, model, prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
        self.model = model
        self.prompt = prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.requests_made = []
        self.prepared_choices = []

    def create(self):
        self.requests_made.append({
            "model": self.model,
            "prompt": self.prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty
        })
        return {"choices": [self._choice(self.prompt)]}

    def _choice(self, text):
        return {"text": text}


openai = SimpleNamespace(api_key=None, Completion=Completion)


class Summary:
    """Summarize a text string and return a summary of the text"""
    def __init__(self, text):
        self.text = text

    def summarize(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = openai.Completion(
            model="text-davinci-002",
            prompt=self.text,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response = completion.create()
        return response["choices"][0]["text"].strip(" \n")


def run(text, choices):
    """Summarizes text; returns the summary and the requests made. Public entry point of this unit."""
    completion = openai.Completion(
        model="text-davinci-002",
        prompt=text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    summary = Summary(text).summarize()
    return summary, completion.requests_made
