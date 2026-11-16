"""Tarefas de manutencao de um projeto Python: renomear o projeto.

Ponto de entrada publico: executar(project_name). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

import shutil
from invoke import Context, task
import toml

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def get_project_path() -> str:
    """Nome do pacote (com _ no lugar de -) lido do pyproject.toml da pasta atual."""
    with open('pyproject.toml', encoding='utf-8') as file:
        return get_pep8_compliant_name(toml.load(file)['tool']['poetry']['name'])

@task
def rename_project(_context: Context, project_name: str):
    current_project_path = get_project_path()
    shutil.move(get_pep8_compliant_name(current_project_path), get_pep8_compliant_name(project_name))
    with open('pyproject.toml', 'r+', encoding='utf-8') as file:
        data = toml.load(file)
        data['tool']['poetry']['name'] = project_name
        file.seek(0)
        toml.dump(data, file)
        file.truncate()

def executar(project_name: str):
    """Renomeia o projeto da pasta atual. Ponto de entrada publico desta unidade."""
    rename_project(Context(), project_name)
