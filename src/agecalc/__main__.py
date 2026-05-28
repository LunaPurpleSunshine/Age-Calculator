"""Entry point for ``python -m agecalc``.

Delegates to :func:`agecalc.cli.main`, which click invokes in standalone
mode and which will call :func:`sys.exit` itself.
"""

from agecalc.cli import main

main()
