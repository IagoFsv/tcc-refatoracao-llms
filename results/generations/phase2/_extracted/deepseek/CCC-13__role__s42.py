"""Package build script: folders of a source tree that hold declaration files.

Public entry point: run(folder). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import importlib
import os
import sys

def get_pxd_include_dirs():
    return [
        directory for directory, dirs, files
        in os.walk(os.path.join('Cython', 'Includes'))
        if '__init__.pyx' in files or '__init__.pxd' in files
        or directory == os.path.join('Cython', 'Includes')
    ]

pxd_include_dirs = get_pxd_include_dirs()

def run(folder):
    """Loads the module again with folder as the working directory and returns
    the include folders found, sorted. Public entry point of this unit."""
    previous = os.getcwd()
    os.chdir(folder)
    try:
        importlib.reload(sys.modules[__name__])
        return sorted(pxd_include_dirs)
    finally:
        os.chdir(previous)
