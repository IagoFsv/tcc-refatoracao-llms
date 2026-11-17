"""Maintenance tasks of a Python project: renaming the project.

Public entry point: run(project_name). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import shutil

import toml
from invoke import Context, task


def get_pep8_compliant_name(name: str) -> str:
    return name.replace('-', '_')


@dataclass
class ProjectDetails:
    name: str
    path: str


def get_project_details() -> ProjectDetails:
    """Package name (with _ instead of -) and path read from pyproject.toml in the current folder."""
    with open('pyproject.toml', encoding='utf-8') as file:
        poetry = toml.load(file)['tool']['poetry']
        return ProjectDetails(
            name=poetry['name'],
            path=get_pep8_compliant_name(poetry['name'])
        )


@task
def rename_project(_context: Context, project_name: str):
    # Get the current project details
    project_details = get_project_details()

    # Rename the directory
    shutil.move(project_details.path, get_pep8_compliant_name(project_name))

    # Update the project name in pyproject.toml
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = toml.load(file)

    data['tool']['poetry']['name'] = project_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)


def run(project_name):
    """Renames the project in the current folder. Public entry point of this unit."""
    rename_project(Context(), project_name)
