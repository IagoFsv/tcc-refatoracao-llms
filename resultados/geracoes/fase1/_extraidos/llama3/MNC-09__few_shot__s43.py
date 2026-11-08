import toml

class ProjectConfig:
    def __init__(self, file_path: str):
        with open(file_path, encoding='utf-8') as file:
            self.data = toml.load(file)

    def get_project_name(self) -> str:
        return self.data['tool']['poetry']['name']

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def get_project_path():
    return 'pyproject.toml'

def executar():
    config = ProjectConfig(get_project_path())
    return get_pep8_compliant_name(config.get_project_name())
