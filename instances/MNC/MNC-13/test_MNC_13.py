"""Tests for instance MNC-13: they pin the observable behavior of run().

Only run() is imported. The test runs in a temporary folder (where users.log
is written), intercepts requests.get with recorded responses of the bot API
and fixes the clock by replacing datetime.datetime. The refactoring may
reorganize the access to the JSON; what must not change is the URL
requested, the value returned for each endpoint, the lines appended to
users.log and the errors.

The tests pin the behavior as it is: in users.log the id comes before the
username (the loop variables are swapped in the original).
"""

import datetime

import pytest
import requests

from MNC_13 import run


class Response:
    def __init__(self, data, status_code=200, text="{}"):
        self.data = data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self.data


class FixedClock(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 10, 14, 9, 30, 0)


@pytest.fixture
def api(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(datetime, "datetime", FixedClock)
    requests_made = []
    responses = {}

    def fake_get(url, *args, **kwargs):
        requests_made.append(url)
        return responses["response"]

    monkeypatch.setattr(requests, "get", fake_get)
    return tmp_path, requests_made, responses


def update(user_id, username=None):
    sender = {"id": user_id}
    if username is not None:
        sender["username"] = username
    return {"message": {"from": sender, "text": "hi"}}


def test_typical_get_updates_lists_users_without_repeats_and_writes_log(api):
    folder, requests_made, responses = api
    result = [update(11, "ana"), update(22, "bia"), update(11, "ana"),
              update(33), {"edited_message": {}}]
    responses["response"] = Response({"ok": True, "result": result})

    assert run("TOKEN", "getUpdates") == [(11, "ana"), (22, "bia")]
    assert requests_made == ["https://api.telegram.org/botTOKEN/getUpdates"]
    assert (folder / "users.log").read_text() == (
        "2026-10-14 09:30:00, TOKEN, 11, ana\n"
        "2026-10-14 09:30:00, TOKEN, 22, bia\n"
    )


def test_edge_get_me_other_endpoint_and_accumulated_log(api):
    folder, requests_made, responses = api
    profile = {"id": 99, "is_bot": True, "first_name": "Robot", "username": "robot_bot"}
    responses["response"] = Response({"ok": True, "result": profile})
    assert run("T1", "getMe") == ("robot_bot", "Robot", 99)

    responses["response"] = Response({"ok": True, "result": True})
    assert run("T1", "deleteWebhook") is None

    (folder / "users.log").write_text("old line\n")
    responses["response"] = Response({"ok": True, "result": [update(5, "caio")]})
    run("T1", "getUpdates")
    assert (folder / "users.log").read_text() == "old line\n2026-10-14 09:30:00, T1, 5, caio\n"
    assert requests_made == [
        "https://api.telegram.org/botT1/getMe",
        "https://api.telegram.org/botT1/deleteWebhook",
        "https://api.telegram.org/botT1/getUpdates",
    ]


def test_invalid_error_status_and_incomplete_profile(api):
    _, _, responses = api
    responses["response"] = Response({}, status_code=401, text='{"ok":false,"error_code":401}')
    with pytest.raises(Exception, match=r'^Error: \{"ok":false,"error_code":401\}$'):
        run("BAD", "getUpdates")

    responses["response"] = Response({"ok": True, "result": {"id": 1}}, text="no name")
    with pytest.raises(Exception, match="^Error: no name$"):
        run("T1", "getMe")
