"""Entry points declared by the distributions of a working set.

Public entry point: run(distributions, group, name=None). Do not change its
name or signature; the rest of the file may be freely reorganized.
"""


class EntryPoint:
    """Object representing an advertised importable object."""

    def __init__(self, name, value, dist):
        self.name = name
        self.value = value
        self.dist = dist


class Distribution:
    """A distribution and the entry points it declares, by group and name."""

    def __init__(self, project_name, entry_points):
        self.project_name = project_name
        self._ep_map = {}
        for group, entries in entry_points.items():
            self._ep_map[group] = {}
            for name, value in entries.items():
                self._ep_map[group][name] = EntryPoint(name, value, self)

    def get_entry_map(self, group=None):
        """Return the entry point map for `group`, or the full entry map"""
        try:
            ep_map = self._ep_map
        except AttributeError:
            ep_map = self._ep_map = EntryPoint.parse_map(
                self._get_metadata('entry_points.txt'), self
            )
        if group is not None:
            return ep_map.get(group, {})
        return ep_map


class WorkingSet:
    """A collection of active distributions, in the order they were added."""

    def __init__(self, distributions):
        self.distributions = list(distributions)

    def __iter__(self):
        """Yield distributions in the order they were added."""
        return iter(self.distributions)

    def iter_entry_points(self, group, name=None):
        """Yield entry point objects from `group` matching `name`

        If `name` is None, yields all entry points in `group` from all
        distributions in the working set, otherwise only ones matching
        both `group` and `name` are yielded  (in distribution order).
        """
        entries = []
        for dist in self:
            entries.extend(dist.get_entry_map(group).values())
        if name is not None:
            entries = [entry for entry in entries if entry.name == name]
        return entries


def run(distributions, group, name=None):
    """distributions is a list of  (project name, {group: {entry name: value}}).
    Returns (project, entry name, value) for each entry point of the group that
    matches the name. Public entry point of this unit."""
    working_set = WorkingSet(Distribution(project, entries) for project, entries in distributions)
    found = []
    for entry in working_set.iter_entry_points(group, name):
        found.append((entry.dist.project_name, entry.name, entry.value))
    return found
