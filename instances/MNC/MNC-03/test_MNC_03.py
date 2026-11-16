"""Tests for instance MNC-03: they pin the observable behavior of run().

Only run() is imported. The text completion service is imitated in the
unit: run receives the choices the service would return and returns the
summary and the requests made (key used and parameters). The refactoring may
reorganize the access to the response; what must not change is the request
(key read from OPENAI_API_KEY, model and parameters), the summary (first
choice, without spaces and line breaks at the ends) and the error when no
choice comes back.
"""

import pytest

from MNC_03 import run

PARAMETERS = {
    "model": "text-davinci-002",
    "temperature": 0.7,
    "max_tokens": 256,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


def test_typical_first_choice_without_spaces_at_the_ends(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    summary, requests_made = run("Long text about the weather.", ["\n\nShort summary.\n", "Another choice"])

    assert summary == "Short summary."
    assert requests_made == [("test-key", dict(PARAMETERS, prompt="Long text about the weather."))]


def test_edge_tab_kept_and_missing_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    summary, requests_made = run("", [" \n\tSummary\t \n "])

    assert summary == "\tSummary\t"  # only spaces and line breaks leave the ends
    assert requests_made == [(None, dict(PARAMETERS, prompt=""))]


def test_invalid_response_without_choices(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    with pytest.raises(IndexError):
        run("Text", [])
