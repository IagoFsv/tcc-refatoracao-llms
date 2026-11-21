import importlib
import os
import sys

def run(folder):
    """Loads the module again with folder as the working directory and returns
    the include folders found, sorted. Public entry point of this unit."""
    previous = os.getcwd()
    os.chdir(folder)
    try:
        importlib.reload(sys.modules[__name__])
        pxd_include_dirs = []
        for directory, dirs, files in os.walk(os.path.join('Cython', 'Includes')):
            if '__init__.pyx' in files or '__init__.pxd' in files or directory == os.path.join('Cython', 'Includes'):
                pxd_include_dirs.append(directory)
        return sorted(pxd_include_dirs)
    finally:
        os.chdir(previous)
