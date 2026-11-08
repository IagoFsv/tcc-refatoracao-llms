import toml
from invoke import Context, task, UnexpectedExit, Result
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class ConfiguracaoPoetry:
    version: str

@dataclass
class ContextoDeBuild(Context):
    """Contexto que não roda comandos de verdade.

    Cada chamada de run registra o comando, os argumentos e a versão gravada
    no pyproject.toml naquele momento. Com falhar ligado, o comando termina
    com código 1, como faria um build ou publicação que falhou.
    """

    comandos: List[Tuple[str, Dict[str, Any], ConfiguracaoPoetry]] = field(default_factory=list)
    falhar: bool = False

    def run(self, command: str, **kwargs: Any) -> Result:
        with open('pyproject.toml', encoding='utf-8') as arquivo:
            poetry = toml.load(arquivo)['tool']['poetry']
        self.comandos.append((command, kwargs, ConfiguracaoPoetry(version=poetry['version'])))
        if self.falhar:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)

@task
def release(context: ContextoDeBuild, version: str) -> None:
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

def executar(version: str, falhar_publicacao: bool = False) -> List[Tuple[str, Dict[str, Any], ConfiguracaoPoetry]]:
    """Roda a publicação da versão; devolve os comandos registrados. Ponto de entrada público desta unidade."""
    ContextoDeBuild.comandos = []
    ContextoDeBuild.falhar = falhar_publicacao
    release(ContextoDeBuild(), version)
    return ContextoDeBuild.comandos
