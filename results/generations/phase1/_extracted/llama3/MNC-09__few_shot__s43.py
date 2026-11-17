"""Maintenance tasks of a Python project: package name from pyproject.toml.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import toml


@dataclass
class Project:
    name: str


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def load_project_data() -> Project:
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        project_name = get_pep8_compliant_name(data['tool']['poetry']['name'])
        return Project(name=project_name)


def run():
    """Reads pyproject.toml in the current folder and returns the package name. Public entry point of this unit."""
    return load_project_data().name
