import argparse
import os

from conda import cli as conda_cli
# from conda.cli.conda_argparse import add_parser_channels

from .download import main as main_download
from .release import main as main_release
from .tools import add_parser_channels

def download():
    parser = argparse.ArgumentParser(description='Download conda recipe dependencies')

    parser.add_argument('directory',
                        help='The directory containing conda recipes to build.')

    parser.add_argument('--run',
                        dest='run',
                        action='store_true',
                        help="")
    parser.add_argument('--no-run',
                        dest='run',
                        action='store_false')
    parser.set_defaults(run=True)

    parser.add_argument('--build',
                        dest='build',
                        action='store_true')
    parser.add_argument('--no-build',
                        dest='build',
                        action='store_false')
    parser.set_defaults(build=True)

    parser.add_argument('--test',
                        dest='test',
                        action='store_true')
    parser.add_argument('--no-test',
                        dest='test',
                        action='store_false')
    parser.set_defaults(test=True)

    add_parser_channels(parser)

    args = parser.parse_args()
    main_download(directory = args.directory,
                  run = args.run,
                  build = args.build,
                  test = args.test,
                  channel_urls = args.channel)

def release():
    parser = argparse.ArgumentParser(description='Create a release from conda recipes')

    parser.add_argument('directory',
                        help='The directory containing conda recipes to build.')

    parser.add_argument('--inspect-conda-bld-directory',
                        dest='inspect_conda_bld_directory',
                        action='store_true',
                        help="")
    parser.add_argument('--no-inspect-conda-bld-directory',
                        dest='inspect_conda_bld_directory',
                        action='store_false',
                        help="")
    parser.set_defaults(inspect_conda_bld_directory=True)

    add_parser_channels(parser)

    args = parser.parse_args()
    main_release(directory = args.directory,
                 channel_urls = args.channel,
                 inspect_conda_bld_directory = inspect_conda_bld_directory)