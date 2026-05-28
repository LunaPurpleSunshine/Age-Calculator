"""Pure calculations for ages and birthdays.

This module exposes the three functions used by both the :mod:`agecalc`
command-line interface and any code that imports the package as a
library. All dates use :class:`whenever.Date` so the calendar arithmetic
is explicit and type-safe.

"Today" is always taken from the system timezone via
:meth:`whenever.Date.today_in_system_tz`.
"""

from __future__ import annotations

from whenever import Date


def expand_year(yy: int) -> int:
    """Expand a 2-digit year to a 4-digit year.

    A 2-digit year ``yy`` is interpreted as ``20YY`` whenever that would
    fall on or before today; otherwise it is interpreted as ``19YY``.
    The crossover point is ``Date.today_in_system_tz().year % 100``.

    Parameters
    ----------
    yy : int
        A 2-digit year in the inclusive range ``0..99``.

    Returns
    -------
    int
        The corresponding 4-digit year.

    Examples
    --------
    Assuming today falls in 2026, so the crossover is ``26``:

    >>> expand_year(22)  # doctest: +SKIP
    2022
    >>> expand_year(94)  # doctest: +SKIP
    1994
    """
    this_year_index = Date.today_in_system_tz().year % 100
    if yy > this_year_index:
        return 1900 + yy
    return 2000 + yy


def calculate_age(birth_date: Date) -> int:
    """Return the age in completed years for ``birth_date`` as of today.

    The result is negative when ``birth_date`` lies in the future.

    Parameters
    ----------
    birth_date : whenever.Date
        The date of birth.

    Returns
    -------
    int
        The age in completed years. Negative for future dates.

    Examples
    --------
    Assuming today is 2026-05-28:

    >>> from whenever import Date
    >>> calculate_age(Date(2000, 1, 1))  # doctest: +SKIP
    26
    >>> calculate_age(Date(2050, 1, 1))  # doctest: +SKIP
    -24
    """
    today = Date.today_in_system_tz()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def _birthday_in_year(year: int, birth_date: Date) -> Date:
    """Return the birthday falling in ``year`` with a leap-day fallback.

    For most birthdays this is simply ``Date(year, birth_date.month,
    birth_date.day)``. When ``birth_date`` is 29 February and ``year``
    is not a leap year, the result falls back to 28 February.

    Parameters
    ----------
    year : int
        The calendar year in which to place the birthday.
    birth_date : whenever.Date
        The original date of birth.

    Returns
    -------
    whenever.Date
        The birthday in ``year``, observing the 29 February fallback.
    """
    try:
        return Date(year, birth_date.month, birth_date.day)
    except ValueError:
        # Only 29 February in a non-leap year reaches this branch.
        return Date(year, 2, 28)


def calculate_next_birthday(birth_date: Date) -> Date:
    """Return the date of the next birthday, or today if it falls today.

    For people born on 29 February, non-leap years observe the birthday
    on 28 February.

    Parameters
    ----------
    birth_date : whenever.Date
        The date of birth.

    Returns
    -------
    whenever.Date
        The next birthday on or after today.

    Examples
    --------
    Assuming today is 2026-05-28:

    >>> from whenever import Date
    >>> calculate_next_birthday(Date(1990, 3, 10))  # doctest: +SKIP
    Date(2027-03-10)
    """
    today = Date.today_in_system_tz()
    current_year_bday = _birthday_in_year(today.year, birth_date)

    if current_year_bday < today:
        return _birthday_in_year(today.year + 1, birth_date)
    return current_year_bday
