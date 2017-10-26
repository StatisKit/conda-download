import os

from conda_build import api as conda_build
from conda_build.metadata import MetaData

def list_packages(directory, config=None):
    """
    Get the build metadata of all recipes in a directory.
 
    :Parameters:
     - `directory` (basestring) - The directory where to start looking for metas using os.walk.
    """
    packages = []
    root = os.path.abspath(directory)

    for new_root, dirs, files in os.walk(root, followlinks=True):
        if 'meta.yaml' in files:
            package = conda_build.render(new_root, config=config)[0]
            if isinstance(package, MetaData):
                packages.append(package)
            else:
                packages.append(package[0])
                
    return packages