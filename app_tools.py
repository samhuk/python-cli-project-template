import json
from os import path

this_dir = path.abspath(path.dirname(__file__))

app_info_path = path.join(this_dir, 'app_info.json')
readme_path = path.join(this_dir, 'README.md')

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


def create_readme_from_template(app_name):
    _outpath = path.join(this_dir, 'README.md')
    new_readme = get_readme().replace('$$name', app_name)
    with open(_outpath, 'w') as f:
        f.write(new_readme)


def setup_app_from_template_stage(app_name):
    create_readme_from_template(app_name)