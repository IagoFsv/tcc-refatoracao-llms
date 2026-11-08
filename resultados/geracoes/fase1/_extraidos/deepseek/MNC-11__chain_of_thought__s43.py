import toml
from invoke import Context, task
from invoke.exceptions import UnexpectedExit
from invoke.runners import Result


class ContextoDeBuild(Context):
    comandos = []
    falhar = False

    def run(self, command, **kwargs):
        with open('pyproject.toml', encoding='utf-8') as arquivo:
            poetry = toml.load(arquivo)['tool']['poetry']
        ContextoDeBuild.comandos.append((command, kwargs, poetry['version']))
        if ContextoDeBuild.falhar:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)


def ler_arquivo_toml(arquivo_path: str) -> dict:
    with open(arquivo_path, 'r', encoding='utf-8') as arquivo:
        return toml.load(arquivo)


def escrever_arquivo_toml(arquivo_path: str, pyproject: dict) -> None:
    with open(arquivo_path, 'w', encoding='utf-8') as arquivo:
        toml.dump(pyproject, arquivo)


def alterar_versao(pyproject: dict, nova_versao: str) -> None:
    pyproject['tool']['poetry']['version'] = nova_versao


@task
def build_publish(context: Context, pyproject_path: str, nova_versao: str) -> None:
    '''Build & Publish to PyPI.'''
    pyproject = ler_arquivo_toml(pyproject_path)
    alterar_versao(pyproject, nova_versao)
    escrever_arquivo_toml(pyproject_path, pyproject)

    # build & publish
    try:
        context.run(
            '''
                poetry build  --no-interaction
                poetry publish  --no-interaction
            ''',
            pty=True,
        )
    except UnexpectedExit as exception:
        escrever_arquivo_toml(pyproject_path, ler_arquivo_toml(pyproject_path))
        raise exception from exception

    # restore original version
    escrever_arquivo_toml(pyproject_path, ler_arquivo_toml(pyproject_path))


def executar(version, falhar_publicacao=False):
    """Roda a publicacao da versao; devolve os comandos registrados. Ponto de entrada publico desta unidade."""
    ContextoDeBuild.comandos = []
    ContextoDeBuild.falhar = falhar_publicacao
    build_publish(ContextoDeBuild(), 'pyproject.toml', version)
    return ContextoDeBuild.comandos
