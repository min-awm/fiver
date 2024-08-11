import argparse
from .utils import SubcommandHelpFormatter
import importlib.metadata


def cli_entry_point():
    parser = argparse.ArgumentParser(description="fiver - Fiver command line interface",  usage="fiver command [arguments...]", formatter_class=SubcommandHelpFormatter)
    parser._positionals.title = "commands"
    parser.add_argument('-v', '--version', action='store_true', help='print the version')

    subparsers = parser.add_subparsers()
    connect = subparsers.add_parser('connect', help='connect to server', usage='fiver connect')
    connect.add_argument('connect', nargs='?', type=bool, default=True, help='connect to server')

   
    args = parser.parse_args()
    if args.version:
        print(f"fiver version {importlib.metadata.version("fiver")}")
    elif getattr(args, 'connect', None):
        print(args)
    else:
        parser.print_help()
