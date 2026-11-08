import shutil
import toml
from invoke import Context, task

@dataclass
class ProjectInfo:
    name: str
    path: str

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def get_project_info():
    """Lê o nome do pacote (com _ no lugar de -) e o caminho do pyproject.toml."""
    with open('pyproject.toml', encoding='utf-8') as file:
        poetry = toml.load(file)['tool']['poetry']
        return ProjectInfo(
            name=poetry['name'],
            path=get_pep8_compliant_name(poetry['name'])
        )

@task
def rename_project(_context: Context, project_name: str):
    project_info = get_project_info()

    # Rename the directory
    shutil.move(project_info.path, get_pep8_compliant_name(project_name))

    # Update the project name in pyproject.toml
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = toml.load(file)

    data['tool']['poetry']['name'] = project_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)

def executar(project_name):
    """Renomeia o projeto da pasta atual. Ponto de entrada publico desta unidade."""
    rename_project(Context(), project_name)
