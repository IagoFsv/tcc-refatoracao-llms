import toml
from invoke import Context, task, UnexpectedExit, Result

class ContextoDeBuild(Context):
    """Contexto que não roda comandos de verdade.

    Cada chamada de run registra o comando, os argumentos e a versão gravada
    no pyproject.toml naquele momento. Com falhar ligado, o comando termina
    com código 1, como faria um build ou publicação que falhou.
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
    pyproject_string = read_pyproject(pyproject_path)
    pyproject = toml.loads(pyproject_string)
    # change version to today datetime
    pyproject['tool']['poetry']['version'] = version
    write_pyproject(pyproject_path, pyproject)

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
        write_pyproject(pyproject_path, toml.loads(pyproject_string))
        raise exception from exception

    # recover to original
    write_pyproject(pyproject_path, toml.loads(pyproject_string))


def read_pyproject(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def write_pyproject(path: str, pyproject: dict) -> None:
    with open(path, 'w', encoding='utf-8') as file:
        toml.dump(pyproject, file)


def executar(version, falhar_publicacao=False):
    """Roda a publicacao da versao; devolve os comandos registrados. Ponto de entrada publico desta unidade."""
    ContextoDeBuild.comandos = []
    ContextoDeBuild.falhar = falhar_publicacao
    release(ContextoDeBuild(), version)
    return ContextoDeBuild.comandos
