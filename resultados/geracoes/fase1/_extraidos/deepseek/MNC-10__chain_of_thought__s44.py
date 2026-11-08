import shutil
import toml
from invoke import Context, task


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def read_project_name_from_pyproject_toml():
    """Lê o nome do pacote (com _ no lugar de -) do arquivo pyproject.toml da pasta atual."""
    with open('pyproject.toml', encoding='utf-8') as file:
        poetry = toml.load(file)['tool']['poetry']
        return get_pep8_compliant_name(poetry['name'])


@task
def rename_project_directory(_context: Context, project_name: str):
    # Get the current project path
    current_project_path = read_project_name_from_pyproject_toml()

    # Rename the directory
    shutil.move(get_pep8_compliant_name(current_project_path), get_pep8_compliant_name(project_name))


@task
def update_project_name_in_pyproject_toml(project_name: str):
    # Update the project name in pyproject.toml
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = toml.load(file)

    data['tool']['poetry']['name'] = project_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)


def execute(project_name):
    """Renomeia o projeto da pasta atual. Ponto de entrada publico desta unidade."""
    rename_project_directory(Context(), project_name)
    update_project_name_in_pyproject_toml(project_name)
