import re
import progression.cal as pitt_cal
from datetime import datetime
from pprint import pprint

FINALS_START = re.compile("FINAL EXAM(|S|INATION)\s[\w\s]+?UNDERGRAD(|S)\s")
SPRING_START = "SPRING TERM CLASSES BEGIN"
FALL_START = "FALL TERM CLASSES BEGIN"


def find_next_semester():
    pass


for event in pitt_cal.get_academic_calendar():
    if "All Campus Dates" in event.meta:
        if FALL_START in event.title.upper():
            print(event)
            print(datetime.strptime(event.date, "%Y-%m-%d").date())
        if SPRING_START in event.title.upper():
            print(event)
            print(datetime.strptime(event.date, "%Y-%m-%d").date())
