#!/usr/bin/python3

import sched
from pathlib import Path
from subprocess import Popen, PIPE

current_dir = Path(__file__).parent

s = sched.scheduler()

def main_loop():
    process  = Popen['python3', str(current_dir / 'draw.py'), '-o', '~/.sp_config']
    s.enter(60 * 60 * 24, 1, main_loop)

s.enter(0, 1, main_loop)
s.run()