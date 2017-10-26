import argparse
import os

from . import download

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

    parser.add_argument('-c', '--channel', nargs='*',
                        help="""Additional channels to search for packages. These are
                                URLs searched in the order they are given (including
                                file:// for local directories)""",
                        default=[])

    args = parser.parse_args()
    download(directory = args.directory,
             run = args.run,
             build = args.build,
             test = args.test,
             channel_urls = args.channels)