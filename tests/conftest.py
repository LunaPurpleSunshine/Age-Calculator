"""Shared pytest fixtures."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date

import pytest

import agecalc.cli
import agecalc.core


@pytest.fixture
def freeze_today(monkeypatch: pytest.MonkeyPatch) -> Callable[[date], None]:
    """Return a function that pins ``date.today()`` to a given value.

    The patch is applied to the ``date`` symbol imported by both ``core`` and
    ``cli`` modules so all internal calls see the same frozen value.
    """

    def _freeze(today: date) -> None:
        class FrozenDate(date):
            @classmethod
            def today(cls) -> date:
                return today

        monkeypatch.setattr(agecalc.core, "date", FrozenDate)
        monkeypatch.setattr(agecalc.cli, "date", FrozenDate)

    return _freeze
