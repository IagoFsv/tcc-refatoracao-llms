import shutil
import toml
from invoke import Context, task

class ProjectRenamer:
    def __init__(self, context: Context):
        self.context = context

    def get_pep8_compliant_name(self, project_name: str) -> str:
        return project_name.replace('-', '_')

    def get_project_path(self):
        """Nome do pacote (com _ no lugar de -) lido do pyproject.toml da pasta atual."""
        with open('pyproject.toml', encoding='utf-8') as file:
            poetry = toml.load(file)['tool']['poetry']
            return self.get_pep8_compliant_name(poetry['name'])

    def rename_project(self, project_name: str):
        # Get the current project path
        current_project_path = self.get_project_path()

        # Rename the directory
        shutil.move(self.get_pep8_compliant_name(current_project_path), self.get_pep8_compliant_name(project_name))

        # Update the project name in pyproject.toml
        with open('pyproject.toml', 'r', encoding='utf-8') as file:
            data = toml.load(file)

        data['tool']['poetry']['name'] = project_name

        with open('pyproject.toml', 'w', encoding='utf-8') as file:
            toml.dump(data, file)

    def execute(self, project_name: str):
        """Renomeia o projeto da pasta atual. Ponto de entrada publico desta unidade."""
        self.rename_project(project_name)

@task
def executar(context: Context, project_name: str):
    ProjectRenamer(context).execute(project_name)
