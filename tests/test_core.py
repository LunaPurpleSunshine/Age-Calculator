"""Tests for the pure functions in ``agecalc.core``."""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st
from whenever import Date

from agecalc.core import calculate_age, calculate_next_birthday, expand_year
from tests._helpers import freeze


def _is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _birthday_in_year_for_test(year: int, birth: Date) -> Date:
    """Mirror of ``core._birthday_in_year`` for use in property assertions."""
    if birth.month == 2 and birth.day == 29 and not _is_leap(year):
        return Date(year, 2, 28)
    return Date(year, birth.month, birth.day)


# ---------------------------------------------------------------------------
# expand_year
# ---------------------------------------------------------------------------


def test_expand_year_below_pivot_maps_to_2000s() -> None:
    with freeze(Date(2025, 6, 1)):
        # 2025 % 100 == 25; values <= 25 should be 2000s
        assert expand_year(0) == 2000
        assert expand_year(15) == 2015
        assert expand_year(25) == 2025


def test_expand_year_above_pivot_maps_to_1900s() -> None:
    with freeze(Date(2025, 6, 1)):
        assert expand_year(26) == 1926
        assert expand_year(99) == 1999


@pytest.mark.parametrize(
    "today, yy, expected",
    [
        (Date(2030, 1, 1), 30, 2030),
        (Date(2030, 1, 1), 31, 1931),
        (Date(2099, 12, 31), 99, 2099),
        (Date(2000, 1, 1), 0, 2000),
        (Date(2000, 1, 1), 1, 1901),
    ],
)
def test_expand_year_boundary_examples(today: Date, yy: int, expected: int) -> None:
    with freeze(today):
        assert expand_year(yy) == expected


@given(
    today_year=st.integers(min_value=2000, max_value=2099),
    yy=st.integers(min_value=0, max_value=99),
)
def test_expand_year_invariant(today_year: int, yy: int) -> None:
    """Property: expansion always lands within ±100 years of ``today.year``."""
    with freeze(Date(today_year, 6, 15)):
        result = expand_year(yy)

    pivot = today_year % 100
    if yy > pivot:
        assert result == 1900 + yy
    else:
        assert result == 2000 + yy
    assert result % 100 == yy


# ---------------------------------------------------------------------------
# calculate_age
# ---------------------------------------------------------------------------


def test_calculate_age_today_is_birthday() -> None:
    with freeze(Date(2025, 6, 1)):
        assert calculate_age(Date(2000, 6, 1)) == 25


def test_calculate_age_day_before_birthday() -> None:
    with freeze(Date(2025, 6, 1)):
        assert calculate_age(Date(2000, 6, 2)) == 24


def test_calculate_age_day_after_birthday() -> None:
    with freeze(Date(2025, 6, 1)):
        assert calculate_age(Date(2000, 5, 31)) == 25


def test_calculate_age_future_date_is_negative() -> None:
    with freeze(Date(2025, 6, 1)):
        assert calculate_age(Date(2050, 6, 1)) == -25


_DATE_STRATEGY = st.dates(
    min_value=Date(1970, 1, 2).to_stdlib(),
    max_value=Date(2099, 12, 31).to_stdlib(),
).map(lambda d: Date(d.year, d.month, d.day))


@given(today=_DATE_STRATEGY, birth=_DATE_STRATEGY)
def test_calculate_age_matches_reference_formula(today: Date, birth: Date) -> None:
    with freeze(today):
        result = calculate_age(birth)

    expected = (
        today.year - birth.year - (1 if (today.month, today.day) < (birth.month, birth.day) else 0)
    )
    assert result == expected


# ---------------------------------------------------------------------------
# calculate_next_birthday
# ---------------------------------------------------------------------------


def test_next_birthday_is_today_when_birthday_today() -> None:
    with freeze(Date(2025, 6, 1)):
        assert calculate_next_birthday(Date(1990, 6, 1)) == Date(2025, 6, 1)


def test_next_birthday_later_this_year() -> None:
    with freeze(Date(2025, 6, 1)):
        assert calculate_next_birthday(Date(1990, 12, 25)) == Date(2025, 12, 25)


def test_next_birthday_already_passed_rolls_to_next_year() -> None:
    with freeze(Date(2025, 6, 1)):
        assert calculate_next_birthday(Date(1990, 3, 10)) == Date(2026, 3, 10)


def test_next_birthday_feb_29_in_leap_year() -> None:
    # 2024 is a leap year and Feb 29 is still ahead.
    with freeze(Date(2024, 1, 15)):
        assert calculate_next_birthday(Date(2000, 2, 29)) == Date(2024, 2, 29)


def test_next_birthday_feb_29_in_non_leap_year_falls_to_feb_28() -> None:
    with freeze(Date(2025, 1, 15)):
        assert calculate_next_birthday(Date(2000, 2, 29)) == Date(2025, 2, 28)


def test_next_birthday_feb_29_after_feb_in_non_leap_year_rolls_to_next_year() -> None:
    # March 1 2025 (non-leap): we already passed Feb 28, so next birthday is Feb 28 2026.
    with freeze(Date(2025, 3, 1)):
        assert calculate_next_birthday(Date(2000, 2, 29)) == Date(2026, 2, 28)


@given(today=_DATE_STRATEGY, birth=_DATE_STRATEGY)
def test_next_birthday_properties(today: Date, birth: Date) -> None:
    with freeze(today):
        result = calculate_next_birthday(birth)

    assert result >= today
    assert result.year in {today.year, today.year + 1}
    is_leap_day = birth.month == 2 and birth.day == 29
    if is_leap_day and not _is_leap(result.year):
        assert (result.month, result.day) == (2, 28)
    else:
        assert (result.month, result.day) == (birth.month, birth.day)
    # The result must be the earliest birthday-in-year that is >= today.
    candidates = [
        _birthday_in_year_for_test(today.year, birth),
        _birthday_in_year_for_test(today.year + 1, birth),
    ]
    earliest = min(c for c in candidates if c >= today)
    assert result == earliest
