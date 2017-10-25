import conda_build
import os

def fetch_metadata(directory, max_depth=0, config=None):
    """
    Get the build metadata of all recipes in a directory.
    The order of metas from this function is not guaranteed.
    Parameters
    ----------
    directory
        Where to start looking for metas using os.walk.
    max_depth : int
        How deep to recurse when looking for recipes.
        A value ``<=0`` will recurse indefinitely. A value of 1
        will look in the given directory for a meta.yaml.
        (default: 0)
    """
    metadata = []
    current_depth = max_depth
    root = os.path.normpath(directory)
    for new_root, dirs, files in os.walk(root, followlinks=True):
        depth = new_root[len(root):].count(os.path.sep) + 1
        if max_depth > 0 and depth >= max_depth:
            del dirs[:]
        if 'meta.yaml' in files:
            metadata.append(conda_build.api.render(new_root, config=config)[0])

    return metadata

def download(directory, run, build, *channels, **kwargs):
    """
    """
    metadata = fetch_metadata(directory, **kwargs)
    print(metadata)    