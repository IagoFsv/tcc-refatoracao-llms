"""Tests for instance MNC-21: they pin the observable behavior of run().

Only run() is imported. The test intercepts requests.post with a recorded
streamed response ("data: {...}" lines). The refactoring may reorganize how
the request is built and how the stream is read; what must not change is the
request (URL, headers, JSON body, stream on), the returned text (chunks
joined in order, empty lines and lines that are not JSON ignored) and the
error on a chunk without choices.

The tests pin the behavior as it is, including the defect of the original:
with suffix, the list of extra stops goes in as a single item (a list inside
stops), not as four stops.
"""

import json

import pytest
import requests

from MNC_21 import run

URL = "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions"
HEADERS = {
    "OpenAI-Intent": "copilot-ghost",
    "OpenAI-Organization": "github-copilot",
    "Authorization": "Bearer tok-123",
    "Content-Type": "application/json",
}


class StreamedResponse:
    def __init__(self, lines):
        self.lines = lines

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def iter_lines(self):
        return iter(self.lines)


@pytest.fixture
def api(monkeypatch):
    """Intercepts requests.post; returns (requests made, stream)."""
    requests_made = []
    stream = []

    def fake_post(url, **kwargs):
        requests_made.append((url, kwargs))
        return StreamedResponse(list(stream))

    monkeypatch.setattr(requests, "post", fake_post)
    return requests_made, stream


def chunk(text):
    return ("data: " + json.dumps({"choices": [{"text": text, "index": 0}]})).encode("utf-8")


def body(prompt, suffix, temperature, stops):
    return {
        "prompt": prompt,
        "suffix": suffix,
        "max_tokens": 200,
        "temperature": temperature,
        "top_p": 1,
        "n": 1,
        "stop": stops,
        "stream": True,
        "extra": {"language": "python", "next_indent": 0, "trim_by_indentation": True},
    }


def test_typical_chunks_joined_and_complete_request(api):
    requests_made, stream = api
    stream += [chunk("return "), b"", chunk("a + b"), b"data: [DONE]"]
    prompt = "def add(a, b):\n    "

    assert run(prompt, ["\n\n"]) == "return a + b"

    assert len(requests_made) == 1
    url, kwargs = requests_made[0]
    assert url == URL
    assert kwargs["headers"] == HEADERS
    assert kwargs["stream"] is True
    assert json.loads(kwargs["data"]) == body(prompt, "", 0, ["\n\n"])


def test_edge_suffix_temperature_by_line_count_and_empty_stream(api):
    requests_made, stream = api

    assert run("x = 1\n" * 12, ["\n"], suffix="end") == ""
    for breaks in (3, 4, 13, 21, 22):  # lines counted = breaks - 2
        assert run("x = 1\n" * breaks, []) == ""

    sent = [json.loads(kwargs["data"]) for _, kwargs in requests_made]
    assert sent[0] == body("x = 1\n" * 12, "end", 0.2, ["\n", ["def ", "class ", "if ", "\n#"]])
    assert [s["temperature"] for s in sent[1:]] == [0, 0.2, 0.4, 0.4, 0.8]


def test_invalid_chunk_without_choices(api):
    _, stream = api
    stream += [chunk("ok"), b'data: {"error": "rate limited"}']

    with pytest.raises(KeyError):
        run("def f():\n", [])
