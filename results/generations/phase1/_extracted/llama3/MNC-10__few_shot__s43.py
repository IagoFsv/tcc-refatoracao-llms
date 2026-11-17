"""Maintenance tasks of a Python project: renaming the project.

Public entry point: run(project_name). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import shutil
from dataclasses import dataclass
from typing import Dict
from toml import load

@dataclass
class Project:
    name: str

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def get_project_path() -> Project:
    """Package name (with _ instead of -) read from pyproject.toml in the current folder."""
    with open('pyproject.toml', encoding='utf-8') as file:
        data = load(file)
        return Project(name=get_pep8_compliant_name(data['tool']['poetry']['name']))

@dataclass
class RenameProjectConfig:
    current_project_path: str
    project_name: str

@task
def rename_project(_context: Context, config: RenameProjectConfig):
    # Rename the directory
    shutil.move(config.current_project_path, config.project_name)

    # Update the project name in pyproject.toml
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = load(file)

    data['tool']['poetry']['name'] = config.project_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        load(data, file)

def run(project_name: str):
    """Renames the project in the current folder. Public entry point of this unit."""
    config = RenameProjectConfig(current_project_path=get_project_path().name, project_name=project_name)
    rename_project(Context(), config)
