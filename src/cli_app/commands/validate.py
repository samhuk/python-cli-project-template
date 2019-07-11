"""
validate
---
Validates the app and host system configuration.

Usage:
    xc validate -h | --help
    xc validate

Options:
    -h --help           display this screen
"""
from src.common.command.command import Command
from docopt import docopt
from os import path, devnull
from src.common.printouts.progress_update import success, success_only_green_tick, error, step, info
import subprocess
import pyodbc

# -- Utils

def create_job_result(is_success, message=None):
    return {'is_success': is_success, 'message': message}


def print_job_result(job_name, job_result):
    is_success = job_result['is_success']
    message = job_result['message']
    if is_success == True:
        text = job_name + (' - ' + message if message else '   ')
        success_only_green_tick(text, carriage_return=True)
    else:
        error(f'{job_name}: FALSE!', carriage_return=True)
        info(message)


def print_jobs_summary(n_jobs, n_success):
    line = f'{n_success}/{n_jobs} successful'
    if (n_success == n_jobs):
        success(line)
    else:
        error(line)


def run_path_check_job(_path, is_file=False):
    is_success = path.isfile(_path) if is_file else path.exists(_path)
    message = _path if is_success else f'Path/file not found: {_path}'
    return create_job_result(True, message)

# -- config validation

def example_test_job(env):
    return create_job_result(True, message="this test always passes")


class Validate(Command):
    def run(self):
        docopt(__doc__)

        jobs = [{'func': example_test_job, 'name': 'example_test_job passes'}]
        
        n_success = 0
        n_jobs = len(jobs)
        

        for job in jobs:
            job_name = job['name']  # get job name
            step(job_name + '...', new_line=False)  # print job name loading line
            job_result = job['func'](self.env)  # run job
            print_job_result(job_name, job_result)  # print job result
            if job_result['is_success']: n_success += 1 # iterate n_success

        print_jobs_summary(n_jobs, n_success)