import toml

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def get_project_details():
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)

def get_project_name(project_details):
    return get_pep8_compliant_name(project_details['tool']['poetry']['name'])

def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    project_details = get_project_details()
    return get_project_name(project_details)
