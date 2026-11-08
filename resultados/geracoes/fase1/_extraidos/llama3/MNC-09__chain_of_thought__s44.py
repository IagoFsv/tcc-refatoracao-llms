import toml


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def read_project_file() -> dict:
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)


def get_project_name(data: dict) -> str:
    return get_pep8_compliant_name(data['tool']['poetry']['name'])


def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    file_data = read_project_file()
    return get_project_name(file_data)
