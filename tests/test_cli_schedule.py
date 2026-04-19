import pytest
from click.testing import CliRunner
from unittest.mock import patch
from envchain.cli_schedule import schedule_cmd
from envchain.schedule import ScheduleError


@pytest.fixture
def runner():
    return CliRunner()


def test_set_schedule(runner):
    with patch("envchain.cli_schedule.set_schedule") as mock:
        result = runner.invoke(schedule_cmd, ["set", "proj", "0 9 * * 1"])
        assert result.exit_code == 0
        mock.assert_called_once_with("proj", "0 9 * * 1", "")
        assert "Schedule set" in result.output


def test_set_schedule_with_message(runner):
    with patch("envchain.cli_schedule.set_schedule") as mock:
        result = runner.invoke(schedule_cmd, ["set", "proj", "0 9 * * 1", "-m", "standup"])
        assert result.exit_code == 0
        mock.assert_called_once_with("proj", "0 9 * * 1", "standup")
        assert "standup" in result.output


def test_remove_schedule(runner):
    with patch("envchain.cli_schedule.remove_schedule"):
        result = runner.invoke(schedule_cmd, ["remove", "proj"])
        assert result.exit_code == 0
        assert "removed" in result.output


def test_remove_schedule_missing(runner):
    with patch("envchain.cli_schedule.remove_schedule", side_effect=ScheduleError("No schedule for chain 'x'")):
        result = runner.invoke(schedule_cmd, ["remove", "x"])
        assert result.exit_code != 0
        assert "No schedule" in result.output


def test_show_schedule(runner):
    with patch("envchain.cli_schedule.get_schedule", return_value={"cron": "0 8 * * *", "message": "daily"}):
        result = runner.invoke(schedule_cmd, ["show", "proj"])
        assert result.exit_code == 0
        assert "0 8 * * *" in result.output
        assert "daily" in result.output


def test_show_schedule_missing(runner):
    with patch("envchain.cli_schedule.get_schedule", side_effect=ScheduleError("No schedule for chain 'x'")):
        result = runner.invoke(schedule_cmd, ["show", "x"])
        assert result.exit_code != 0


def test_list_schedules_empty(runner):
    with patch("envchain.cli_schedule.list_schedules", return_value={}):
        result = runner.invoke(schedule_cmd, ["list"])
        assert "No schedules" in result.output


def test_list_schedules(runner):
    data = {"a": {"cron": "0 8 * * *", "message": ""}, "b": {"cron": "0 9 * * *", "message": "hi"}}
    with patch("envchain.cli_schedule.list_schedules", return_value=data):
        result = runner.invoke(schedule_cmd, ["list"])
        assert "a" in result.output
        assert "b" in result.output
        assert "hi" in result.output
