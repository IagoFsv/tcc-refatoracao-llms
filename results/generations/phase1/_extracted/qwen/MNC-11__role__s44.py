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
        BuildContext.commands.append((command, kwargs, poetry['version']))
        if BuildContext.fail:
            raise UnexpectedExit(Result(command=command, exited=1))
        return Result(command=command, exited=0)


@task
def release(context: Context, version: str) -> None:
    '''Build & Publish to PyPI.'''

    # load pyproject
    pyproject_path = 'pyproject.toml'
    pyproject_string = read_pyproject(pyproject_path)
    pyproject = toml.loads(pyproject_string)
    # change version to today datetime
    pyproject['tool']['poetry']['version'] = version
    write_pyproject(pyproject_path, pyproject)

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
        write_pyproject(pyproject_path, toml.loads(pyproject_string))
        raise exception from exception

    # recover to original
    write_pyproject(pyproject_path, toml.loads(pyproject_string))


def read_pyproject(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def write_pyproject(path, data):
    with open(path, 'w', encoding='utf-8') as file:
        toml.dump(data, file)


def run(version, fail_publish=False):
    """Runs the release of the version; returns the recorded commands. Public entry point of this unit."""
    BuildContext.commands = []
    BuildContext.fail = fail_publish
    release(BuildContext(), version)
    return BuildContext.commands
