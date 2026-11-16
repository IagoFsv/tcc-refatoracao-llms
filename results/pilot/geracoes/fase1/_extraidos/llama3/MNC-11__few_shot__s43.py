from toml import loads, dumps
from invoke import Context, task
from invoke.exceptions import UnexpectedExit
from invoke.runners import Result

class BuildContext:
    """Build context that records commands and arguments."""
    commands = []
    fail = False

    def __init__(self, pyproject_path='pyproject.toml'):
        self.pyproject_path = pyproject_path

    def run(self, command, **kwargs):
        self.commands.append((command, kwargs))
        if self.fail:
            raise UnexpectedExit(command=command, exited=1)
        return Result(command=command, exited=0)

    def load_pyproject(self):
        with open(self.pyproject_path, 'r', encoding='utf-8') as pyproject_file:
            return loads(pyproject_file.read())

    def save_pyproject(self, pyproject):
        with open(self.pyproject_path, 'w', encoding='utf-8') as pyproject_file:
            dumps(pyproject, pyproject_file)

    def build_and_publish(self, pyproject):
        try:
            self.run('poetry build --no-interaction')
            self.run('poetry publish --no-interaction')
        except UnexpectedExit as exception:
            self.save_pyproject(pyproject)
            raise exception from exception

    def recover(self):
        self.save_pyproject(self.load_pyproject())

@task
def release(context: Context, version: str) -> None:
    """Build & Publish to PyPI."""
    pyproject = context.build_context.load_pyproject()
    pyproject['tool']['poetry']['version'] = version
    context.build_context.save_pyproject(pyproject)
    try:
        context.build_context.build_and_publish(pyproject)
    except UnexpectedExit as exception:
        context.build_context.recover()
        raise exception from exception

def executar(version, fail_publication=False):
    """Run the publication of the version; returns the recorded commands."""
    build_context = BuildContext()
    build_context.commands = []
    build_context.fail = fail_publication
    release(build_context, version)
    return build_context.commands
