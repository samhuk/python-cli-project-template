"""
legend
---
prints to console all the output types of the application

Usage:
    xc legend -h | --help
    xc legend

Options:
    -h --help           display this screen
"""
from src.common.command.command import Command
from docopt import docopt
from src.common.printouts import progress_update


class Legend(Command):
    def run(self):
        docopt(__doc__)
        progress_update.success('Success')
        progress_update.warn('Warn')
        progress_update.error('Error')
        progress_update.step('Task')
        progress_update.info('Info')
        progress_update.not_done('Not done | Skipped')
