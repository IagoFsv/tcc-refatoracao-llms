"""Node of a tree of transforms that keeps weak references to its parents.

Public entry point: run(parents). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import weakref


class TransformNode:
    """The base class for anything that participates in the transform tree."""

    _VALID, _INVALID_AFFINE_ONLY, _INVALID_FULL = range(3)

    def __init__(self, shorthand_name=None):
        """
        Parameters
        ----------
        shorthand_name : str
            A string representing the "name" of the transform. The name carries
            no significance other than to improve the readability of
            ``str(transform)`` when DEBUG=True.
        """
        self._parents = {}
        # Initially invalid, until first computation.
        self._invalid = self._INVALID_FULL
        self._shorthand_name = shorthand_name or ''

    def __getstate__(self):
        # turn the dictionary with weak values into a normal dictionary
        return {**self.__dict__,
                '_parents': {k: v() for k, v in self._parents.items()}}

    def __setstate__(self, data_dict):
        self.__dict__ = data_dict
        # turn the normal dictionary back into a dictionary with weak values
        # The extra lambda is to provide a callback to remove dead
        # weakrefs from the dictionary when garbage collection is done.
        self._parents = {
            k: weakref.ref(v, lambda _, pop=self._parents.pop, k=k: pop(k))
            for k, v in self._parents.items() if v is not None}


def run(parents):
    """Restores a node from a saved state whose parents are given as {key: parent
    or None} and returns {key: object referenced by the restored node}.
    Public entry point of this unit."""
    node = TransformNode.__new__(TransformNode)
    node.__setstate__({"_invalid": 0, "_shorthand_name": "node", "_parents": dict(parents)})
    result = {}
    for key, reference in node._parents.items():
        result[key] = reference()
    return result
