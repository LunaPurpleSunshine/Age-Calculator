"""Test helpers shared across the test modules.

These helpers are not part of the public API. They exist purely to give
the tests a small, readable way to freeze the system clock around
:meth:`whenever.Date.today_in_system_tz`.
"""

from __future__ import annotations

from contextlib import AbstractContextManager

from whenever import Date, Instant, patch_current_time


def freeze(today: Date) -> AbstractContextManager[object]:
    """Pin :meth:`whenever.Date.today_in_system_tz` to ``today``.

    The returned context manager wraps :func:`whenever.patch_current_time`
    with an :class:`whenever.Instant` at 12:00 UTC. That instant resolves
    to ``today`` for every system timezone between UTC-11 and UTC+11,
    which covers every CI runner the project supports.

    Parameters
    ----------
    today : whenever.Date
        The date that ``Date.today_in_system_tz()`` should return for
        the duration of the ``with`` block.

    Returns
    -------
    contextlib.AbstractContextManager[object]
        A context manager that pins the clock on entry and restores it
        on exit.
    """
    pinned = Instant.from_utc(today.year, today.month, today.day, hour=12)
    return patch_current_time(pinned, keep_ticking=False)
