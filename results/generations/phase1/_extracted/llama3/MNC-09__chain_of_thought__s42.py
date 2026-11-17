"""Maintenance tasks of a Python project: package name from pyproject.toml.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import toml


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def get_tool(data: dict) -> dict:
    return data.get('tool', {})

def get_poetry(tool: dict) -> dict:
    return tool.get('poetry', {})

def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        tool = get_tool(data)
        poetry = get_poetry(tool)
        project_name = get_pep8_compliant_name(poetry.get('name', ''))
        return project_name


def run():
    """Reads pyproject.toml in the current folder and returns the package name. Public entry point of this unit."""
    return get_project_path()
