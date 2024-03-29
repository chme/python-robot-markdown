"""Module that contains the command line application."""

# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m robot_markdown` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `robot_markdown.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `robot_markdown.__main__` in `sys.modules`.

from __future__ import annotations

import argparse
import sys
from typing import Any

from robot_markdown import debug
from robot_markdown.renderer import Renderer


class _DebugInfo(argparse.Action):
    def __init__(self, nargs: int | str | None = 0, **kwargs: Any) -> None:
        super().__init__(nargs=nargs, **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        debug.print_debug_info()
        sys.exit(0)


def get_parser() -> argparse.ArgumentParser:
    """Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(prog="robot-markdown")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {debug.get_version()}")
    parser.add_argument("--debug-info", action=_DebugInfo, help="Print debug information.")
    parser.add_argument("file", help="RobotFramework output.xml file.")
    return parser


def main(args: list[str] | None = None) -> int:
    """Run the main program.

    This function is executed when you type `robot-markdown` or `python -m robot_markdown`.

    Parameters:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts = parser.parse_args(args=args)
    print(opts)
    renderer = Renderer()
    print(renderer.render(opts.file))

    return 0
