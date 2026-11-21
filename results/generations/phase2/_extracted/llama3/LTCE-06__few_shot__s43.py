"""Python-specific override of an entry of an API documentation file.

Public entry point: run(item). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

from typing import Any


def get_python_override(item: Any) -> Any:
    """Get the Python override from the item."""
    return item["langs"].get("overrides").get("python") if item["langs"].get("overrides") else None


def self_or_override(item: Any) -> Any:
    """Return the Python override if available, otherwise return the item."""
    override = get_python_override(item)
    return override if override is not None else item


def run(item):
    """Returns the entry that documents the Python API. Public entry point of this unit."""
    return self_or_override(item)
