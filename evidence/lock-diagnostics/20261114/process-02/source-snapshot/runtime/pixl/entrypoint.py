"""Dispatch readiness before importing the dependency-heavy runtime CLI."""

import sys


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] == "readiness":
        from .readiness import main as readiness_main

        return readiness_main(arguments[1:])
    from .cli import main as cli_main

    return cli_main(arguments)
