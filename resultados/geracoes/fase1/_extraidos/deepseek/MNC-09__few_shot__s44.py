import toml

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def get_project_info():
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)


def get_project_name():
    project_info = get_project_info()
    project_name = project_info['tool']['poetry']['name']
    return get_pep8_compliant_name(project_name)


def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    return get_project_name()
