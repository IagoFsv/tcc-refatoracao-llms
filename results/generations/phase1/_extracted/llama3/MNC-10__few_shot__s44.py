"""Maintenance tasks of a Python project: renaming the project.

Public entry point: run(project_name). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import shutil
from dataclasses import dataclass
from typing import Dict, Any

import toml
from invoke import Context, task

@dataclass
class ProjectConfig:
    name: str

@dataclass
class ProjectPath:
    project_path: str
    pep8_compliant_name: str

@dataclass
class RenameConfig:
    project_name: str
    current_project_path: str

@task
def rename_project(_context: Context, rename_config: RenameConfig):
    # Rename the directory
    shutil.move(rename_config.current_project_path, rename_config.project_name)

    # Update the project name in pyproject.toml
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = toml.load(file)

    data['tool']['poetry']['name'] = rename_config.project_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)

def get_project_path() -> ProjectPath:
    """Package name (with _ instead of -) read from pyproject.toml in the current folder."""
    with open('pyproject.toml', encoding='utf-8') as file:
        poetry = toml.load(file)['tool']['poetry']
        return ProjectPath(project_path=poetry['name'], pep8_compliant_name=get_pep8_compliant_name(poetry['name']))

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def run(project_name: str):
    """Renames the project in the current folder. Public entry point of this unit."""
    current_project_path = get_project_path()
    rename_project(Context(), RenameConfig(project_name, current_project_path.pep8_compliant_name))
