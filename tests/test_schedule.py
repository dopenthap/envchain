import pytest
from pathlib import Path
from envchain.schedule import (
    set_schedule, remove_schedule, get_schedule, list_schedules, ScheduleError
)


@pytest.fixture
def base(tmp_path):
    return tmp_path


def test_set_and_get_schedule(base):
    set_schedule("myproject", "0 9 * * 1", "Monday standup", base=base)
    s = get_schedule("myproject", base=base)
    assert s["cron"] == "0 9 * * 1"
    assert s["message"] == "Monday standup"


def test_set_schedule_no_message(base):
    set_schedule("proj", "0 8 * * *", base=base)
    s = get_schedule("proj", base=base)
    assert s["message"] == ""


def test_get_schedule_missing(base):
    with pytest.raises(ScheduleError, match="No schedule"):
        get_schedule("ghost", base=base)


def test_remove_schedule(base):
    set_schedule("proj", "0 9 * * *", base=base)
    remove_schedule("proj", base=base)
    with pytest.raises(ScheduleError):
        get_schedule("proj", base=base)


def test_remove_schedule_missing(base):
    with pytest.raises(ScheduleError, match="No schedule"):
        remove_schedule("nope", base=base)


def test_list_schedules_empty(base):
    assert list_schedules(base=base) == {}


def test_list_schedules_multiple(base):
    set_schedule("a", "0 8 * * *", base=base)
    set_schedule("b", "0 9 * * *", base=base)
    result = list_schedules(base=base)
    assert set(result.keys()) == {"a", "b"}


def test_overwrite_schedule(base):
    set_schedule("proj", "0 8 * * *", base=base)
    set_schedule("proj", "0 10 * * *", "new message", base=base)
    s = get_schedule("proj", base=base)
    assert s["cron"] == "0 10 * * *"
    assert s["message"] == "new message"


def test_creates_parent_dirs(tmp_path):
    base = tmp_path / "deep" / "nested"
    set_schedule("x", "* * * * *", base=base)
    assert get_schedule("x", base=base)["cron"] == "* * * * *"
