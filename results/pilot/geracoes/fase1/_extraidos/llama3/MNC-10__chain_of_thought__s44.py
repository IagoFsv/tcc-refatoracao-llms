@task
def rename_project(_context: Context, project_name: str):
    current_project_path = get_project_path()
    rename_directory(current_project_path, project_name)
    update_pyproject_toml(project_name)

def rename_directory(current_project_path: str, new_name: str):
    shutil.move(get_pep8_compliant_name(current_project_path), get_pep8_compliant_name(new_name))

def update_pyproject_toml(project_name: str):
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = toml.load(file)

    data['tool']['poetry']['name'] = project_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)

def executar(project_name):
    """Renomeia o projeto da pasta atual. Ponto de entrada publico desta unidade."""
    rename_project(Context(), project_name)
