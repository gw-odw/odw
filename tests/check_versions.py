#!/usr/bin/env python
"""
This script is a bascic linter that checks that
a notebook don't install anything different from environment.yml
The messages are displayed at the end.

The error code is a combination of the 4 errors:
  - a notebook installs a module that is not in environment.yml
  - a notebook installs a different version than environment.yml

TODO:
  - add CLI (for file names, mode of operation, etc.)?
  - should we split that in 2 separate scripts
    (one for requirements.txt)?
  - extend (or create a new script) to compare environment.yml
    to production environment
"""
import sys
import argparse
import re
import json
import yaml


# Error codes and messages
NB_INSTALL_ERR = 1 << 0
NB_INSTALL_MSG = "Extra installation in {fname}: this notebook requires {module}=={version}, but it is not in environment.yml"

NB_MISMATCH_ERR = 1 << 1
NB_MISMATCH_MSG = "Version mismatch in {fname} for {module}: notebook requires {version}, environment.yml requires {environment_mod}"

# Let's be optimistic: there is no error (yet)
errors = []
error_code = 0

# CLI
parser = argparse.ArgumentParser(
    description='Check that pip requirements file match conda environment file',
)
parser.add_argument(
    'environment',
    help='conda environment file',
    type=argparse.FileType('r'),
)
parser.add_argument(
    'notebook',
    help='the notebook to check',
    type=argparse.FileType('r'),
)
parser.add_argument(
    '-v', '--verbose',
    help='verbose',
    action='store_true',
)
args = parser.parse_args()

# Read the conda environment file
environment_yaml = yaml.load(args.environment, Loader=yaml.loader.SafeLoader)
args.environment.close()

# Extract the dependencies and versions
environment = {}
for element in environment_yaml["dependencies"]:
    module, version = element.split("=")
    environment[module] = version

# Read the notebook
content = json.load(args.notebook)
fname = args.notebook.name
args.notebook.close()

if args.verbose:
    print("Checking content of notebooks")
for cell in content["cells"]:
    code = "\n".join(cell["source"])
    if "pip install " in code:
        if args.verbose:
            print(f"Checking cell {cell['execution_count']}")
        pip_installs = re.findall("([a-z]+==[0-9.]+)", code, flags=re.IGNORECASE)
        if args.verbose:
            print(f"Cell {cell['execution_count']} installs {pip_installs}")
        for element in pip_installs:
            module, version = element.split("==")
            if args.verbose:
                print(f"\tChecking {module}")
            module = module.lower()
            if module in environment:
                if args.verbose:
                    print(f"\t\tModule found")
                if environment[module] != version:
                    if args.verbose:
                        print(f"\t\tVersion mismatch")
                    # Add message and position error code
                    msg = NB_MISMATCH_MSG.format(
                        fname=fname,
                        module=module,
                        version=version,
                        environment_mod=environment[module],
                    )
                    errors.append(msg)
                    error_code |= NB_MISMATCH_ERR
                else:
                    if args.verbose:
                        print(f"\t\tVersion match ({version})")
            else:
                if args.verbose:
                    print(f"\t\tModule not found in conda environment")
                # Add message and position error code
                msg = NB_INSTALL_MSG.format(
                    fname=fname,
                    module=module,
                    version=version,
                )
                errors.append(msg)
                error_code |= NB_INSTALL_ERR

if errors:
    print("Error(s) found:", file=sys.stderr)
    print("\n".join(errors), file=sys.stderr)
    sys.exit(error_code)
