import toml

def read_pyproject_toml() -> dict:
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
    return data

def process_project_name(data: dict) -> str:
    project_name = data['tool']['poetry']['name']
    return project_name.replace('-', '_')

def get_project_path() -> str:
    data = read_pyproject_toml()
    project_name = process_project_name(data)
    return project_name

def executar() -> str:
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    return get_project_path()
