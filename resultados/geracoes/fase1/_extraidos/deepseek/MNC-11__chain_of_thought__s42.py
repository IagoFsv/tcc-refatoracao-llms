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
        if ContextoDeBuild.falhar:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)

def ler_pyproject():
    with open('pyproject.toml', encoding='utf-8') as arquivo:
        return toml.load(arquivo)['tool']['poetry']

def escrever_pyproject(pyproject):
    with open('pyproject.toml', 'w', encoding='utf-8') as arquivo:
        toml.dump(pyproject, arquivo)

def gerar_versao(version):
    pyproject = ler_pyproject()
    pyproject['version'] = version
    escrever_pyproject(pyproject)

def publicar(context: Context):
    '''Build & Publish to PyPI.'''
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
    gerar_versao(version)
    publicar(context)
    escrever_pyproject(ler_pyproject())

def executar(version, falhar_publicacao=False):
    """Roda a publicacao da versao; devolve os comandos registrados. Ponto de entrada publico desta unidade."""
    ContextoDeBuild.comandos = []
    ContextoDeBuild.falhar = falhar_publicacao
    release(ContextoDeBuild(), version)
    return ContextoDeBuild.comandos
