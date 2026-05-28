# age-calculator

A small command-line tool that calculates someone's age and tells you when their next birthday falls.

```console
$ agecalc 1994 07 01
30 years old today 2025-05-27
Will turn 31 on next birthday 2025-07-01
```

## Install

The package is published as **`age-calculator`** on PyPI and exposes the **`agecalc`** command.

Using [uv](https://docs.astral.sh/uv/) (recommended):

```bash
uv tool install age-calculator
```

Run without installing:

```bash
uvx age-calculator 1994 07 01
```

Or with pipx:

```bash
pipx install age-calculator
```

You can also run the module form once the package is on your `PYTHONPATH`:

```bash
python -m agecalc 1994 07 01
```

## CLI reference

```
agecalc [-h | --help] YEAR [MONTH] [DAY]
```

| Argument | Required | Format          | Default | Description                                                                                          |
| -------- | -------- | --------------- | ------- | ---------------------------------------------------------------------------------------------------- |
| `YEAR`   | yes      | `YYYY` or `YY`  | —       | Birth year. A 2-digit year that would otherwise fall in the future is interpreted as 19YY, not 20YY. |
| `MONTH`  | no       | `MM`            | `01`    | Birth month.                                                                                         |
| `DAY`    | no       | `DD`            | `01`    | Birth day.                                                                                           |

| Option         | Description              |
| -------------- | ------------------------ |
| `-h`, `--help` | Show usage and exit (0). |

The CLI prints today's age and the date of the next upcoming birthday. If today *is* the birthday, it prints `Turned N today!` in place of the next-birthday line. Future birth dates print `N years in the future`. People born on 29 February have their non-leap-year birthdays observed on 28 February.

Invalid input (a year that is not 2 or 4 digits, a non-numeric month or day, or a date that does not exist on the calendar) exits with status `2` and a click-formatted error message on standard error.

### Examples

```bash
# Full date with a 4-digit year
agecalc 1994 07 01

# Year only — month and day default to 01
agecalc 1994

# 2-digit year (auto-expanded against the current year)
agecalc 94 07 01      # → 1994-07-01
agecalc 22 07 01      # → 2022-07-01

# A future birth date
agecalc 2050 01 01    # → 24 years in the future
```

## Library use

The package ships type information (PEP 561 `py.typed`), so any importer gets full type-checking out of the box:

```python
from whenever import Date

from agecalc import calculate_age, calculate_next_birthday, expand_year

calculate_age(Date(1994, 7, 1))
calculate_next_birthday(Date(1994, 7, 1))
expand_year(94)
```

All three functions are pure and read "today" from the system timezone via `whenever.Date.today_in_system_tz()`. See the docstrings (NumPy style) for the full signature and behaviour, including the 29 February fallback.

## Dependencies

Runtime: [`click`](https://click.palletsprojects.com/) for the CLI and [`whenever`](https://whenever.readthedocs.io/) for the date arithmetic. Nothing else.

## Development

The project is managed with [uv](https://docs.astral.sh/uv/) and uses a `src/` layout.

```bash
# Clone and set up
git clone https://github.com/LunaPurpleSunshine/Age-Calculator.git
cd Age-Calculator
uv sync --all-groups

# Run the CLI from your checkout
uv run agecalc 1994 07 01

# Tests, lint, type-check, build
uv run pytest --cov=agecalc
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv build
```

### Pre-commit hooks

The repo ships a `.pre-commit-config.yaml` that runs `ruff` (lint + format) and a handful of file-hygiene hooks on commit. Use [prek](https://prek.j178.dev/) (a fast, drop-in replacement for `pre-commit`):

```bash
uv tool install prek
prek install            # install the git hook in this clone
prek run --all-files    # run all hooks against the whole repo
```

CI runs the same checks across Python 3.12, 3.13, and 3.14 on every push and pull request, plus a `uv build` + `twine check` job to verify the built distribution.

## Licence

Released under the MIT licence.
