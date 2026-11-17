"""Maintenance tasks of a Python project: package name from pyproject.toml.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import toml


def get_pep8_compliant_name(name: str) -> str:
    return name.replace('-', '_')


def get_project_name(data: dict) -> str:
    project_name = data['tool']['poetry']['name']
    return get_pep8_compliant_name(project_name)


def get_project_path() -> str:
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        return get_project_name(data)


def run():
    """Reads pyproject.toml in the current folder and returns the package name. Public entry point of this unit."""
    return get_project_path()
