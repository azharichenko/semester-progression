import json
import sched
from pathlib import Path
from subprocess import Popen, PIPE
from datetime import datetime, date

current_dir = Path(__file__).parent

s = sched.scheduler()

def main_service_loop() -> None:
    """Main service loop to rerun service while raspberry pi is alive"""
    process = Popen(['python3', str(current_dir / 'draw.py'), '-o', '~/.sp_config'])
    s.enter(60 * 60 * 24, 1, main_service_loop)


def start_service_loop() -> None:
    s.enter(0, 1, main_service_loop)
    s.run()


def get_config_path(create_if_absent: bool = False) -> Path:
    """Get semester progression config path"""
    config_path = Path("~") / '.sp_config'
    if not config_path.exists():
        if create_if_absent:
            config_path.mkdir()
        else:
            # TODO: Correct error with more helpful message
            raise RuntimeError("Missing ~/.sp_config. Please run creation script.")
    return config_path


def to_datetime(d: str):
    return datetime.strptime(d, "%m/%d/%Y").date()


def get_configuration_file(filename='default.json', config_path=None):
    # file = config_path / filename
    # if not file.exists():
    #     raise ValueError(str(file) + " does not exist")
    #
    # f = file.open()
    # configuration = json.load(f)
    # f.close()

    configuration = {}

    configuration['start-date'] = '01/06/2020'
    configuration['end-date'] = '04/25/2020'


    configuration['start-date'] = to_datetime(configuration['start-date'])
    configuration['end-date'] = to_datetime(configuration['end-date'])
    return configuration


def write_configuration_file(filename='default.json', config_path=None):
    pass
