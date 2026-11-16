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

    commands = []
    fail = False

    def run(self, command, **kwargs):
        with open('pyproject.toml', encoding='utf-8') as file:
            poetry = toml.load(file)['tool']['poetry']
        ContextoDeBuild.commands.append((command, kwargs, poetry['version']))
        if ContextoDeBuild.fail:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)


@task
def release(context: Context, version: str) -> None:
    '''Build & Publish to PyPI.'''

    # load pyproject
    pyproject_path = 'pyproject.toml'
    with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
        pyproject_string = pyproject_file.read()
    pyproject = toml.loads(pyproject_string)
    # change version to today datetime
    pyproject['tool']['poetry']['version'] = version
    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        toml.dump(pyproject, pyproject_file)

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
        with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
            pyproject_file.write(pyproject_string)
        raise exception from exception

    # recover to original
    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        pyproject_file.write(pyproject_string)


def execute(version, fail_publishing=False):
    """Run the publishing of the version; return the registered commands. Public entry point of this unit."""
    ContextoDeBuild.commands = []
    ContextoDeBuild.fail = fail_publishing
    release(ContextoDeBuild(), version)
    return ContextoDeBuild.commands
