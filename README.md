# PYTHON CLI TEMPLATE PROJECT

## CONVERSION OF TEMPLATE TO PROJECT

This repository is a template for a python CLI(s) project.

This section can be removed after this stage.

To setup the template:
* Copy all repo files (minus the .git) to a new directory.
* Consult and modify app_info.json, ensuring the values are valid.
* Run ```python setup_template.py```.

# $$project_name

## Summary

$$cli_name is an command line interface.

## Prerequisites

Must have python >3 installed on the host system.

## Installation

From the root application directory: `python setup.py install` or `install` (for windows only).

`$$cli_name validate` to validate the CLI configuration.

## Usage

`$$cli_name -h`

## Development

### Running as a python module directly

To run the $$cli_name cli as a python module directly (unpackaged), one must run the src/$$cli_name/cli.py module, like so:

`python -m src.$$cli_name.cli <command> [<args>...]`

For example:
  * `python -m src.$$cli_name.cli -h`
  * `python -m src.$$cli_name.cli legend`
  * etc.

### Adding a command

To add a command to the CLI, create a new python script within src/$$name/commands called {new_command_name}.py,
then import it into the commands module the same way the other commands are. This script must contain a class
that inherits from one of the command classes within src/common/command, and implement the ```run()``` function.