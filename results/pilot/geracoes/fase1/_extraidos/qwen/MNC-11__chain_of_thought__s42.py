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


def carregar_pyproject(version: str) -> dict:
    """Carrega o arquivo pyproject.toml e atualiza a versão."""
    pyproject_path = 'pyproject.toml'
    with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
        pyproject_string = pyproject_file.read()
    pyproject = toml.loads(pyproject_string)
    pyproject['tool']['poetry']['version'] = version
    return pyproject, pyproject_string


def salvar_pyproject(pyproject: dict, pyproject_string: str) -> None:
    """Salva as alterações no arquivo pyproject.toml."""
    with open('pyproject.toml', 'w', encoding='utf-8') as pyproject_file:
        toml.dump(pyproject, pyproject_file)


def executar_build_publicacao(context: Context) -> None:
    """Executa o build e a publicação do projeto."""
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

    # Carrega e atualiza o pyproject.toml
    pyproject, pyproject_string = carregar_pyproject(version)

    # Salva as alterações no pyproject.toml
    salvar_pyproject(pyproject, pyproject_string)

    # Executa o build e a publicação
    executar_build_publicacao(context)

    # Recupera o pyproject.toml ao original
    salvar_pyproject(pyproject, pyproject_string)


def executar(version, falhar_publicacao=False):
    """Roda a publicacao da versao; devolve os comandos registrados. Ponto de entrada publico desta unidade."""
    ContextoDeBuild.comandos = []
    ContextoDeBuild.falhar = falhar_publicacao
    release(ContextoDeBuild(), version)
    return ContextoDeBuild.comandos
