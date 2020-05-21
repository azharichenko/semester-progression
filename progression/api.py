import sched
from pathlib import Path
from datetime import datetime, timedelta

from progression.io import get_configuration_file
from progression.draw import draw_to_display  # , draw_display_message

current_dir = Path(__file__).parent

s = sched.scheduler()


def countdown_loop() -> None:
    pass


def main_loop() -> None:
    """Main service loop to rerun service while raspberry pi is alive"""
    # TODO: Add before semester countdown and after semester please update
    draw_to_display()
    s.enter(0, 1, final_loop)
    # s.enter(60 * 60 * 12, 1, main_service_loop)


def final_loop() -> None:
    pass


def update_loop() -> None:
    pass


def start_loop() -> None:
    config = get_configuration_file()
    today = datetime.today().date()
    if (today - config["start"]) < timedelta():
        s.enter(0, 1, action=countdown_loop)
    elif (today - config["end"]) < timedelta():
        s.enter(0, 1, action=main_loop)
    elif (today - config["outdated"]) < timedelta():
        s.enter(0, 1, action=final_loop)
    else:
        s.enter(0, 1, action=update_loop)
    s.run()


if __name__ == "__main__":
    start_loop()
