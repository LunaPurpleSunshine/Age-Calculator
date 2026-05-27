"""Test helpers shared across the test modules."""

from __future__ import annotations

from contextlib import AbstractContextManager

from whenever import Date, Instant, patch_current_time


def freeze(today: Date) -> AbstractContextManager[object]:
    """Pin ``Date.today_in_system_tz()`` to ``today`` for the duration.

    Uses ``patch_current_time`` with an Instant at 12:00 UTC, which resolves
    to ``today`` for every system timezone between UTC-11 and UTC+11.
    """
    pinned = Instant.from_utc(today.year, today.month, today.day, hour=12)
    return patch_current_time(pinned, keep_ticking=False)
