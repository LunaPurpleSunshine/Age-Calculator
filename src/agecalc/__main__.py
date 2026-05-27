"""Allow ``python -m agecalc`` to invoke the CLI."""

from agecalc.cli import main

raise SystemExit(main())
