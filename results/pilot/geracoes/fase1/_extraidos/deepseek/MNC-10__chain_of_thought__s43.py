"""Tarefas de manutenção de um projeto Python: renomear o projeto.

Ponto de entrada público: executar(project_name). Não altere o nome nem a
assinatura dessa função; o restante do arquivo pode ser reorganizado
livremente.
"""

import shutil
import toml
from invoke import Context, task


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def read_pyproject_toml(file_path: str):
    """Lê o pyproject.toml da pasta atual."""
    with open(file_path, encoding='utf-8') as file:
        poetry = toml.load(file)['tool']['poetry']
        return get_pep8_compliant_name(poetry['name'])


def update_pyproject_toml(file_path: str, project_name: str):
    """Atualiza o nome do projeto no pyproject.toml."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = toml.load(file)

    data['tool']['poetry']['name'] = project_name

    with open(file_path, 'w', encoding='utf-8') as file:
        toml.dump(data, file)


@task
def rename_project_dir(context: Context, current_project_path: str, new_project_name: str):
    # Renomeia a pasta
    shutil.move(current_project_path, new_project_name)


def get_project_path():
    """Nome do pacote (com _ no lugar de -) lido do pyproject.toml da pasta atual."""
    return read_pyproject_toml('pyproject.toml')


def rename_project(context: Context, project_name: str):
    """Renomeia o projeto da pasta atual."""
    # Get the current project path
    current_project_path = get_project_path()

    # Rename the directory
    rename_project_dir(context, current_project_path, project_name)

    # Update the project name in pyproject.toml
    update_pyproject_toml('pyproject.toml', project_name)


def executar(project_name):
    """Renomeia o projeto da pasta atual. Ponto de entrada público desta unidade."""
    rename_project(Context(), project_name)
