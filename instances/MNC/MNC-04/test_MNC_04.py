"""Tests for instance MNC-04: they pin the observable behavior of run().

Only run() is imported. The refactoring may split the permissions table into
named parts or build it another way; what must not change is the content of
each permission (environment variables and volumes) and the error on an
unknown service.
"""

import pytest

from MNC_04 import run


def test_typical_permission_with_environment_and_volume():
    assert run("lnd") == {
        "env": {
            "LND_IP": "${LND_IP}",
            "LND_GRPC_PORT": "${LND_GRPC_PORT}",
            "LND_REST_PORT": "${LND_REST_PORT}",
            "BITCOIN_NETWORK": "${BITCOIN_NETWORK}",
        },
        "volumes": ["${LND_DATA_DIR}:/lnd:ro"],
    }


def test_edge_permission_with_environment_only_and_no_volumes():
    permission = run("bitcoind")

    assert "volumes" not in permission
    assert permission == {
        "env": {
            "BITCOIN_IP": "${BITCOIN_IP}",
            "BITCOIN_NETWORK": "${BITCOIN_NETWORK}",
            "BITCOIN_P2P_PORT": "${BITCOIN_P2P_PORT}",
            "BITCOIN_RPC_PORT": "${BITCOIN_RPC_PORT}",
            "BITCOIN_RPC_USER": "${BITCOIN_RPC_USER}",
            "BITCOIN_RPC_PASS": "${BITCOIN_RPC_PASS}",
            "BITCOIN_RPC_AUTH": "${BITCOIN_RPC_AUTH}",
        },
    }


def test_invalid_unknown_service():
    with pytest.raises(KeyError):
        run("electrs")
