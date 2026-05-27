"""End-to-end-ish tests for the ``agecalc`` CLI."""

from __future__ import annotations

from click.testing import CliRunner
from whenever import Date

from agecalc.cli import main
from tests._helpers import freeze


def test_four_digit_year_only() -> None:
    with freeze(Date(2025, 6, 1)):
        result = CliRunner().invoke(main, ["1990"])
    assert result.exit_code == 0
    assert "35 years old today 2025-06-01" in result.stdout
    assert "Will turn 36 on next birthday 2026-01-01" in result.stdout


def test_two_digit_year_expansion() -> None:
    with freeze(Date(2025, 6, 1)):
        # 22 <= 25, so 22 -> 2022
        result = CliRunner().invoke(main, ["22", "07", "15"])
    assert result.exit_code == 0
    assert "2 years old today 2025-06-01" in result.stdout
    assert "Will turn 3 on next birthday 2025-07-15" in result.stdout


def test_two_digit_year_falls_back_to_1900s() -> None:
    with freeze(Date(2025, 6, 1)):
        # 94 > 25, so 94 -> 1994
        result = CliRunner().invoke(main, ["94", "07", "01"])
    assert result.exit_code == 0
    assert "30 years old today 2025-06-01" in result.stdout
    assert "Will turn 31 on next birthday 2025-07-01" in result.stdout


def test_birthday_today_prints_turned_message() -> None:
    with freeze(Date(2025, 6, 1)):
        result = CliRunner().invoke(main, ["1990", "06", "01"])
    assert result.exit_code == 0
    assert "35 years old today 2025-06-01" in result.stdout
    assert "Turned 35 today!" in result.stdout


def test_future_date_reports_years_in_future() -> None:
    with freeze(Date(2025, 6, 1)):
        result = CliRunner().invoke(main, ["2050", "01", "01"])
    assert result.exit_code == 0
    assert "25 years in the future" in result.stdout


def test_invalid_year_length_exits() -> None:
    with freeze(Date(2025, 6, 1)):
        result = CliRunner().invoke(main, ["123"])
    assert result.exit_code == 2
    assert "year must be 2 or 4 digits" in result.stderr


def test_invalid_calendar_date_exits() -> None:
    with freeze(Date(2025, 6, 1)):
        result = CliRunner().invoke(main, ["2024", "02", "30"])
    assert result.exit_code == 2
    assert "invalid date" in result.stderr


def test_non_numeric_month_exits() -> None:
    with freeze(Date(2025, 6, 1)):
        result = CliRunner().invoke(main, ["2000", "xx"])
    assert result.exit_code == 2


def test_help_flag_exits_cleanly() -> None:
    result = CliRunner().invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    assert "YEAR" in result.stdout
