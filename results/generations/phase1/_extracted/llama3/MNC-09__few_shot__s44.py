"""Maintenance tasks of a Python project: package name from pyproject.toml.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import toml


class ProjectData:
    def __init__(self, tool):
        self.tool = tool

    @property
    def name(self):
        return self.tool.get('poetry', {}).get('name', '')


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        project_data = ProjectData(data['tool'])
        return get_pep8_compliant_name(project_data.name)


def run():
    """Reads pyproject.toml in the current folder and returns the package name. Public entry point of this unit."""
    return get_project_path()
