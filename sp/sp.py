#!/usr/bin/python3

import argparse
import json
import datetime
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--action', '-a', type=str, required=True, choices=["new", "edit", "remove"], help="action to perform")
args = parser.parse_args()

# Create config directory
config_path = Path("~") / '.sp_config'
if not config_path.exists():
    config_path.mkdir()

# TODO: Automatic start and end date finder? Maybe add on to pittapi with calendar
# term_code = input("What's the term code for the Pitt Semester (e.g. 2171)? ")

# Data initialization
data = {}

data['start-date'] = '01/06/2020'
data['end-date'] = '04/20/2020'

