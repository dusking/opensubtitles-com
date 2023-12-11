#!/usr/bin/env python3

import sys
import logging
import argparse
from typing import List


logger = logging.getLogger(__name__)


def hello(args: argparse.Namespace):
    """Just a stub command for the skeleton, this will be replaced in the next commit"""
    print(f"Hello {args.name}!")


def parse_args(argv: List[str]):
    """Parse command-line arguments for the OpenSubtitles CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity level")

    subparsers = parser.add_subparsers(dest="command")

    hello_parser = subparsers.add_parser("hello", help=hello.__doc__)
    hello_parser.set_defaults(command=hello)
    hello_parser.add_argument("name")

    return parser.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    logging.basicConfig(
        level=logging.WARNING - (args.verbose * 10),
        format="%(asctime)s %(message)s",
    )
    if args.command:
        return args.command(args)
    else:
        print("No command given, use --help for usage")


if __name__ == "__main__":
    main()
