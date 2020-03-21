import sched
from pathlib import Path
from subprocess import Popen, PIPE

current_dir = Path(__file__).parent

s = sched.scheduler()


class InkyPHATProperties:
    WIDTH = 212
    HEIGHT = 104

    WHITE = 0
    BLACK = 1
    RED = 2
    YELLOW = 2


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

def write_configuration_file(filename, config_path=get_config_path()):
    pass