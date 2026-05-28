"""Command-line interface for agecalc."""

from __future__ import annotations

import click
from whenever import Date

from agecalc.core import calculate_age, calculate_next_birthday, expand_year


def _parse_year(ctx: click.Context, param: click.Parameter, value: str) -> int:
    if len(value) == 2:
        return expand_year(int(value))
    if len(value) == 4:
        return int(value)
    raise click.BadParameter(f"year must be 2 or 4 digits, got {value!r}", ctx=ctx, param=param)


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("year", callback=_parse_year)
@click.argument("month", default="01")
@click.argument("day", default="01")
def main(year: int, month: str, day: str) -> None:
    """Calculate an age and next birthday from a birth date.

    YEAR may be YYYY or YY (a 2-digit year that would land in the future is
    interpreted as 19YY instead of 20YY). MONTH and DAY default to 01.
    """
    try:
        birthday = Date(year, int(month), int(day))
    except ValueError as exc:
        raise click.BadParameter(f"invalid date {year:04d}-{month}-{day}: {exc}") from exc

    age = calculate_age(birth_date=birthday)
    today = Date.today_in_system_tz()

    if age >= 0:
        click.echo(f"{age} years old today {today}")
        next_birthday = calculate_next_birthday(birth_date=birthday)
        if next_birthday == today:
            click.echo(f"Turned {age} today!")
        else:
            click.echo(f"Will turn {age + 1} on next birthday {next_birthday}")
    else:
        click.echo(f"{abs(age)} years in the future")
