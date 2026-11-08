from toml import loads, dumps
from invoke import Context, task
from invoke.exceptions import UnexpectedExit
from invoke.runners import Result

class BuildContext:
    comandos = []
    falhar = False

    def __init__(self, context: Context):
        self.context = context

    def run(self, command, **kwargs):
        self.comandos.append((command, kwargs))
        if self.falhar:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)

@task
def release(context: Context, version: str) -> None:
    """Build & Publish to PyPI."""
    pyproject_path = 'pyproject.toml'
    with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
        pyproject_string = pyproject_file.read()
    pyproject = loads(pyproject_string)
    pyproject['tool']['poetry']['version'] = version
    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        dumps(pyproject, file=pyproject_file)

    try:
        self.context.run(
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
    context = Context()
    build_context = BuildContext(context)
    build_context.falhar = falhar_publicacao
    release(build_context, version)
    return build_context.comandos
