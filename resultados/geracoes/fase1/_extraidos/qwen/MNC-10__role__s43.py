import shutil
import toml
from invoke import Context, task

def get_pep8_compliant_name(name: str) -> str:
    return name.replace('-', '_')

def get_project_path() -> str:
    """Nome do pacote (com _ no lugar de -) lido do pyproject.toml da pasta atual."""
    with open('pyproject.toml', encoding='utf-8') as file:
        poetry = toml.load(file)['tool']['poetry']
        return get_pep8_compliant_name(poetry['name'])

def update_project_name_in_toml(new_name: str):
    """Atualiza o nome do projeto em pyproject.toml."""
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = toml.load(file)

    data['tool']['poetry']['name'] = new_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)

@task
def rename_project(_context: Context, project_name: str):
    current_project_path = get_project_path()
    new_project_name = get_pep8_compliant_name(project_name)

    # Rename the directory
    shutil.move(current_project_path, new_project_name)

    # Update the project name in pyproject.toml
    update_project_name_in_toml(new_project_name)

def executar(project_name):
    """Renomeia o projeto da pasta atual. Ponto de entrada publico desta unidade."""
    rename_project(Context(), project_name)
