"""Sorting of keyed data by key dimensions, value dimensions and categorical order.

Public entry point: run(data, kdims, vdims, key_index). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

import itertools


class Dimension:
    """A named dimension; a non-empty list of values makes it categorical."""

    def __init__(self, name, values=()):
        self.name = name
        self.values = list(values)


def python2sort(x, key=None):
    if len(x) == 0:
        return x
    it = iter(x)
    groups = [[next(it)]]
    for item in it:
        for group in groups:
            try:
                item_precedence = item if key is None else key(item)
                group_precedence = group[0] if key is None else key(group[0])
                item_precedence < group_precedence  # noqa: B015, TypeError if not comparable
                group.append(item)
                break
            except TypeError:
                continue
        else:  # did not break, make new group
            groups.append([item])
    return itertools.chain.from_iterable(sorted(group, key=key) for group in groups)


def dimension_sort(odict, kdims, vdims, key_index):
    """
    Sorts data by key using usual Python tuple sorting semantics
    or sorts in categorical order for any categorical Dimensions.
    """
    sortkws = {}
    ndims = len(kdims)
    dimensions = kdims + vdims
    indexes = [(dimensions[i], int(i not in range(ndims)),
                i if i in range(ndims) else i - ndims)
               for i in key_index]
    cached_values = {d.name: [None] + list(d.values) for d in dimensions}

    if len(set(key_index)) != len(key_index):
        raise ValueError("Cannot sort on duplicated dimensions")
    else:
        sortkws['key'] = lambda x: tuple(cached_values[dim.name].index(x[t][d])
                                         if dim.values else x[t][d]
                                         for i, (dim, t, d) in enumerate(indexes))
    return python2sort(odict.items(), **sortkws)


def _dimension(spec):
    """A name, or a (name, values) pair for a categorical dimension."""
    if isinstance(spec, str):
        return Dimension(spec)
    name, values = spec
    return Dimension(name, values)


def run(data, kdims, vdims, key_index):
    """Sorts the (key, value) items of data by the dimensions at key_index and
    returns them as a list. Public entry point of this unit."""
    kdims = [_dimension(spec) for spec in kdims]
    vdims = [_dimension(spec) for spec in vdims]
    return list(dimension_sort(data, kdims, vdims, key_index))
