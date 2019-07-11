# PYTHON CLI TEMPLATE PROJECT

## CONVERSION OF TEMPLATE TO PROJECT

This repository is a template for a python CLI(s) project.

If the property "stage" within app_info.json equals "template", the app is in **template** stage.

This section can be removed after this stage.

First, one must run ```python setup.py install```. If the project is in template stage, all instances of $$name
in this file are replaced by the "name" property value.

## Summary

$$name is an command line interface.

## Prerequisites

Must have python >3 installed on the host system.

## Installation

From the root application directory: `python setup.py install` or `install` (for windows only).

`$$name validate` to validate the CLI configuration.

## Usage

`$$name -h`

## Development

To run the $$name cli as a python module directly (unpackaged), one must run the src/$$name/cli.py module, like so:

`python -m src.$$name.cli <command> [<args>...]`

For example:
  * `python -m src.$$name.cli -h`
  * `python -m src.$$name.cli legend`
  * etc.