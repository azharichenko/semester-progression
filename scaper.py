import feedparser
import re
from pprint import pprint

ACADEMIC_CALENDAR_URL = "https://25livepub.collegenet.com/calendars/pitt-academic-calendar.xml"


d = feedparser.parse(ACADEMIC_CALENDAR_URL)

FINALS_START = "FINAL EXAMINATION PERIOD FOR UNDERGRADS" # "FINAL EXAMS UNDERGRAD"
SPRING_START = "SPRING TERM CLASSES BEGIN"
SPRING_END = "SPRING ENDS"

FALL_START = "FALL TERM CLASSES BEGIN"
FALL_END = "FALL TERM ENDS"

for entry in d.entries:
    timestamp = entry.published_parsed
    print(entry.title.upper())