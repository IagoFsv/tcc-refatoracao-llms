import shutil
import toml
from invoke import Context, task


class ProjectRenamer:
    def __init__(self, project_name: str):
        self.project_name = project_name

    def get_pep8_compliant_name(self) -> str:
        return self.project_name.replace('-', '_')

    def get_project_path(self):
        """Nome do pacote  (com _ no lugar de -) lido do pyproject.toml da pasta atual."""
        with open('pyproject.toml', encoding='utf-8') as file:
            poetry = toml.load(file)['tool']['poetry']
            return self.get_pep8_compliant_name(poetry['name'])

    @task
    def rename_project(self, _context: Context):
        # Get the current project path
        current_project_path = self.get_project_path()

        # Rename the directory
        shutil.move(self.get_pep8_compliant_name(current_project_path), self.get_pep8_compliant_name(self.project_name))

        # Update the project name in pyproject.toml
        with open('pyproject.toml', 'r', encoding='utf-8') as file:
            data = toml.load(file)

        data['tool']['poetry']['name'] = self.project_name

        with open('pyproject.toml', 'w', encoding='utf-8') as file:
            toml.dump(data, file)


def executar(project_name):
    """Renomeia o projeto da pasta atual. Ponto de entrada publico desta unidade."""
    renamer = ProjectRenamer(project_name)
    renamer.rename_project(Context())
