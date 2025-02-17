#!/usr/bin/env python

# Check that the cells are executed in order
# To do so we open the notebook and inspects the cells

import argparse
import json
import sys
import re
import yaml


# CLI
parser = argparse.ArgumentParser(
    description='Check that the cells are executed in order',
)
parser.add_argument(
    '-e', '--allow-empty-cells',
    action='store_true'
)
parser.add_argument('notebook')

# Parse CLI
args = parser.parse_args()
fname = args.notebook

# Check cell order
errors = []
with open(fname, "r") as file:
    content = json.load(file)
last_execution_count = 0
for cell in content["cells"]:
    try:
        execution_count = cell["execution_count"]
    except KeyError:
        #print("Markdown cell", file=sys.stderr)
        continue
    if execution_count is None and args.allow_empty_cells:
        #print("Ignoring empty cell")
        continue
    #print(f"Expected: {last_execution_count+1}, Got: {execution_count}")
    if execution_count != last_execution_count + 1:
        msg = f"Cell {execution_count} should be {last_execution_count+1}"
        errors.append(msg)
    last_execution_count += 1

if len(errors) > 0:
    errors = "\n".join(errors)
    msg =  f"Execution order issues in {fname}:\n"
    msg += f"{errors}"
    print(msg)
    sys.exit(1)
else:
    print(f"No execution order issue in {fname}")
    sys.exit(0)
