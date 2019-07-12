"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join, isfile
from subprocess import call
import json
from setuptools import Command, find_packages, find_namespace_packages, setup
import app_tools

from src.__cli_name import __version__


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', f'--cov=src', '--cov-report=term-missing'])
        raise SystemExit(errno)


app_info = app_tools.ensure_valid_app_info()

# create variables from app_info dict
project_name = app_info['project_name']
cli_names = app_info['cli_names']
description = app_info['description']
author = app_info['author']
author_email = app_info['author_email']
license = app_info['license']
classifiers = app_info['classifiers']
url = app_info['url']

entry_points_console_scripts = list(map(lambda s: f'{s}={s}.cli:main', cli_names))

setup(
    name = project_name,
    version = __version__, # Uses version of first CLI app. Could change later.
    description = description,
    long_description = app_tools.get_readme(),
    url = url,
    author = author,
    author_email = author_email,
    license = license,
    classifiers = classifiers,
    keywords = 'cli',
    package_dir={'': 'src'},
    packages = find_packages('src', exclude=['docs', 'tests*']),
    install_requires = ['docopt'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': entry_points_console_scripts,
    },
    cmdclass = {'test': RunTests},
)