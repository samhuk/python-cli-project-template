"""The base command."""

from json import load
from common.env.env import env

class Command(object):
    """A base command."""


    def __init__(self, options):
        self.env = env
        self.command = options['<command>']


    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')


    @staticmethod
    def is_bit_string(v: str) -> bool:
        return v is not None and v in ['0', '1']


    @staticmethod
    def get_arg_value(options: list, key: str, default=None) -> str:
        return options[key] if options[key] is not None else default
