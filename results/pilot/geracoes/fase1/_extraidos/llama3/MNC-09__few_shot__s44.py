import toml

@dataclass
class Project:
    name: str

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def load_project_data() -> Project:
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        return Project(name=get_pep8_compliant_name(data['tool']['poetry']['name']))

def executar():
    """Le o pyproject.toml da pasta atual e devolve o nome do pacote. Ponto de entrada publico desta unidade."""
    return load_project_data().name
