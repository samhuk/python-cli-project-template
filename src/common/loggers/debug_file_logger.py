from os import path
from src.common.env.env import env
from datetime import datetime

def create_logger_file_stamp_line(topic):
    return f'Debug output for {topic}. Created at: {datetime.now()}' + '\n' + '-'*50 + '\n'

class DebugFileLogger():
    """
    Class that provides an opened file in append mode within the debug directory defined in
    the configuration file.
    
    Args:
        topic: The topic of what the logger is logging. This is also the filename without extension of
        debug file.
    
    Usage:
        logger = DebugFileLogger('a_process')
        with logger.file as f:
            f.write(...)
        
        # create a debug file "a_process.log" with "hello" in it
        subprocess.call('echo hello', stdout=logger.file)
    """
    log_path = None
    file = None # ref to the opened log file in append mode


    def __init__(self, topic):
        self.log_path = path.join(env['app_settings']['debug_path'], f'{topic}.log')
        with open(self.log_path, 'w') as f:
            f.write(create_logger_file_stamp_line(topic))
        self.file = open(self.log_path, 'a')


    def info(self, text):
        self.file.write(text)


    def warn(self, text):
        self.file.write(text)


    def error(self, text):
        self.file.write(text)
