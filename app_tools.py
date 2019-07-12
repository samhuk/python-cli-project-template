import json
from os import path


MANDATORY_APP_INFO_VARS = ['project_name', 'cli_names', 'license']
DEFAULT_DESCRIPTION = ''

this_dir = path.abspath(path.dirname(__file__))

app_info_path = path.join(this_dir, 'app_info.json')
readme_path = path.join(this_dir, 'README.md')


# -- internal functions

def create_app_info_validation_result(is_success, msg=None) -> tuple:
    return (is_success, msg if is_success else ':(  Invalid app_info.json: ' + msg)

def get_app_info_validation_result_pre_template_conversion(app_info: str) -> tuple:
    print('* Validating app_info.json')
    # check that app_info has all the mandatory properties
    for key in MANDATORY_APP_INFO_VARS:
        if key not in app_info or app_info[key] is None:
            return create_app_info_validation_result(False, f'Missing mandatory variable - "{key}"')
        print(F':)  app_info.{key} is defined and not null ({app_info[key]}).')
    
    # ensure app_info has valid value for cli_names property
    cli_names = app_info['cli_names']
    if cli_names is None or len(cli_names) == 0:
        return create_app_info_validation_result(False, f'cli_names property needs to be a length>0 string list. Recieved: {cli_names}')
    print(F':)  app_info.cli_names is a len>0 string list ({cli_names}).')

    # ensure unconverted cli_directory exists
    cli_dir = path.join(this_dir, 'src', '__cli_name')
    if path.exists(cli_dir) == False:
        return create_app_info_validation_result(False, f'Missing required directory -> {cli_dir}. Has setup_template.py been run?')
    print(F':)  unconverted cli directory exists ({cli_dir}).')

    return create_app_info_validation_result(True)

def get_app_info_validation_result(app_info: str) -> dict:
    print('* Validating app_info.json')
    # check that app_info has all the mandatory properties
    for key in MANDATORY_APP_INFO_VARS:
        if key not in app_info or app_info[key] is None:
            return create_app_info_validation_result(False, f'Missing mandatory variable - "{key}"')
        print(F':)  app_info.{key} is defined and not null ({app_info[key]}).')
    
    # ensure app_info has valid value for cli_names property
    cli_names = app_info['cli_names']
    if cli_names is None or len(cli_names) == 0:
        return create_app_info_validation_result(False, f'cli_names property needs to be a length>0 string list. Recieved: {cli_names}')
    print(F':)  app_info.cli_names is a len>0 string list ({cli_names}).')

    # ensure cli directory exists
    cli_dir = path.join(this_dir, 'src', get_app_info()['cli_names'][0])
    if path.exists(cli_dir) == False:
        return create_app_info_validation_result(False, f'Missing required directory -> {cli_dir}. Has setup_template.py been run?')
    print(F':)  cli directory exists ({cli_dir}).')

    return create_app_info_validation_result(True)

# --

def get_app_info() -> dict:
    _path = app_info_path
    if path.isfile(_path):
        try:
            with open(_path, encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise e
    else:
        print('Could not find app_info file: ' + _path)
        exit(1)


def get_readme() -> str:
    _path = readme_path
    if path.isfile(_path) == False:
        print("Could not find readme file: " + _path)
        exit(1)
    with open(_path, encoding='utf-8') as f:
        readme = f.read()
    return readme


def ensure_valid_app_info() -> dict:
    """Ensures app_info is valid. Will cause program to exit if not. If valid, returns app_info."""
    app_info = get_app_info()
    app_info_validation_result = get_app_info_validation_result(app_info)
    if app_info_validation_result[0] == False:
        print(app_info_validation_result[1])
        exit(1)
    return app_info


def ensure_valid_app_info_pre_template_conversion() -> dict:
    """Ensures app_info is valid. Will exit(1) if not. If valid, returns app_info.
    This function can be deleted once project has been converted from a template."""
    app_info = get_app_info()
    app_info_validation_result = get_app_info_validation_result_pre_template_conversion(app_info)
    if app_info_validation_result[0] == False:
        print(app_info_validation_result[1])
        exit(1)
    return app_info