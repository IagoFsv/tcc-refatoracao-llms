"""Maintenance tasks of a Python project: package name from pyproject.toml.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import toml


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def load_project_config():
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)


def get_project_name(data: dict) -> str:
    return get_pep8_compliant_name(data['tool']['poetry']['name'])


def run():
    """Reads pyproject.toml in the current folder and returns the package name. Public entry point of this unit."""
    config = load_project_config()
    return get_project_name(config)
