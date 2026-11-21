import os
import sys
import importlib

def get_pxd_include_dirs():
    pxd_include_dirs = []
    for directory, dirs, files in os.walk(os.path.join('Cython', 'Includes')):
        if '__init__.pyx' in files or '__init__.pxd' in files or directory == os.path.join('Cython', 'Includes'):
            pxd_include_dirs.append(directory)
    return pxd_include_dirs

def run(folder):
    previous = os.getcwd()
    os.chdir(folder)
    try:
        importlib.reload(sys.modules[__name__])
        return sorted(get_pxd_include_dirs())
    finally:
        os.chdir(previous)
