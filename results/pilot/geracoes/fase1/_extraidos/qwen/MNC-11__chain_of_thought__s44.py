import toml
from invoke import Context, task
from invoke.exceptions import UnexpectedExit
from invoke.runners import Result


class ContextoDeBuild(Context):
    """Contexto que não roda comandos de verdade.

    Cada chamada de run registra o comando, os argumentos e a versão gravada
    no pyproject.toml naquele momento. Com falhar ligado, o comando termina
    com código 1, como faria um build ou publicacao que falhou.
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


def carregar_pyproject():
    """Carrega o conteúdo do pyproject.toml."""
    with open('pyproject.toml', 'r', encoding='utf-8') as pyproject_file:
        return toml.loads(pyproject_file.read())


def salvar_pyproject(pyproject):
    """Salva o conteúdo do pyproject.toml."""
    with open('pyproject.toml', 'w', encoding='utf-8') as pyproject_file:
        toml.dump(pyproject, pyproject_file)


def modificar_version(pyproject, version):
    """Modifica a versão no pyproject.toml."""
    pyproject['tool']['poetry']['version'] = version
    return pyproject


def executar_build_publicacao(context: Context):
    """Executa os comandos de build e publicação."""
    try:
        context.run(
            '''
                poetry build --no-interaction
                poetry publish --no-interaction
            ''',
            pty=True,
        )
    except UnexpectedExit as exception:
        raise exception from exception


@task
def release(context: Context, version: str) -> None:
    '''Build & Publish to PyPI.'''

    pyproject = carregar_pyproject()
    pyproject = modificar_version(pyproject, version)
    salvar_pyproject(pyproject)

    executar_build_publicacao(context)


def executar(version, falhar_publicacao=False):
    """Roda a publicacao da versao; devolve os comandos registrados. Ponto de entrada publico desta unidade."""
    ContextoDeBuild.comandos = []
    ContextoDeBuild.falhar = falhar_publicacao
    release(ContextoDeBuild(), version)
    return ContextoDeBuild.comandos
