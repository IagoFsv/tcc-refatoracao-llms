"""Maintenance tasks of a Python project: package name from pyproject.toml.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import toml


class ProjectConfig:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> dict:
        with open(self.file_path, encoding='utf-8') as file:
            return toml.load(file)

    def get_project_name(self) -> str:
        config = self.load()
        return get_pep8_compliant_name(config['tool']['poetry']['name'])


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def run():
    """Reads pyproject.toml in the current folder and returns the package name. Public entry point of this unit."""
    config = ProjectConfig('pyproject.toml')
    return config.get_project_name()
