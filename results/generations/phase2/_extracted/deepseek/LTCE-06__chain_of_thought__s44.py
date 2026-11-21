from typing import Any

def self_or_override(item: Any) -> Any:
    overrides = item.get("langs", {}).get("overrides", {})
    override = overrides.get("python")
    if override:
        return override
    return item

def run(item):
    """Returns the entry that documents the Python API. Public entry point of this unit."""
    return self_or_override(item)
