#!/usr/bin/env python
"""
This script is a bascic linter that checks that the requirements
in requirements.txt match those in environment.yml

The messages are displayed at the end.
The error code is a combination of the 4 errors:
  - requirements.txt installs a module that is not in environment.yml
  - requirements.txt installs a different version than environment.yml

TODO:
  - extend (or create a new script) to compare environment.yml
    to production environment
"""
import sys
import argparse
import yaml

# Error codes and messages
REQ_INSTALL_ERR = 1 << 0
REQ_INSTALL_MSG = "Extra installation in requirements.txt: requirements.txt requires {module}=={version}, but it is not in environment.yml"

REQ_MISMATCH_ERR = 1 << 1
REQ_MISMATCH_MSG = "Version mismatch in requirements.txt for {module}: requirements.txt requires {version}, environment.yml requires {environment_mod}"

# Let's be optimistic: there is no error (yet)
errors = []
error_code = 0

# CLI
parser = argparse.ArgumentParser(
    description='Check that pip requirements file match conda environment file',
)
parser.add_argument(
    'requirements',
    help='pip requirements file',
    type=argparse.FileType('r'),
)
parser.add_argument(
    'environment',
    help='conda environment file',
    type=argparse.FileType('r'),
)
parser.add_argument(
    '-v', '--verbose',
    help='verbose',
    action='store_true',
)
args = parser.parse_args()

# Read in the requirements file
requirements = {}
for line in args.requirements:
    module, version = line.split("==")
    requirements[module] = version.rstrip("\n")
args.requirements.close()

# Read the conda environment file
environment_yaml = yaml.load(args.environment, Loader=yaml.loader.SafeLoader)
args.environment.close()

# Extract the dependencies and versions
environment = {}
for element in environment_yaml["dependencies"]:
    module, version = element.split("=")
    environment[module] = version

# Check requirements and environment match
# Note requirements.txt is a subset of the full environment.yml
if args.verbose:
    print("Comparing versions in pip requirements file and conda environment file")
for module, version in requirements.items():
    if args.verbose:
        print(f"Checking {module}")
    if module in environment:
        if args.verbose:
            print(f"\tModule found")
        if version != environment[module]:
            if args.verbose:
                print(f"\tVersion mismatch")
            # Add message and position error code
            msg = REQ_MISMATCH_MSG.format(
                module=module,
                version=version,
                environment_mod=environment[module],
            )
            errors.append(msg)
            error_code |= REQ_MISMATCH_ERR
        else:
            if args.verbose:
                print(f"\tVersion match ({version})")
    else:
        if args.verbose:
            print(f"\tModule not found in conda environment")
        # Add message and position error code
        msg = REQ_INSTALL_MSG.format(
            module=module,
            version=version,
        )
        errors.append(msg)
        error_code |= REQ_INSTALL_ERR

if errors:
    print("Error(s) found:", file=sys.stderr)
    print("\n".join(errors), file=sys.stderr)
    sys.exit(error_code)
