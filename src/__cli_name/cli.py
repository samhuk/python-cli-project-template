"""
cli_app
---
A CLI app.

Usage:
    xc -h | --help
    xc -v | --version
    xc <command> [<args>...]

Options:
    -h --help                       Show this screen
    -v --version                    Show version
    <command>                       The command to run
    <args>                          list of arguments for the command

Commands:
    legend                          Lists all the verbose console output types.
    validate                        Validates config.json and the host system environment.
"""


from inspect import getmembers, isclass
from docopt import docopt
import os
import re
import sys
from src.common.printouts.progress_update import error
from . import __version__

def snake_case_to_pascal_case(s: str) -> str:
    return ''.join(c.capitalize() or '_' for c in s.split('_'))


def get_command_class_from_command_string(command: str, command_list: list):
    class_name = snake_case_to_pascal_case(command)
    return next((c[1] for c in command_list if c[0] == class_name), None)


def ensure_python_version_3():
    if sys.version_info[0] < 3:
        error(f'Using Python {sys.version}. Must use Python >3. If installed, run with python >3, otherwise install the latest at https://www.python.org/downloads/')
        exit(1)


def main(options=None):
    ensure_python_version_3()
    if not options:
        options = docopt(__doc__, version=__version__, options_first=True)

    # try to dynamically match the command_string the user entered to
    # a command class. This uses an implicit matching of the name of the class.
    from . import commands
    command_string = options['<command>']
    command_classes = getmembers(commands, isclass)
    command_class = get_command_class_from_command_string(command_string, command_classes)
    if command_class is not None:
        command_class(options).run()
    else:
        error(f'Command not found: {command_string}')


if __name__ == '__main__':
    os.environ['DEBUG'] = 'TRUE'
    # if run via python -m xc.cli, the docopt only works in this scope
    options = docopt(__doc__, version=__version__, options_first=True)
    main(options=options)
