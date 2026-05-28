"""Calculate ages and next birthdays from a date of birth.

The package exposes three pure functions in :mod:`agecalc.core` for
programmatic use and an ``agecalc`` command-line interface in
:mod:`agecalc.cli`. The command is installed as a console script via
``[project.scripts]`` in :file:`pyproject.toml` and can also be run as
``python -m agecalc``.

Examples
--------
Programmatic use:

>>> from whenever import Date
>>> from agecalc import calculate_age
>>> calculate_age(Date(1994, 7, 1))  # doctest: +SKIP
30
"""

from agecalc.core import calculate_age, calculate_next_birthday, expand_year

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "calculate_age",
    "calculate_next_birthday",
    "expand_year",
]
