import json
from os import path


MANDATORY_APP_INFO_VARS = ['project_name', 'cli_names', 'license']
DEFAULT_DESCRIPTION = ''

this_dir = path.abspath(path.dirname(__file__))

app_info_path = path.join(this_dir, 'app_info.json')
readme_path = path.join(this_dir, 'README.md')


def create_app_info_validation_result(is_success, msg=None) -> tuple:
    return (is_success, msg if is_success else 'Invalid app_info.json: ' + msg)


def get_app_info_validation_result(app_info: str) -> dict:
    # check that app_info has all the mandatory values
    for key in MANDATORY_APP_INFO_VARS:
        if key not in app_info:
            return create_app_info_validation_result(False, f'Missing mandatory variable - "{key}"')
    return create_app_info_validation_result(True)


def get_app_info():
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
    """Ensures app_info is valid. Will exit(1) if not. If valid, returns app_info."""
    app_info = get_app_info()
    app_info_validation_result = get_app_info_validation_result(app_info)
    if app_info_validation_result[0] == False:
        print(app_info_validation_result[1])
        exit(1)
    return app_info


def create_readme_from_template(app_name):
    _outpath = path.join(this_dir, 'README.md')
    new_readme = get_readme().replace('$$name', app_name)
    with open(_outpath, 'w') as f:
        f.write(new_readme)


def setup_app_from_template_stage(app_name):
    create_readme_from_template(app_name)
