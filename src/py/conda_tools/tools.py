import os

from conda_build import api as conda_build

def list_packages(directory):
    """
    Get the build metadata of all recipes in a directory.
 
    :Parameters:
     - `directory` (basestring) - The directory where to start looking for metas using os.walk.
    """
    packages = []
    root = os.path.abspath(directory)
    for new_root, dirs, files in os.walk(root, followlinks=True):
        if 'meta.yaml' in files:
            packages.append(conda_build.render(new_root, config=None)[0])
    return packages