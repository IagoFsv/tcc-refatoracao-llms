import toml
from invoke import Context, task
from invoke.exceptions import UnexpectedExit
from invoke.runners import Result

class ContextoDeBuild:
    """Contexto que nao roda comandos de verdade."""

    comandos = []
    falhar = False

    def __init__(self, falhar=False):
        self.falhar = falhar

    def run(self, command, **kwargs):
        with open('pyproject.toml', encoding='utf-8') as arquivo:
            poetry = toml.load(arquivo)['tool']['poetry']
        self.comandos.append((command, kwargs, poetry['version']))
        if self.falhar:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)

@task
def release(context: Context, version: str) -> None:
    '''Build & Publish to PyPI.'''
    pyproject_path = 'pyproject.toml'
    pyproject_string = ''
    with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
        pyproject_string = pyproject_file.read()
    pyproject = toml.loads(pyproject_string)
    # change version to today datetime
    pyproject['tool']['poetry']['version'] = version
    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        toml.dump(pyproject, pyproject_file)

    try:
        context.run(
            '''
                poetry build --no-interaction
                poetry publish --no-interaction
            ''',
            pty=True,
        )
    except UnexpectedExit as exception:
        with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
            pyproject_file.write(pyproject_string)
        raise exception from exception

    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        pyproject_file.write(pyproject_string)

def executar(version, falhar_publicacao=False):
    """Roda a publicacao da versao; devolve os comandos registrados. Ponto de entrada publico desta unidade."""
    contexto = ContextoDeBuild(falhar_publicacao)
    contexto.comandos = []
    release(contexto, version)
    return contexto.comandos
