"""Maintenance tasks of a Python project: package name from pyproject.toml.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import toml
from typing import Dict


class PyProjectToml:
    def __init__(self, data: Dict):
        self.data = data

    @property
    def project_name(self) -> str:
        return self.data['tool']['poetry']['name']

    @property
    def pep8_compliant_name(self) -> str:
        return self.project_name.replace('-', '_')


def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        pyproject_toml = PyProjectToml(toml.load(file))
        return pyproject_toml.pep8_compliant_name


def run():
    """Reads pyproject.toml in the current folder and returns the package name. Public entry point of this unit."""
    return get_project_path()
