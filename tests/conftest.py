"""Shared pytest configuration.

Currently empty: the ``whenever`` migration removed the previous
``freeze_today`` fixture in favour of the ``freeze`` context manager in
:mod:`tests._helpers`. The file is kept so pytest's conftest collection
still picks up the directory as a rootdir, and for future fixtures.
"""
