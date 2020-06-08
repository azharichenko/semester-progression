import requests
from collections import namedtuple
from typing import List
from ics import Calendar
from datetime import datetime

ICalEvent = namedtuple("ICalEvent", ['name', 'dt', 'board'])

def fetch_ical_events(url: str) -> List[ICalEvent]:
    resp = requests.get(url)
    c = Calendar(resp.text)
    events = list(c.events)
    converted_events = []
    for event in events:
        dt = datetime.fromisoformat(str(event.begin))
        ical_event = ICalEvent(name=event.name, dt=dt)
        converted_events.append(ical_event)
    return converted_events

if __name__ == '__main__':
    url = "https://trello.com/calendar/558b268ba17523360d3d4021/5d6e84ae714b94230ad7a9ef/94ca85a3db4308c4c0cb8b6340aa557d.ics"
    from pprint import pprint

    pprint(fetch_ical_events(url))
