import toml


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def load_project_config() -> dict:
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)


def get_project_path():
    config = load_project_config()
    project_name = get_pep8_compliant_name(config['tool']['poetry']['name'])
    return project_name


def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    return get_project_path()
