"""Pure functions for age and birthday calculations."""

from __future__ import annotations

from datetime import date


def expand_year(yy: int) -> int:
    """Expand a 2-digit year to 4 digits.

    Years that would land in the future when interpreted as 20YY are treated
    as 19YY instead; everything else is treated as 20YY.
    """
    this_year_index = date.today().year % 100
    if yy > this_year_index:
        return 1900 + yy
    return 2000 + yy


def calculate_age(birth_date: date) -> int:
    """Return the age in whole years for ``birth_date`` as of today.

    Negative values mean the date is in the future.
    """
    today = date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def _birthday_in_year(year: int, birth_date: date) -> date:
    """Return the birthday in ``year``, mapping Feb 29 to Feb 28 in non-leap years."""
    try:
        return date(year, birth_date.month, birth_date.day)
    except ValueError:
        # Only Feb 29 in a non-leap year can hit this with a valid birth_date.
        return date(year, 2, 28)


def calculate_next_birthday(birth_date: date) -> date:
    """Return the date of the next birthday, or today if it falls today.

    For Feb 29 birthdays, non-leap years use Feb 28.
    """
    today = date.today()
    current_year_bday = _birthday_in_year(today.year, birth_date)

    if current_year_bday < today:
        return _birthday_in_year(today.year + 1, birth_date)
    return current_year_bday
