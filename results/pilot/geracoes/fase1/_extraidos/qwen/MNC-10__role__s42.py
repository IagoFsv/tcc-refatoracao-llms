import shutil
import toml
from invoke import Context, task

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        poetry = toml.load(file)['tool']['poetry']
        return get_pep8_compliant_name(poetry['name'])

def rename_directory(current_project_path, new_project_name):
    shutil.move(current_project_path, new_project_name)

def update_project_name_in_toml(new_project_name):
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = toml.load(file)
    data['tool']['poetry']['name'] = new_project_name
    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)

@task
def rename_project(_context: Context, project_name: str):
    current_project_path = get_project_path()
    new_project_name = get_pep8_compliant_name(project_name)
    rename_directory(current_project_path, new_project_name)
    update_project_name_in_toml(project_name)

def executar(project_name):
    rename_project(Context(), project_name)
