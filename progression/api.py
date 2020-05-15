import json
import sched
from pathlib import Path
from datetime import datetime, timedelta

current_dir = Path(__file__).parent

s = sched.scheduler()

ONE_DAY = timedelta(days=1)
ONE_WEEK = timedelta(weeks=1)
REGULAR_SEMESTER = timedelta(weeks=16)


def get_config_path(create_if_absent: bool = False) -> Path:
    """Get semester progression config path"""
    config_path = Path("~") / ".sp_config"
    if not config_path.exists():
        if create_if_absent:
            config_path.mkdir()
        else:
            # TODO: Correct error with more helpful message
            raise RuntimeError("Missing ~/.sp_config. Please run creation script.")
    return config_path


def to_datetime(d: str):
    return datetime.strptime(d, "%m/%d/%Y").date()


def get_configuration_file(filename="default.json", config_path=None):
    # file = config_path / filename
    # if not file.exists():
    #     raise ValueError(str(file) + " does not exist")
    #
    # f = file.open()
    # configuration = json.load(f)
    # f.close()

    configuration = {}
    semester_start = to_datetime("01/05/2020")
    semester_end = semester_start + REGULAR_SEMESTER - ONE_DAY
    configuration["start"] = semester_start
    configuration["end"] = semester_end
    configuration["breaks"] = [
        {
            "start": semester_start + (ONE_WEEK * 9),
            "end": semester_start + (ONE_WEEK * 10),
        },
        {
            "start": semester_start + (ONE_WEEK * 10),
            "end": semester_start + (ONE_WEEK * 11),
        },
    ]
    configuration["midterm"] = {
        "start": semester_start + (ONE_WEEK * 6),
        "end": semester_start + (ONE_WEEK * 9),
    }
    configuration["finals"] = {
        "start": semester_end - ONE_WEEK + ONE_DAY,
        "end": semester_end - ONE_DAY,
    }
    configuration["outdated"] = semester_end + ONE_WEEK
    return configuration


def write_configuration_file(filename="default.json", config_path=None):
    pass


from .draw import draw_to_display, draw_display_message


def main_service_loop() -> None:
    """Main service loop to rerun service while raspberry pi is alive"""
    # TODO: Add before semester countdown and after semester please update
    draw_to_display()
    s.enter(60 * 60 * 12, 1, main_service_loop)


def start_service_loop() -> None:
    s.enter(0, 1, main_service_loop)
    s.run()
