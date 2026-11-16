import toml

def load_project_config() -> dict:
    with open('pyproject.toml', encoding='utf-8') as file:
        return toml.load(file)

def get_project_name(config: dict) -> str:
    return get_pep8_compliant_name(config['tool']['poetry']['name'])

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    config = load_project_config()
    return get_project_name(config)
