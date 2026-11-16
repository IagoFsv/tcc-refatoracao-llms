"""Tests for instance LPL-16: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
Transaction.__init__ into an object, change the signature or split the
method, as long as it updates the call inside the unit; what must not change
is the dictionary representation of the transaction, including the hash.

The transaction hash is the sha256 of str(sender) + str(receiver) +
str(amount) + str(timestamp).
"""

import hashlib

from LPL_16 import run


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_typical_transfer_between_two_people():
    transaction = run({"sender": "Alice", "receiver": "Bob", "amount": 100,
                       "timestamp": 1700000000.0})

    assert transaction == {
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 100,
        "timestamp": 1700000000.0,
        "hash": _sha("Alice" + "Bob" + "100" + "1700000000.0"),
    }


def test_edge_zero_amount_to_oneself():
    transaction = run({"sender": "Alice", "receiver": "Alice", "amount": 0,
                       "timestamp": 0})

    assert transaction == {
        "sender": "Alice",
        "receiver": "Alice",
        "amount": 0,
        "timestamp": 0,
        "hash": _sha("Alice" + "Alice" + "0" + "0"),
    }


def test_invalid_data_of_the_wrong_type_is_accepted_without_validation():
    transaction = run({"sender": None, "receiver": "Bob", "amount": -50,
                       "timestamp": "yesterday"})

    assert transaction == {
        "sender": None,
        "receiver": "Bob",
        "amount": -50,
        "timestamp": "yesterday",
        "hash": _sha("None" + "Bob" + "-50" + "yesterday"),
    }
