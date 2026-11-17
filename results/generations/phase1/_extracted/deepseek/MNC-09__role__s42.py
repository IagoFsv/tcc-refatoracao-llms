"""Maintenance tasks of a Python project: package name from pyproject.toml.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import toml


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def read_pyproject_toml():
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)


def get_project_name(data):
    return data['tool']['poetry']['name']


def get_project_path():
    data = read_pyproject_toml()
    project_name = get_project_name(data)
    return get_pep8_compliant_name(project_name)


def run():
    """Reads pyproject.toml in the current folder and returns the package name. Public entry point of this unit."""
    return get_project_path()
