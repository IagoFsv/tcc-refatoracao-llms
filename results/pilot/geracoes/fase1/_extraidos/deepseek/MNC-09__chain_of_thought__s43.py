"""Tarefas de manutenção de um projeto Python: nome do pacote a partir do pyproject.toml.

Ponto de entrada público: executar(). Não altere o nome nem a assinatura
dessa função; o restante do arquivo pode ser reorganizado livremente.
"""

import toml


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def load_data_from_pyproject_toml():
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)


def get_project_name_from_data(data):
    return data['tool']['poetry']['name']


def get_project_path():
    data = load_data_from_pyproject_toml()
    project_name = get_pep8_compliant_name(get_project_name_from_data(data))
    return project_name


def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada público desta unidade."""
    return get_project_path()
