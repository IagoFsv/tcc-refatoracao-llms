import toml
from invoke import Context, task
from invoke.exceptions import UnexpectedExit
from invoke.runners import Result

class Pyproject:
    """Representa o conteúdo do arquivo pyproject.toml"""

    def __init__(self, path):
        self.path = path
        self.data = self.load()

    def load(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            return toml.loads(file.read())

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as file:
            toml.dump(self.data, file)

class BuildContext(Context):
    """Contexto que não roda comandos de verdade"""

    def __init__(self, falhar=False):
        self.falhar = falhar
        self.comandos = []

    def run(self, command, **kwargs):
        if self.falhar:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)

@task
def release(context: BuildContext, version: str) -> None:
    """Build & Publish to PyPI"""
    pyproject = Pyproject('pyproject.toml')
    pyproject.data['tool']['poetry']['version'] = version
    pyproject.save()

    try:
        context.run(
            '''
                poetry build --no-interaction
                poetry publish --no-interaction
            ''',
            pty=True,
        )
    except UnexpectedExit as exception:
        pyproject.data = pyproject.load()
        raise exception from exception

    pyproject.data = pyproject.load()

def executar(version, falhar_publicacao=False):
    """Roda a publicação da versão; devolve os comandos registrados"""
    context = BuildContext(falhar_publicacao)
    context.comandos = []
    release(context, version)
    return context.comandos
