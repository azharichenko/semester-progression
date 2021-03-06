import json
from pathlib import Path
from datetime import datetime, timedelta, date
from typing import List, NamedTuple, Optional

import requests
from parse import compile
from ics import Calendar

ONE_DAY = timedelta(days=1)
ONE_WEEK = timedelta(weeks=1)
REGULAR_SEMESTER = timedelta(weeks=16)

TRELLO_EVENT_FORMAT = compile("{name} [{board}]")


class TrelloICalEvent(NamedTuple):
    name: str
    dt: date
    board: str


class Period(NamedTuple):
    start: date
    end: date


class Event(NamedTuple):
    name: str
    date: date


class Semester(NamedTuple):
    type: str
    events: List[Event]
    period: Period
    midterms: Period
    finals: Period


class Config(NamedTuple):
    url: str


_config: Optional[Config] = None
_semester: Optional[Semester] = None


def to_date(d: str) -> date:
    return datetime.strptime(d, "%Y-%m-%d").date()


def fetch_ical_events(url: str) -> List[TrelloICalEvent]:
    resp = requests.get(url)
    c = Calendar(resp.text)
    events = list(c.events)
    converted_events = []
    for event in events:
        dt = datetime.fromisoformat(str(event.begin))
        content = TRELLO_EVENT_FORMAT.parse(event.name)
        ical_event = TrelloICalEvent(**content.named, dt=dt.date())
        converted_events.append(ical_event)
    return converted_events


def get_semester_file() -> Semester:
    global _semester
    if _semester is not None:
        return _semester

    period_start, period_end = None, None
    events = list()
    semester_type = None
    finals_start = None
    config = get_config_file()

    for event in fetch_ical_events(config.url):
        if event.board == "metadata":
            if event.name.startswith("S"):
                # TODO: Correct so that this can throw an exception
                _, type_, period_type = event.name.split(" ")
                semester_type = type_
                if period_type == "START":
                    period_start = event.dt
                elif period_type == "END":
                    period_end = event.dt
            elif event.name.startswith("B"):
                pass
            elif event.name.startswith("F"):
                finals_start = event.dt
        elif date.today() - event.dt <= timedelta(days=0):
            events.append(Event(name=event.name, date=event.dt))

    events = sorted(events, key=lambda x: x.date)

    _semester = Semester(
        type=semester_type,
        period=Period(start=period_start, end=period_end),
        events=events,
        midterms=Period(
            start=period_start + (ONE_WEEK * 6), end=period_start + (ONE_WEEK * 9)
        ),
        finals=Period(start=finals_start, end=finals_start + ONE_WEEK - ONE_DAY),
    )
    return _semester


def get_config_path(create_if_absent: bool = False) -> Path:
    """Get config path"""
    # config_path = Path("~") / ".sp_config"
    config_path = Path(".") / ".sp_config"
    if not config_path.is_dir():
        if create_if_absent:
            config_path.mkdir()
        else:
            # TODO: Correct error with more helpful message
            raise RuntimeError("Missing ~/.sp_config. Please run creation script.")
    return config_path


def get_config_file(filename="config.json", config_path=get_config_path()) -> Config:
    global _config
    if _config is not None:
        return _config

    file = config_path / filename
    if not file.is_file():
        raise ValueError(str(file) + " does not exist")

    with file.open() as f:
        configuration = json.load(f)

    return Config(url=configuration["url"])


if __name__ == "__main__":
    print(get_semester_file())
