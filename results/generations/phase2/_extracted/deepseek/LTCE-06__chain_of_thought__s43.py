from typing import Any


def self_or_override(item: Any) -> Any:
    if item["langs"].get("overrides"):
        override = item["langs"].get("overrides").get("python")
    else:
        override = None
    return override or item


def run(item):
    """Returns the entry that documents the Python API. Public entry point of this unit."""
    return self_or_override(item)
