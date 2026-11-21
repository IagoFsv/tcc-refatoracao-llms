"""Lists the example scripts of a folder that should be run on their own.

Public entry point: run(folder, excluded=()). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import os
from typing import Set

EXCLUDED_FILENAMES: Set[str] = set()


def _get_filenames(folder):
    folder_path = os.path.abspath(folder)
    filenames = os.listdir(folder_path)
    filenames.sort()
    result = []
    for filename in filenames:
        if filename.endswith(".py") and not filename.endswith("_test.py") and filename not in EXCLUDED_FILENAMES:
            result.append(os.path.join(folder_path, filename))
    return result


def run(folder, excluded=()):
    """Returns the absolute paths of the scripts of the folder, leaving out the
    file names in excluded. Public entry point of this unit."""
    EXCLUDED_FILENAMES.clear()
    EXCLUDED_FILENAMES.update(excluded)
    return _get_filenames(folder)
