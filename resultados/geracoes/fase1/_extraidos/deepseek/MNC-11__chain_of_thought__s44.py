import toml
from invoke import Context, task
from invoke.exceptions import UnexpectedExit
from invoke.runners import Result


class PyProject:
    def __init__(self, path: str):
        self.path = path

    def load(self):
        with open(self.path, 'r', encoding='utf-8') as pyproject_file:
            pyproject_string = pyproject_file.read()
        return toml.loads(pyproject_string)

    def save(self, pyproject: dict):
        with open(self.path, 'w', encoding='utf-8') as pyproject_file:
            toml.dump(pyproject, pyproject_file)


class ContextoDeBuild(Context):
    comandos = []
    falhar = False

    def __init__(self, pyproject: PyProject):
        self.pyproject = pyproject

    def run(self, command, **kwargs):
        ContextoDeBuild.comandos.append((command, kwargs, self.pyproject.load()['tool']['poetry']['version']))
        if ContextoDeBuild.falhar:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)


@task
def release(context: ContextoDeBuild, version: str) -> None:
    pyproject = context.pyproject
    pyproject_data = pyproject.load()
    pyproject_data['tool']['poetry']['version'] = version
    pyproject.save(pyproject_data)

    try:
        context.run(
            '''
                poetry build  --no-interaction
                poetry publish --no-interaction
            ''',
            pty=True,
        )
    except UnexpectedExit as exception:
        pyproject.save(pyproject.load())
        raise exception from exception

    pyproject.save(pyproject.load())


def executar(version, falhar_publicacao=False):
    ContextoDeBuild.comandos = []
    ContextoDeBuild.falhar = falhar_publicacao
    pyproject = PyProject('pyproject.toml')
    release(ContextoDeBuild(pyproject), version)
    return ContextoDeBuild.comandos
