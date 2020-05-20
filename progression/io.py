import json
import sched
from pathlib import Path
from datetime import datetime, timedelta, date
from typing import Dict, Any

ONE_DAY = timedelta(days=1)
ONE_WEEK = timedelta(weeks=1)
REGULAR_SEMESTER = timedelta(weeks=16)

_config = None


class DateEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, date):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def get_config_path(create_if_absent: bool = False) -> Path:
    """Get semester progression config path"""
    # config_path = Path("~") / ".sp_config"
    config_path = Path(".") / ".sp_config"
    if not config_path.exists():
        if create_if_absent:
            config_path.mkdir()
        else:
            # TODO: Correct error with more helpful message
            raise RuntimeError("Missing ~/.sp_config. Please run creation script.")
    return config_path


def to_date(d: str) -> date:
    return datetime.strptime(d, "%Y-%m-%d").date()


def values_to_date(content: Dict) -> None:
    for k in content.keys():
        if isinstance(content[k], str):
            content[k] = to_date(content[k])
        elif isinstance(content[k], list):
            for e in content[k]:
                e['start'] = to_date(e['start'])
                e['end'] = to_date(e['end'])
        elif isinstance(content[k], dict):
            content[k]['start'] = to_date(content[k]['start'])
            content[k]['end'] = to_date(content[k]['end'])


def get_configuration_file(filename="default.json", config_path=get_config_path()) -> Dict:
    global _config
    if _config is not None:
        return _config

    file = config_path / filename
    if not file.exists():
        raise ValueError(str(file) + " does not exist")

    with file.open() as f:
        configuration = json.load(f)

    values_to_date(content=configuration)
    _config = configuration
    from pprint import pprint
    pprint(configuration)
    return configuration


def write_configuration_file(content, filename="default.json", config_path=None) -> None:
    global _config
    file = config_path / filename
    with file.open("w") as f:
        json.dump(obj=content, fp=f, cls=DateEncoder, indent=4)
    _config = None
