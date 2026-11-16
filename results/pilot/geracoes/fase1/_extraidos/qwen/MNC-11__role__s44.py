import toml
from invoke import Context, task
from invoke.exceptions import UnexpectedExit
from invoke.runners import Result


class ContextoDeBuild(Context):
    """Contexto que nao roda comandos de verdade.

    Cada chamada de run registra o comando, os argumentos e a versao gravada
    no pyproject.toml naquele momento. Com falhar ligado, o comando termina
    com codigo 1, como faria um build ou publicacao que falhou.
    """

    comandos = []
    falhar = False

    def run(self, command, **kwargs):
        with open('pyproject.toml', encoding='utf-8') as arquivo:
            poetry = toml.load(arquivo)['tool']['poetry']
        ContextoDeBuild.comandos.append((command, kwargs, poetry['version']))
        if ContextoDeBuild.falhar:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)


@task
def release(context: Context, version: str) -> None:
    '''Build & Publish to PyPI.'''

    # load pyproject
    pyproject_path = 'pyproject.toml'
    pyproject = toml.load(pyproject_path)
    pyproject['tool']['poetry']['version'] = version
    toml.dump(pyproject, pyproject_path)

    # build & publish
    try:
        context.run(
            '''
                poetry build --no-interaction
                poetry publish --no-interaction
            ''',
            pty=True,
        )
    except UnexpectedExit as exception:
        with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
            pyproject_string = pyproject_file.read()
        with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
            toml.dump(pyproject, pyproject_file)
        raise exception from exception


def executar(version, falhar_publicacao=False):
    """Roda a publicacao da versao; devolve os comandos registrados. Ponto de entrada publico desta unidade."""
    ContextoDeBuild.comandos = []
    ContextoDeBuild.falhar = falhar_publicacao
    release(ContextoDeBuild(), version)
    return ContextoDeBuild.comandos
