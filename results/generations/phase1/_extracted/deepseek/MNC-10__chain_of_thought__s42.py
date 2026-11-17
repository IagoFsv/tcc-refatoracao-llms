"""Maintenance tasks of a Python project: renaming the project.

Public entry point: run(project_name). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import shutil
import toml
from invoke import Context, task


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def read_pyproject_toml():
    """Package name (with _ instead of -) read from pyproject.toml in the current folder."""
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)['tool']['poetry']


def get_project_path() -> str:
    return get_pep8_compliant_name(read_pyproject_toml()['name'])


@task
def rename_project(_context: Context, project_name: str):
    # Get the current project path
    current_project_path = get_project_path()

    # Rename the directory
    shutil.move(get_pep8_compliant_name(current_project_path), get_pep8_compliant_name(project_name))

    # Update the project name in pyproject.toml
    data = read_pyproject_toml()
    data['name'] = project_name
    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)


def run(project_name):
    """Renames the project in the current folder. Public entry point of this unit."""
    rename_project(Context(), project_name)
