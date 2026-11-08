import toml

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def read_pyproject_toml():
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        project_name = data['tool']['poetry']['name']
        return project_name

def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    project_name = read_pyproject_toml()
    pep8_compliant_name = get_pep8_compliant_name(project_name)
    return pep8_compliant_name
