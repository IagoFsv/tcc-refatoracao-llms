"""Tarefas de manutencao de um projeto Python: nome do pacote a partir do pyproject.toml.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import toml

def read_pyproject_toml() -> dict:
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)

def get_project_name(data: dict) -> str:
    return get_pep8_compliant_name(data['tool']['poetry']['name'])

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    data = read_pyproject_toml()
    return get_project_name(data)
