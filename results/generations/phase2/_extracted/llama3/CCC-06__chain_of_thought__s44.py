def run(parents):
    """Restores a node from a saved state whose parents are given as {key: parent
    or None} and returns {key: object referenced by the restored node}.
    Public entry point of this unit."""
    node = TransformNode.__new__(TransformNode)
    node.__setstate__({"_invalid": 0, "_shorthand_name": "node", "_parents": dict(parents)})
    restored_parents = {}
    for key, reference in node._parents.items():
        if reference is not None:
            restored_parents[key] = reference()
    return restored_parents
