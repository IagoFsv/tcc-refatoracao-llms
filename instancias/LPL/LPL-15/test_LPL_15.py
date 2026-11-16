"""Tests for instance LPL-15: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
Block.__init__ into an object, change the signature or split the method, as
long as it updates the call inside the unit; what must not change is the
dictionary representation of the block, including the hash and the default
proof (None).

The block hash is the sha256 of str(index) + str(timestamp) + the hashes of
the transactions + str(previous_hash) + str(proof). Each supporting
transaction has as its hash the sha256 of its own description.
"""

import hashlib

from LPL_15 import run


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_typical_block_with_two_transactions_and_proof():
    fields = {"index": 1, "timestamp": 1700000000.0,
              "transactions": ["Alice->Bob:100", "Bob->Carol:20"],
              "previous_hash": "abc123", "proof": 42}

    block = run(fields)

    hashes = _sha("Alice->Bob:100") + _sha("Bob->Carol:20")
    assert block == {
        "hash": _sha("1" + "1700000000.0" + hashes + "abc123" + "42"),
        "index": 1,
        "timestamp": 1700000000.0,
        "transactions": [{"description": "Alice->Bob:100"}, {"description": "Bob->Carol:20"}],
        "previous_hash": "abc123",
        "proof": 42,
    }


def test_edge_genesis_block_without_transactions_and_without_proof():
    block = run({"index": 0, "timestamp": 1700000000.0, "transactions": [],
                 "previous_hash": None})

    assert block == {
        "hash": _sha("0" + "1700000000.0" + "" + "None" + "None"),
        "index": 0,
        "timestamp": 1700000000.0,
        "transactions": [],
        "previous_hash": None,
        "proof": None,
    }


def test_invalid_data_of_the_wrong_type_is_accepted_without_validation():
    block = run({"index": "first", "timestamp": -1, "transactions": [],
                 "previous_hash": 123, "proof": "x"})

    assert block == {
        "hash": _sha("first" + "-1" + "" + "123" + "x"),
        "index": "first",
        "timestamp": -1,
        "transactions": [],
        "previous_hash": 123,
        "proof": "x",
    }
