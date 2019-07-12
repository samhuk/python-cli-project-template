from command import Command
from common.loggers.debug_file_logger import DebugFileLogger

class FileLoggedCommand(Command):
    """A base command that provides an instance of debugFileLogger."""


    def __init__(self):
        self.logger = DebugFileLogger(self.command)
