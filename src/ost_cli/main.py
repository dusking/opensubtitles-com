#!/usr/bin/env python3

import typing as t
from pathlib import Path
import sys
import argparse
import os
import logging

from opensubtitlescom import OpenSubtitles, FileUtils
from .config import Config

log = logging.getLogger(__name__)


APP_NAME = "CLI Test"
APP_VER = "0.0.0"
API_KEY = "F0f1dadQ89xKIP5TIsu3Y8KT7TiDBIfG"
API_APP = f"{APP_NAME} v{APP_VER}"

def _get_api(cfg: Config):
    """
    Create an OpenSubtitles API object and login with the credentials in the config file
    """
    subtitles = OpenSubtitles(API_KEY, API_APP)
    if cfg.username and cfg.password:
        subtitles.login(cfg.username, cfg.password)
    return subtitles


def login(args: argparse.Namespace):
    """
    Check that the login credentials are valid and save them to the config file
    """
    try:
        subtitles = OpenSubtitles(API_KEY, API_APP)
        subtitles.login(args.username, args.password)

        log.info("Login successful, saving credentials to config file")
        cfg = Config(args.config)
        cfg.username = args.username
        cfg.password = args.password
        cfg.save()
    except Exception as e:
        print(e)
        return


def search(args: argparse.Namespace):
    """
    Search for subtitles by various criteria
    """
    ...


def download(args: argparse.Namespace):
    """
    Download a subtitle by file-id or moviehash
    """
    cfg = Config(args.config)
    api = _get_api(cfg)

    if args.key.isdigit():
        # Given a file-id, download the subtitle
        ...
    elif os.path.exists(args.key):
        # Given a local file, search for the hash and download the first result,
        # eg "download mymovie.mp4" will download the subtitle for mymovie.mp4
        # and save it as mymovie.srt
        mov = Path(args.key)
        srt = mov.with_suffix(".srt")
        fu = FileUtils(mov)
        h = fu.get_hash()
        response = api.search(moviehash=h, languages=cfg.langauge)
        log.info("Found %d subtitles, downloading the first into %s", len(response.data), srt)
        with open(srt, "wb") as fp:
            fp.write(api.download(file_id=response.data[0].file_id))


def parse_args(argv: t.List[str]):
    """Parse command-line arguments for the OpenSubtitles CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity level")
    parser.add_argument("--config", type=Path, default="~/.config/opensubtitlescom/cli.json")

    subparsers = parser.add_subparsers(dest="command")

    login_parser = subparsers.add_parser("login", help=login.__doc__)
    login_parser.set_defaults(command=login)
    login_parser.add_argument("username", type=str)
    login_parser.add_argument("password", type=str)

    search_parser = subparsers.add_parser("search", help=search.__doc__)
    search_parser.set_defaults(command=search)
    search_parser.add_argument("--moviehash", type=str)
    search_parser.add_argument("--languages", type=str)

    download_parser = subparsers.add_parser("download", help=download.__doc__)
    download_parser.set_defaults(command=download)
    download_parser.add_argument(
        "key", type=str, help="unique ID - either file-id, or a local filename to download by moviehash"
    )

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
