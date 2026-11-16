import toml
from pathlib import Path

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def get_project_path() -> Path:
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        project_name = get_pep8_compliant_name(data['tool']['poetry']['name'])
        return Path.cwd() / project_name

def executar() -> str:
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    return get_project_path().name
