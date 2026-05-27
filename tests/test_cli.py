"""End-to-end-ish tests for the ``agecalc`` CLI."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date

import pytest

from agecalc.cli import main

FreezeToday = Callable[[date], None]


def test_four_digit_year_only(
    capsys: pytest.CaptureFixture[str], freeze_today: FreezeToday
) -> None:
    freeze_today(date(2025, 6, 1))
    exit_code = main(["1990"])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "35 years old today 2025-06-01" in out
    assert "Will turn 36 on next birthday 2026-01-01" in out


def test_two_digit_year_expansion(
    capsys: pytest.CaptureFixture[str], freeze_today: FreezeToday
) -> None:
    freeze_today(date(2025, 6, 1))
    # 22 > 25 is False, so 22 -> 2022
    exit_code = main(["22", "07", "15"])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "2 years old today 2025-06-01" in out
    assert "Will turn 3 on next birthday 2025-07-15" in out


def test_two_digit_year_falls_back_to_1900s(
    capsys: pytest.CaptureFixture[str], freeze_today: FreezeToday
) -> None:
    freeze_today(date(2025, 6, 1))
    # 94 > 25, so 94 -> 1994
    exit_code = main(["94", "07", "01"])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "30 years old today 2025-06-01" in out
    assert "Will turn 31 on next birthday 2025-07-01" in out


def test_birthday_today_prints_turned_message(
    capsys: pytest.CaptureFixture[str], freeze_today: FreezeToday
) -> None:
    freeze_today(date(2025, 6, 1))
    exit_code = main(["1990", "06", "01"])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "35 years old today 2025-06-01" in out
    assert "Turned 35 today!" in out


def test_future_date_reports_years_in_future(
    capsys: pytest.CaptureFixture[str], freeze_today: FreezeToday
) -> None:
    freeze_today(date(2025, 6, 1))
    exit_code = main(["2050", "01", "01"])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "25 years in the future" in out


def test_invalid_year_length_exits(
    capsys: pytest.CaptureFixture[str], freeze_today: FreezeToday
) -> None:
    freeze_today(date(2025, 6, 1))
    with pytest.raises(SystemExit) as excinfo:
        main(["123"])
    assert excinfo.value.code == 2
    err = capsys.readouterr().err
    assert "year must be 2 or 4 digits" in err


def test_invalid_calendar_date_exits(
    capsys: pytest.CaptureFixture[str], freeze_today: FreezeToday
) -> None:
    freeze_today(date(2025, 6, 1))
    with pytest.raises(SystemExit) as excinfo:
        main(["2024", "02", "30"])
    assert excinfo.value.code == 2
    err = capsys.readouterr().err
    assert "invalid date" in err


def test_non_numeric_month_exits(
    capsys: pytest.CaptureFixture[str], freeze_today: FreezeToday
) -> None:
    freeze_today(date(2025, 6, 1))
    with pytest.raises(SystemExit) as excinfo:
        main(["2000", "xx"])
    assert excinfo.value.code == 2


def test_help_flag_exits_cleanly(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["--help"])
    assert excinfo.value.code == 0
    out = capsys.readouterr().out
    assert "agecalc" in out
    assert "year" in out
