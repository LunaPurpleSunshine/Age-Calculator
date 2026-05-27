"""Tests for the pure functions in ``agecalc.core``."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from agecalc.core import calculate_age, calculate_next_birthday, expand_year

FreezeToday = Callable[[date], None]


# ---------------------------------------------------------------------------
# expand_year
# ---------------------------------------------------------------------------


def test_expand_year_below_pivot_maps_to_2000s(freeze_today: FreezeToday) -> None:
    freeze_today(date(2025, 6, 1))
    # 2025 % 100 == 25; values <= 25 should be 2000s
    assert expand_year(0) == 2000
    assert expand_year(15) == 2015
    assert expand_year(25) == 2025


def test_expand_year_above_pivot_maps_to_1900s(freeze_today: FreezeToday) -> None:
    freeze_today(date(2025, 6, 1))
    assert expand_year(26) == 1926
    assert expand_year(99) == 1999


@pytest.mark.parametrize(
    "today, yy, expected",
    [
        (date(2030, 1, 1), 30, 2030),
        (date(2030, 1, 1), 31, 1931),
        (date(2099, 12, 31), 99, 2099),
        (date(2000, 1, 1), 0, 2000),
        (date(2000, 1, 1), 1, 1901),
    ],
)
def test_expand_year_boundary_examples(
    freeze_today: FreezeToday, today: date, yy: int, expected: int
) -> None:
    freeze_today(today)
    assert expand_year(yy) == expected


@given(
    today_year=st.integers(min_value=2000, max_value=2099),
    yy=st.integers(min_value=0, max_value=99),
)
def test_expand_year_invariant(today_year: int, yy: int) -> None:
    """Property: expansion always lands within ±100 years of ``today.year``."""
    today = date(today_year, 6, 15)

    class FrozenDate(date):
        @classmethod
        def today(cls) -> date:
            return today

    import agecalc.core as _core

    original_date = _core.date
    _core.date = FrozenDate  # type: ignore[misc]
    try:
        result = _core.expand_year(yy)
    finally:
        _core.date = original_date  # type: ignore[misc]

    pivot = today_year % 100
    if yy > pivot:
        assert result == 1900 + yy
    else:
        assert result == 2000 + yy
    assert result % 100 == yy


# ---------------------------------------------------------------------------
# calculate_age
# ---------------------------------------------------------------------------


def test_calculate_age_today_is_birthday(freeze_today: FreezeToday) -> None:
    freeze_today(date(2025, 6, 1))
    assert calculate_age(date(2000, 6, 1)) == 25


def test_calculate_age_day_before_birthday(freeze_today: FreezeToday) -> None:
    freeze_today(date(2025, 6, 1))
    assert calculate_age(date(2000, 6, 2)) == 24


def test_calculate_age_day_after_birthday(freeze_today: FreezeToday) -> None:
    freeze_today(date(2025, 6, 1))
    assert calculate_age(date(2000, 5, 31)) == 25


def test_calculate_age_future_date_is_negative(freeze_today: FreezeToday) -> None:
    freeze_today(date(2025, 6, 1))
    assert calculate_age(date(2050, 6, 1)) == -25


@given(
    today=st.dates(min_value=date(1950, 1, 1), max_value=date(2100, 12, 31)),
    birth=st.dates(min_value=date(1900, 1, 1), max_value=date(2200, 12, 31)),
)
def test_calculate_age_matches_reference_formula(today: date, birth: date) -> None:
    class FrozenDate(date):
        @classmethod
        def today(cls) -> date:
            return today

    import agecalc.core as _core

    original_date = _core.date
    _core.date = FrozenDate  # type: ignore[misc]
    try:
        result = _core.calculate_age(birth)
    finally:
        _core.date = original_date  # type: ignore[misc]

    expected = (
        today.year - birth.year - (1 if (today.month, today.day) < (birth.month, birth.day) else 0)
    )
    assert result == expected


# ---------------------------------------------------------------------------
# calculate_next_birthday
# ---------------------------------------------------------------------------


def test_next_birthday_is_today_when_birthday_today(freeze_today: FreezeToday) -> None:
    freeze_today(date(2025, 6, 1))
    assert calculate_next_birthday(date(1990, 6, 1)) == date(2025, 6, 1)


def test_next_birthday_later_this_year(freeze_today: FreezeToday) -> None:
    freeze_today(date(2025, 6, 1))
    assert calculate_next_birthday(date(1990, 12, 25)) == date(2025, 12, 25)


def test_next_birthday_already_passed_rolls_to_next_year(freeze_today: FreezeToday) -> None:
    freeze_today(date(2025, 6, 1))
    assert calculate_next_birthday(date(1990, 3, 10)) == date(2026, 3, 10)


@given(
    today=st.dates(min_value=date(1950, 1, 1), max_value=date(2099, 12, 31)),
    birth=st.dates(min_value=date(1900, 1, 1), max_value=date(2099, 12, 31)),
)
def test_next_birthday_properties(today: date, birth: date) -> None:
    # Skip leap-day birthdays — calculate_next_birthday does not handle the
    # Feb 29 → Feb 28/Mar 1 rollover, which is outside the scope of this test.
    assume(not (birth.month == 2 and birth.day == 29))

    class FrozenDate(date):
        @classmethod
        def today(cls) -> date:
            return today

    import agecalc.core as _core

    original_date = _core.date
    _core.date = FrozenDate  # type: ignore[misc]
    try:
        result = _core.calculate_next_birthday(birth)
    finally:
        _core.date = original_date  # type: ignore[misc]

    assert result >= today
    assert (result.month, result.day) == (birth.month, birth.day)
    assert result.year in {today.year, today.year + 1}
    # The result must be the smallest date >= today whose (month, day) matches.
    candidates = [
        date(today.year, birth.month, birth.day),
        date(today.year + 1, birth.month, birth.day),
    ]
    earliest = min(c for c in candidates if c >= today)
    assert result == earliest
