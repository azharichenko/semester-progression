import sched
from pathlib import Path

from pidriver.draw import draw_to_display

current_dir = Path(__file__).parent

s = sched.scheduler()

HOUR = 60 * 60


def countdown_loop() -> None:
    pass


def main_loop() -> None:
    """Main service loop to rerun service while raspberry pi is alive"""
    # TODO: Add before semester countdown and after semester please update
    draw_to_display()
    s.enter(4 * HOUR, 1, main_loop)


def final_loop() -> None:
    pass


def start() -> None:
    # semester = get_semester_file()
    # today = datetime.today().date()
    # if (today - semester.period.start) < timedelta():
    #     s.enter(0, 1, action=countdown_loop)
    # elif (today - semester.period.end) < timedelta():
    s.enter(0, 1, action=main_loop)
    # elif (today - config["outdated"]) < timedelta():
    #     s.enter(0, 1, action=final_loop)
    s.run()


if __name__ == "__main__":
    start()
