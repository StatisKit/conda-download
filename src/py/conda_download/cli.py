import argparse
import os

import conda_download

def main():
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

    parser.add_argument('--channels', nargs='*',
                        help="""Additional channel to search for packages. These are
                                URLs searched in the order they are given (including
                                file:// for local directories)""",
                        default=["default"])

    args = parser.parse_args()
    conda_download.main(directory = args.directory,
                        run = args.run,
                        build = args.build,
                        *args.channels)

if __name__ == '__main__':
    main()