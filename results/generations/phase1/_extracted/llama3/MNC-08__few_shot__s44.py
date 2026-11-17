"""Question answered by a text completion service.

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

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.requests_made = []
        self.prepared_choices = []

    def create(self, prompt, **kwargs):
        self.requests_made.append((self.api_key, kwargs))
        return {"choices": [self._choice(text) for text in self.prepared_choices]}

    @staticmethod
    def _choice(text):
        return {"text": text}


openai = SimpleNamespace(api_key=None, Completion=Completion)


class QuestionSubmission:
    """This submits a question to the OpenAI API"""

    def submit_question(self, text):
        self.api_key = os.getenv("OPENAI_API_KEY")
        prompt = text

        result = openai.Completion(self.api_key).create(
            prompt=prompt,
            temperature=0,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model="text-davinci-003",
        )["choices"][0]["text"].strip(" \n")
        return result


def run(text, choices):
    """Submits the question; returns the answer and the requests made. Public entry point of this unit."""
    question_submission = QuestionSubmission()
    question_submission.prepared_choices = list(choices)
    answer = question_submission.submit_question(text)
    return answer, question_submission.requests_made
