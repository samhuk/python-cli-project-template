"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join, isfile
from subprocess import call
import json
from setuptools import Command, find_packages, find_namespace_packages, setup
import app_tools

from src.cli_app import __version__

MANDATORY_APP_INFO_VARS = ['license', 'name', 'stage']
DEFAULT_DESCRIPTION = ''
TEMPLATE_STAGE = 'template'

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
        errno = call(['py.test', f'--cov={name}', '--cov-report=term-missing'])
        raise SystemExit(errno)


def create_app_info_validation_result(is_success, msg=None) -> tuple:
    return (is_success, msg if is_success else 'Invalid app_info.json: ' + msg)


def get_app_info_validation_result(app_info: str) -> dict:
    # check that app_info has all the mandatory values
    for key in MANDATORY_APP_INFO_VARS:
        if key not in app_info:
            return create_app_info_validation_result(False, f'Missing mandatory variable - "{key}"')
    
    
    return create_app_info_validation_result(True)


this_dir = abspath(dirname(__file__))
app_info = app_tools.get_app_info()

# ensure app_info is valid
app_info_validation_result = get_app_info_validation_result(app_info)
if app_info_validation_result[0] == False:
    print(app_info_validation_result[1])
    exit(1)

name = app_info['name']
description = app_info['description']
author = app_info['author']
author_email = app_info['author_email']
license = app_info['license']
classifiers = app_info['classifiers']
url = app_info['url']
stage = app_info['stage']

if stage == TEMPLATE_STAGE:
    app_tools.setup_app_from_template_stage(name)

setup(
    name = name,
    version = __version__,
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
        'console_scripts': [
            f'{name}=src.{name}.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)