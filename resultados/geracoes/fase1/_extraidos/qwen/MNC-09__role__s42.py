import toml


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def get_project_name_from_toml(file_path: str) -> str:
    with open(file_path, encoding='utf-8') as file:
        data = toml.load(file)
        return get_pep8_compliant_name(data['tool']['poetry']['name'])


def get_project_path():
    return get_project_name_from_toml('pyproject.toml')


def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    return get_project_path()
