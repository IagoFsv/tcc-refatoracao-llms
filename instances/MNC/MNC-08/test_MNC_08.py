"""Tests for instance MNC-08: they pin the observable behavior of run().

Only run() is imported. The text completion service is imitated in the
unit: run receives the choices the service would return and returns the
answer and the requests made (key used and parameters). The refactoring may
reorganize the access to the response; what must not change is the request
(key read from OPENAI_API_KEY, model and parameters), the answer (first
choice, without spaces and line breaks at the ends) and the error when no
choice comes back.
"""

import pytest

from MNC_08 import run

PARAMETERS = {
    "temperature": 0,
    "max_tokens": 300,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "model": "text-davinci-003",
}


def test_typical_first_choice_without_spaces_at_the_ends(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    answer, requests_made = run("What is the capital of Norway?", ["\n\nOslo.\n", "Bergen"])

    assert answer == "Oslo."
    assert requests_made == [("test-key", dict(PARAMETERS, prompt="What is the capital of Norway?"))]


def test_edge_tab_kept_and_missing_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    answer, requests_made = run("", [" \n\tOslo\t \n "])

    assert answer == "\tOslo\t"  # only spaces and line breaks leave the ends
    assert requests_made == [(None, dict(PARAMETERS, prompt=""))]


def test_invalid_response_without_choices(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    with pytest.raises(IndexError):
        run("Question", [])
