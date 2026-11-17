"""Maintenance tasks of a Python project: package name from pyproject.toml.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import toml


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        tool = data.get('tool')
        if tool is None:
            return None
        poetry = tool.get('poetry')
        if poetry is None:
            return None
        name = poetry.get('name')
        if name is None:
            return None
        return get_pep8_compliant_name(name)


def run():
    """Reads pyproject.toml in the current folder and returns the package name. Public entry point of this unit."""
    return get_project_path()
