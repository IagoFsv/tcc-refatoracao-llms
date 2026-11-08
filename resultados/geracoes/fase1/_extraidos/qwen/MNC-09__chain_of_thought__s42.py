import toml


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def read_pyproject_toml() -> dict:
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)


def get_project_name_from_toml(toml_data: dict) -> str:
    return get_pep8_compliant_name(toml_data['tool']['poetry']['name'])


def get_project_path() -> str:
    toml_data = read_pyproject_toml()
    project_name = get_project_name_from_toml(toml_data)
    return project_name


def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    return get_project_path()
