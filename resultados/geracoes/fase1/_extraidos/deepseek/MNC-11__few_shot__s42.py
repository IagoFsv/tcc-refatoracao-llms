"""Tarefas de manutencao de um projeto Python: gerar e publicar uma versao.

Ponto de entrada publico: executar(version, falhar_publicacao=False). Nao
altere o nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.
"""

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
    """Build & Publish to PyPI."""

    # load pyproject
    pyproject_path = 'pyproject.toml'
    with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
        pyproject = toml.load(pyproject_file)

    # change version to today datetime
    pyproject['tool']['poetry']['version'] = version
    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        toml.dump(pyproject, pyproject_file)

    # build & publish
    try:
        context.run('poetry build --no-interaction', pty=True)
        context.run('poetry publish --no-interaction', pty=True)
    except UnexpectedExit:
        with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
            pyproject = toml.load(pyproject_file)
        with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
            toml.dump(pyproject, pyproject_file)
        raise

    # recover to original
    with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
        pyproject = toml.load(pyproject_file)
    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        toml.dump(pyproject, pyproject_file)


def executar(version: str, falhar_publicacao: bool = False) -> list:
    """Runs the publishing of the version; returns the registered commands. Public entry point of this unit."""
    ContextoDeBuild.comandos.clear()
    ContextoDeBuild.falhar = falhar_publicacao
    release(ContextoDeBuild(), version)
    return ContextoDeBuild.comandos
