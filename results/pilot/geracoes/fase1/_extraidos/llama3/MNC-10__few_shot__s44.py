from dataclasses import dataclass
from typing import List
import shutil
import toml
from invoke import Context, task


@dataclass
class ProjectRenameRequest:
    project_name: str


@task
def rename_project(context: Context, request: ProjectRenameRequest):
    current_project_path = get_project_path()
    shutil.move(get_pep8_compliant_name(current_project_path), get_pep8_compliant_name(request.project_name))
    update_project_name_in_pyproject_toml(request.project_name)


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def get_project_path():
    """Nome do pacote (com _ no lugar de -) lido do pyproject.toml da pasta atual."""
    with open('pyproject.toml', encoding='utf-8') as file:
        poetry = toml.load(file)['tool']['poetry']
        return get_pep8_compliant_name(poetry['name'])


def update_project_name_in_pyproject_toml(project_name: str):
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = toml.load(file)

    data['tool']['poetry']['name'] = project_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)


def executar(project_name: str):
    """Renomeia o projeto da pasta atual. Ponto de entrada publico desta unidade."""
    rename_project(Context(), ProjectRenameRequest(project_name))
