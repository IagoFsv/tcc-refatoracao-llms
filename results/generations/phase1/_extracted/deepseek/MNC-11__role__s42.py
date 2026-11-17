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
def release(context: Context, version: str):
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
        context.run(
            '''
                poetry build --no-interaction
                poetry publish --no-interaction
            ''',
            pty=True,
        )
    except UnexpectedExit as exception:
        with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
            toml.dump(pyproject, pyproject_file)
        raise exception from exception

    # recover to original
    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        toml.dump(pyproject, pyproject_file)


def run(version, fail_publish=False):
    """Runs the release of the version; returns the recorded commands. Public entry point of this unit."""
    BuildContext.commands = []
    BuildContext.fail = fail_publish
    release(BuildContext(), version)
    return BuildContext.commands
