"""Maintenance tasks of a Python project: building and publishing a release.

Public entry point: run(version, fail_publish=False). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

import toml
from invoke import Context, task
from invoke.exceptions import UnexpectedExit
from invoke.runners import Result

class BuildContext(Context):
    """Context that does not run commands for real.

    Each call to run records the command, the arguments and the version
    written to pyproject.toml at that moment. With fail on, the command ends
    with exit code 1, as a failed build or publication would.
    """

    commands = []
    fail = False

    def run(self, command, **kwargs):
        with open('pyproject.toml', encoding='utf-8') as file:
            poetry = toml.load(file)['tool']['poetry']
        self.commands.append((command, kwargs, poetry['version']))
        if self.fail:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)


@task
def release(context: Context, version: str) -> None:
    """Build & Publish to PyPI."""

    pyproject = toml.load('pyproject.toml')
    pyproject['tool']['poetry']['version'] = version
    toml.dump(pyproject, open('pyproject.toml', 'w', encoding='utf-8'))

    try:
        context.run(
            '''
                poetry build --no-interaction
                poetry publish --no-interaction
            ''',
            pty=True,
        )
    except UnexpectedExit as exception:
        toml.dump(toml.loads(open('pyproject.toml', 'r', encoding='utf-8').read()), open('pyproject.toml', 'w', encoding='utf-8'))
        raise exception from exception

    toml.dump(toml.loads(open('pyproject.toml', 'r', encoding='utf-8').read()), open('pyproject.toml', 'w', encoding='utf-8'))


def run(version, fail_publish=False):
    """Runs the release of the version; returns the recorded commands. Public entry point of this unit."""
    context = BuildContext()
    context.commands = []
    context.fail = fail_publish
    release(context, version)
    return context.commands
