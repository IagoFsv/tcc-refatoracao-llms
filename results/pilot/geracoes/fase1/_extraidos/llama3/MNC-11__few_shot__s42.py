from dataclasses import dataclass, field
from typing import List

@dataclass
class PyProject:
    tool: dict
    tool_poetry: dict

@dataclass
class ContextoDeBuild:
    comandos: List[tuple]
    falhar: bool

    def run(self, command: str, **kwargs) -> Result:
        self.comandos.append((command, kwargs, self.falhar))
        if self.falhar:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)

@task
def release(context: Context, version: str) -> None:
    """Build & Publish to PyPI."""
    pyproject_path = 'pyproject.toml'
    pyproject_string = ''
    with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
        pyproject_string = pyproject_file.read()
    pyproject = PyProject(**tomy.loads(pyproject_string))
    pyproject.tool_poetry['version'] = version
    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        tomy.dump(pyproject, pyproject_file)

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
    contexto = ContextoDeBuild(comandos=[], falhar=falhar_publicacao)
    release(contexto, version)
    return contexto.comandos
