"""Tests for instance MNC-14: they pin the observable behavior of run().

Only run() is imported. The test intercepts requests.get with recorded
responses of the bot API (getUpdates and getFile). The refactoring may
reorganize the access to the JSON and the loops; what must not change is the
order of the requests, the returned list of paths (first documents from
replies, then direct documents, without repeats) and the error when getFile
does not bring the result.
"""

import pytest
import requests

from MNC_14 import run

URL = "https://api.telegram.org/bot{}/{}"


class Response:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


def document(file_id):
    return {"document": {"file_id": file_id, "file_name": file_id + ".pdf"}}


def reply_to(file_id):
    return {"message": {"reply_to_message": document(file_id), "text": "see"}}


def direct(file_id):
    return {"message": document(file_id)}


@pytest.fixture
def api(monkeypatch):
    """Intercepts requests.get; returns (requests made, updates, paths)."""
    requests_made = []
    updates = []
    paths = {}

    def fake_get(url, *args, **kwargs):
        requests_made.append(url)
        if url.endswith("/getUpdates"):
            return Response({"ok": True, "result": updates})
        file_id = url.split("file_id=")[1]
        if file_id in paths:
            return Response({"ok": True, "result": {"file_id": file_id, "file_path": paths[file_id]}})
        return Response({"ok": False, "description": "Bad Request: invalid file_id"})

    monkeypatch.setattr(requests, "get", fake_get)
    return requests_made, updates, paths


def test_typical_replies_first_then_direct_without_repeats(api):
    requests_made, updates, paths = api
    updates += [direct("d1"), reply_to("r1"), {"message": {"text": "text only"}},
                reply_to("d1"), direct("d2")]
    paths.update(r1="documents/r1.pdf", d1="documents/d1.pdf", d2="documents/d2.pdf")

    assert run("TOKEN") == ["documents/r1.pdf", "documents/d1.pdf", "documents/d2.pdf"]
    assert requests_made == [
        URL.format("TOKEN", "getUpdates"),
        URL.format("TOKEN", "getFile?file_id=r1"),
        URL.format("TOKEN", "getFile?file_id=d1"),
        URL.format("TOKEN", "getFile?file_id=d2"),
    ]


def test_edge_no_files_and_reply_to_a_message_without_document(api):
    requests_made, updates, _ = api
    updates += [{"message": {"reply_to_message": {"text": "hi"}}}, {"edited_message": {}}]

    assert run("T1") == []
    assert requests_made == [URL.format("T1", "getUpdates")]


def test_invalid_get_file_without_result(api):
    _, updates, _ = api
    updates.append(direct("deleted"))

    with pytest.raises(KeyError):
        run("T1")
