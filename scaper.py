import feedparser
import re
from pprint import pprint

ACADEMIC_CALENDAR_URL = "https://25livepub.collegenet.com/calendars/pitt-academic-calendar.xml"


d = feedparser.parse(ACADEMIC_CALENDAR_URL)

FINALS_START = re.compile("FINAL EXAM(\s|S\s|INATION\s)[\w\s]+?UNDERGRAD(\s|S\s)")
SPRING_START = "SPRING TERM CLASSES BEGIN"
SPRING_END = "SPRING ENDS"

FALL_START = "FALL TERM CLASSES BEGIN"
FALL_END = "FALL TERM ENDS"

for entry in d.entries:
    timestamp = entry.published_parsed
    print(entry.title.upper(), re.match(FINALS_START, entry.title.upper()))