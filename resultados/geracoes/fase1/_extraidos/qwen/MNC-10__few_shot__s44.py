import shutil
import toml
from invoke import Context, task

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        poetry = toml.load(file)['tool']['poetry']
        return get_pep8_compliant_name(poetry['name'])

@task
def rename_project(_context: Context, project_name: str):
    current_project_path = get_project_path()
    new_project_name = get_pep8_compliant_name(project_name)

    shutil.move(current_project_path, new_project_name)

    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = toml.load(file)

    data['tool']['poetry']['name'] = project_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)

def executar(project_name):
    rename_project(Context(), project_name)
