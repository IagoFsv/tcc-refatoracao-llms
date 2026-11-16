"""Tarefas de manutenção de um projeto Python: nome do pacote a partir do pyproject.toml.

Ponto de entrada público: executar(). Não altere o nome nem a assinatura
dessa função; o restante do arquivo pode ser reorganizado livremente.
"""

import toml


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        project_name = get_pep8_compliant_name(data['tool']['poetry']['name'])
        return project_name


def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada público desta unidade."""
    return get_project_path()
