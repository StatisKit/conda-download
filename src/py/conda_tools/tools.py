import os

from conda_build import api as conda_build
from conda_build.metadata import MetaData

def list_packages(directory, channel_urls=[], config=None):
    """
    Get the build metadata of all recipes in a directory.
 
    :Parameters:
     - `directory` (basestring) - The directory where to start looking for metas using os.walk.
    """
    packages = []
    root = os.path.abspath(directory)

    for new_root, dirs, files in os.walk(root, followlinks=True):
        if 'meta.yaml' in files:
            for package in conda_build.render(new_root, config=config):
                if isinstance(package, MetaData):
                    packages.append(package)
                else:
                    packages.append(package[0])
                if packages[-1].meta.get('build', {}).get('skip', False):
                    packages.pop()

    return packages

def add_parser_channels(p):
    p.add_argument(
        '-c', '--channel',
        dest='channel',  # apparently conda-build uses this; someday rename to channels are remove context.channels alias to channel  # NOQA
        # TODO: if you ever change 'channel' to 'channels', make sure you modify the context.channels property accordingly # NOQA
        action="append",
        help="""Additional channel to search for packages. These are URLs searched in the order
        they are given (including file:// for local directories).  Then, the defaults
        or channels from .condarc are searched (unless --override-channels is given).  You can use
        'defaults' to get the default packages for conda, and 'system' to get the system
        packages, which also takes .condarc into account.  You can also use any name and the
        .condarc channel_alias value will be prepended.  The default channel_alias
        is http://conda.anaconda.org/.""",
    )
    p.add_argument(
        "--override-channels",
        action="store_true",
        help="""Do not search default or .condarc channels.  Requires --channel.""",
    )
