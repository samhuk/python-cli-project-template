"""This script converts the project from a template to an active project.
This script can be deleted once it has been run (app_info.json SHOULD be kept however)."""


from os import path, rename
from subprocess import call
import app_tools


DIR = path.abspath(path.dirname(__file__))
SETUP_SCRIPT_PATH = path.join(DIR, 'setup.py')
README_PATH = path.join(DIR, 'README.md')
SETUP_SCRIPT_CLI_NAME_STRING = '__cli_name' # can't have a directory in python with a '$' character
README_CLI_NAME_STRING = '$$cli_name'
README_PROJECT_NAME_STRING = '$$project_name'


def replace_cli_name_occurances_in_setup_script(name):
    print(f'* replacing references to {SETUP_SCRIPT_CLI_NAME_STRING} in {SETUP_SCRIPT_PATH} with {name}')
    with open(SETUP_SCRIPT_PATH, 'r') as f:
        setup_script_text = f.read()
    new_setup_script_text = setup_script_text.replace(SETUP_SCRIPT_CLI_NAME_STRING, name)
    with open(SETUP_SCRIPT_PATH, 'w') as f:
        f.write(new_setup_script_text)


def replace_cli_and_project_name_occurances_in_readme(project_name, cli_name):
    print(f'* replacing occurances of {README_PROJECT_NAME_STRING} in {README_PATH} with {project_name}')
    print(f'* replacing occurances of {README_CLI_NAME_STRING} in {README_PATH} with {cli_name}')
    new_readme = app_tools.get_readme()\
        .replace(README_PROJECT_NAME_STRING, project_name)\
        .replace(README_CLI_NAME_STRING, cli_name)
    with open(README_PATH, 'w') as f:
        f.write(new_readme)


def remame_cli_directory(name):
    src = path.join(DIR, 'src', SETUP_SCRIPT_CLI_NAME_STRING)
    dst = path.join(DIR, 'src', name)
    print(f'* renaming {src} to {dst}')
    rename(src, dst)


app_info = app_tools.ensure_valid_app_info_pre_template_conversion()
project_name = app_info['project_name']
first_cli_name = app_info['cli_names'][0]

new_cli_dir = path.join(DIR, 'src', first_cli_name)
if path.exists(new_cli_dir):
    print(f':(  new cli directory already exists ({new_cli_dir}). Must remove this since before this script is run .')
    exit(1)

# Do replacements
replace_cli_name_occurances_in_setup_script(first_cli_name)
replace_cli_and_project_name_occurances_in_readme(project_name, first_cli_name)
remame_cli_directory(first_cli_name)

# run install script
call(['python', 'setup.py', 'install'])

print(f'Done! Try running: {first_cli_name} validate')