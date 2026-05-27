# age-calculator

A tiny command-line tool that calculates someone's age and tells you when their next birthday falls.

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

You can also run the module form:

```bash
python -m agecalc 1994 07 01
```

## CLI reference

```
agecalc <year> [month] [day]
```

| Argument | Required | Format        | Default | Description                                                                                          |
| -------- | -------- | ------------- | ------- | ---------------------------------------------------------------------------------------------------- |
| `year`   | yes      | `YYYY` or `YY` | —       | Birth year. A 2-digit year that would land in the future is interpreted as 19YY instead of 20YY. |
| `month`  | no       | `MM`          | `01`    | Birth month.                                                                                         |
| `day`    | no       | `DD`          | `01`    | Birth day.                                                                                           |

### Examples

```bash
# 4-digit year, full date
agecalc 1994 07 01

# Year only — defaults month/day to 01/01
agecalc 1994

# 2-digit year (auto-expanded)
agecalc 94 07 01      # → 1994-07-01
agecalc 22 07 01      # → 2022-07-01

# Future birth date
agecalc 2050 01 01
# 24 years in the future
```

The CLI prints today's age and the next upcoming birthday. If today happens to be the birthday, you'll see `Turned N today!` instead. Future dates report how many years away they are.

## Development

This project is managed with [uv](https://docs.astral.sh/uv/) and uses a `src/` layout.

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

This repo ships a `.pre-commit-config.yaml` that runs `ruff` lint + format on commit. Use [prek](https://prek.j178.dev/) (a fast, drop-in replacement for `pre-commit`):

```bash
uv tool install prek
prek install            # install the git hook in this clone
prek run --all-files    # run all hooks against the whole repo
```

CI runs the same checks across Python 3.12, 3.13, and 3.14 on every push and pull request.

## License

MIT
