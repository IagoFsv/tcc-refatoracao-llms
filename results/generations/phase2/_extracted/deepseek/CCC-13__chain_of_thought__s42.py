"""Package build script: folders of a source tree that hold declaration files.

Public entry point: run(folder). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import importlib
import os
import sys

def get_include_dirs(directory):
    dirs, files = [], []
    for dirpath, dirnames, filenames in os.walk(directory):
        dirs.append(dirpath)
        files.append(filenames)

    return dirs, files

pxd_include_dirs = []

def run(folder):
    """Loads the module again with folder as the working directory and returns
    the include folders found, sorted. Public entry point of this unit."""
    previous = os.getcwd()
    os.chdir(folder)
    try:
        importlib.reload(sys.modules[__name__])
        dirs, files = get_include_dirs(os.path.join('Cython', 'Includes'))
        for dirpath in dirs:
            if '__init__.pyx' in files or '__init__.pxd' in files or dirpath == os.path.join('Cython', 'Includes'):
                pxd_include_dirs.append(dirpath)
        return sorted(pxd_include_dirs)
    finally:
        os.chdir(previous)
