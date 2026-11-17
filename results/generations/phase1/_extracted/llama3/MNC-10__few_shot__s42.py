"""Maintenance tasks of a Python project: renaming the project.

Public entry point: run(project_name). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import shutil
from dataclasses import dataclass
from typing import Dict
from toml import load, dump
from invoke import Context, task


@dataclass
class Project:
    name: str


@dataclass
class Poetry:
    name: str


@dataclass
class Pyproject:
    tool: Dict[str, Poetry]


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def load_pyproject() -> Pyproject:
    with open('pyproject.toml', encoding='utf-8') as file:
        return Pyproject(tool=load(file)['tool']['poetry'])


def rename_project(context: Context, project_name: str):
    current_project_path = get_pep8_compliant_name(load_pyproject().tool.name)
    shutil.move(get_pep8_compliant_name(current_project_path), get_pep8_compliant_name(project_name))
    load_pyproject().tool.name = project_name
    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        dump(load_pyproject(), file)


@task
def rename_project_task(context: Context, project_name: str):
    rename_project(context, project_name)


def run(project_name):
    """Renames the project in the current folder. Public entry point of this unit."""
    rename_project_task(Context(), project_name)
