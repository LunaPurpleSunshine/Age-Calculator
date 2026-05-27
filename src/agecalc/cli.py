"""Command-line interface for agecalc."""

from __future__ import annotations

import argparse
from datetime import date

from agecalc.core import calculate_age, calculate_next_birthday, expand_year


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agecalc",
        description="Calculate an age and next birthday from a birth date.",
    )
    parser.add_argument(
        "year",
        help=(
            "Required. The birth year of the person to be aged. "
            "YYYY or YY (assumes 19XX if not possible in 2000s)."
        ),
    )
    parser.add_argument(
        "month",
        nargs="?",
        default="01",
        help="Optional (default 01). The birth month of the person to be aged. MM.",
    )
    parser.add_argument(
        "day",
        nargs="?",
        default="01",
        help="Optional (default 01). The birth day of the person to be aged. DD.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``agecalc`` console script."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if len(args.year) == 2:
        year = expand_year(int(args.year))
    elif len(args.year) == 4:
        year = int(args.year)
    else:
        parser.error(f"year must be 2 or 4 digits, got {args.year!r}")

    try:
        month = int(args.month)
        day = int(args.day)
        birthday = date(year, month, day)
    except ValueError as exc:
        parser.error(f"invalid date {args.year}-{args.month}-{args.day}: {exc}")

    age = calculate_age(birth_date=birthday)

    if age >= 0:
        print(f"{age} years old today {date.today()}")
        next_birthday = calculate_next_birthday(birth_date=birthday)
        if next_birthday == date.today():
            print(f"Turned {age} today!")
        else:
            print(f"Will turn {age + 1} on next birthday {next_birthday}")
    else:
        print(f"{abs(age)} years in the future")

    return 0
