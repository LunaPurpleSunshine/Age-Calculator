"""Pure functions for age and birthday calculations."""

from __future__ import annotations

from whenever import Date


def expand_year(yy: int) -> int:
    """Expand a 2-digit year to 4 digits.

    Years that would land in the future when interpreted as 20YY are treated
    as 19YY instead; everything else is treated as 20YY.
    """
    this_year_index = Date.today_in_system_tz().year % 100
    if yy > this_year_index:
        return 1900 + yy
    return 2000 + yy


def calculate_age(birth_date: Date) -> int:
    """Return the age in whole years for ``birth_date`` as of today.

    Negative values mean the date is in the future.
    """
    today = Date.today_in_system_tz()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def _birthday_in_year(year: int, birth_date: Date) -> Date:
    """Return the birthday in ``year``, mapping Feb 29 to Feb 28 in non-leap years."""
    try:
        return Date(year, birth_date.month, birth_date.day)
    except ValueError:
        # Only Feb 29 in a non-leap year can hit this with a valid birth_date.
        return Date(year, 2, 28)


def calculate_next_birthday(birth_date: Date) -> Date:
    """Return the date of the next birthday, or today if it falls today.

    For Feb 29 birthdays, non-leap years use Feb 28.
    """
    today = Date.today_in_system_tz()
    current_year_bday = _birthday_in_year(today.year, birth_date)

    if current_year_bday < today:
        return _birthday_in_year(today.year + 1, birth_date)
    return current_year_bday
