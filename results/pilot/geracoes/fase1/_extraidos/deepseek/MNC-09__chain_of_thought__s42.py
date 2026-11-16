import toml

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def read_pyproject_toml():
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)

def get_project_data(data):
    return data['tool']['poetry']['name']

def get_project_path():
    data = read_pyproject_toml()
    project_name = get_project_data(data)
    return get_pep8_compliant_name(project_name)

def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    return get_project_path()
