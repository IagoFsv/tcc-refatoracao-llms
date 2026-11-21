"""Public names of a toolkit wrapper module, computed when the module loads.

Public entry point: run(extra_names). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import importlib
import sys
import types

wantobjects = 1
TkVersion = 8.6
_default_root = None


class TclError(Exception):
    """Error raised by the toolkit."""


class Variable:
    """Value holder shared with the toolkit."""

    def __init__(self, value=None):
        self._value = value

    def get(self):
        return self._value


def getint(text):
    return int(text)


def _join(value):
    return "  ".join(str(item) for item in value)


def run(extra_names):
    """Loads the module again with extra_names 
    ({name: object}) added to its namespace and returns its public names, 
    sorted. Public entry point of this unit."""
    module = sys.modules[__name__]
    namespace = vars(module)
    namespace.update(extra_names)
    try:
        importlib.reload(module)
        return sorted(__all__)
    finally:
        for name in extra_names:
            namespace.pop(name, None)


__all__ = [name for name, obj in globals().items()
           if not name.startswith('_') and not isinstance(obj, types.ModuleType)
           and name not in {'wantobjects'}
           ]
