"""Tests for instance MNC-05: they pin the observable behavior of run().

Only run() is imported. The refactoring may reorganize the access to the
dictionaries; what must not change is the returned app (services indexed by
container name, without the name key, without the containers list, other
keys intact) and the error on a container without a name.
"""

import pytest

from MNC_05 import run


def container(name, image):
    return {"name": name, "image": image}


def test_typical_containers_become_named_services():
    app = {"id": "shop", "containers": [container("web", "nginx"), container("db", "postgres")]}

    assert run(app) == {
        "id": "shop",
        "services": {"web": {"image": "nginx"}, "db": {"image": "postgres"}},
    }


def test_edge_repeated_name_keeps_the_last_one_and_empty_list():
    app = {"containers": [container("web", "nginx"), container("web", "caddy")]}
    assert run(app) == {"services": {"web": {"image": "caddy"}}}

    assert run({"containers": []}) == {"services": {}}


def test_invalid_container_without_a_name():
    with pytest.raises(KeyError):
        run({"containers": [{"image": "nginx"}]})
