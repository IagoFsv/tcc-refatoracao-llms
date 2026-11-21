"""Python-specific override of an entry of an API documentation file.

Public entry point: run(item). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

from typing import Any


def self_or_override(item: Any) -> Any:
    override = item["langs"].get("overrides")
    if override and isinstance(override, dict) and "python" in override:
        return override["python"]
    return item


def run(item):
    """Returns the entry that documents the Python API. Public entry point of this unit."""
    return self_or_override(item)
