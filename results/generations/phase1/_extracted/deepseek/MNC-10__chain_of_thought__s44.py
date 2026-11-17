"""Maintenance tasks of a Python project: renaming the project.

Public entry point: run(project_name). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import shutil
import toml
from invoke import Context, task


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def read_pyproject_toml() -> dict:
    """Read the pyproject.toml file and return its content."""
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)


def get_project_name_from_pyproject_toml() -> str:
    """Package name (with _ instead of -) read from pyproject.toml in the current folder."""
    poetry = read_pyproject_toml()['tool']['poetry']
    return get_pep8_compliant_name(poetry['name'])


def move_project_directory(current_project_path: str, new_project_name: str):
    """Rename the directory."""
    shutil.move(get_pep8_compliant_name(current_project_path), get_pep8_compliant_name(new_project_name))


def update_project_name_in_pyproject_toml(new_project_name: str):
    """Update the project name in pyproject.toml."""
    data = read_pyproject_toml()
    data['tool']['poetry']['name'] = new_project_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)


@task
def rename_project(_context: Context, project_name: str):
    """Renames the project in the current folder. Public entry point of this unit."""
    current_project_path = get_project_name_from_pyproject_toml()
    move_project_directory(current_project_path, project_name)
    update_project_name_in_pyproject_toml(project_name)


def run(project_name):
    """Renames the project in the current folder. Public entry point of this unit."""
    rename_project(Context(), project_name)
