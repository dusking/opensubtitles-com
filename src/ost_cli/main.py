"""
This file is part of Opensubtitles API wrapper.

Opensubtitles API is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published by the Massachusetts
Institute of Technology.

For full details, please see the LICENSE file located in the root
directory of this project.
"""

import sys
import getpass
import logging
import argparse
from typing import List
from pathlib import Path

from opensubtitlescom import Config, OpenSubtitles, FileUtils
from opensubtitlescom.exceptions import OpenSubtitlesException
from .table import dict_to_pt, dicts_to_pt

logger = logging.getLogger(__name__)

APP_NAME = "opensubtitlescom_py"
APP_VER = "0.1.3"
API_KEY = "CFpwJe7burdfYLEoTzSNG88Z7Lc2ex3b"
API_APP = f"{APP_NAME} v{APP_VER}"


def _get_api(cfg: Config):
    """Create an OpenSubtitles API object and login with the credentials in the config file."""
    subtitles = OpenSubtitles(API_APP, cfg.api_key or API_KEY)
    if cfg.username and cfg.password:
        subtitles.login(cfg.username, cfg.password)
    return subtitles


def set_credentials(args: argparse.Namespace):
    """Set the API key, username and password in the config file."""
    entered_api_key = input("Enter your API key (leave blank to keep existing): ").strip()
    entered_username = input("Enter your username (leave blank to keep existing): ").strip()
    entered_password = getpass.getpass("Enter your password (leave blank to keep existing): ").strip()
    cfg = Config(args.config)
    if entered_api_key:
        cfg.api_key = entered_api_key
    if entered_username:
        cfg.username = entered_username
    if entered_password:
        cfg.password = entered_password

    try:
        api = _get_api(cfg)
        api.login(cfg.username, cfg.password)
        if cfg.save():
            print("Credentials set successfully!")
    except OpenSubtitlesException:
        print("Failed to authorize user. Check the provided username/password.")


def hide_secret(secret, show_chars=2):
    """Hide most characters in the middle of the secret value.

    Args:
        secret (str): The secret to be hidden.
        show_chars (int): The number of characters to reveal at the beginning and end.

    Returns:
        str: The password with hidden characters.
    """
    if not secret:
        return ""
    if len(secret) <= show_chars * 2:
        return secret  # Not enough characters to hide

    hidden_part = "*" * (len(secret) - show_chars * 2)
    hidden_password = secret[:show_chars] + hidden_part + secret[-show_chars:]
    return hidden_password


def show_credentials(args: argparse.Namespace):
    """Show the username and password in the config file."""
    cfg = Config(args.config)
    values = {
        "username": cfg.username,
        "password": hide_secret(cfg.password, 2),
        "language": cfg.language,
    }
    if cfg.api_key:
        # The API Key is not really a credential, but it is in the scope of it.
        values["api key"] = cfg.api_key
    print(dict_to_pt(values, align="l"))


def user_info(args: argparse.Namespace):
    """Print current user info."""
    cfg = Config(args.config)
    try:
        api = _get_api(cfg)
        response = api.user_info()
        print(dict_to_pt(response["data"], align="l"))
    except OpenSubtitlesException as ex:
        print(f"Failed to retrieve user info: {ex.message}")


def search(args: argparse.Namespace):
    """Search for subtitles by various criteria."""
    cfg = Config(args.config)
    api = _get_api(cfg)

    search_params = {"query": args.query, "languages": args.language or cfg.language}
    response = api.search(**search_params)
    all_results = []
    for result in response.data:
        all_results.append(
            {"title": result.title, "imdb-id": result.imdb_id, "file-id": result.file_id, "file-name": result.file_name}
        )
    print(dicts_to_pt(all_results, sort="imdb-id", align="l"))


def get_srt_output_file(args: argparse.Namespace):
    """Get the subtitle file name."""
    if args.output:
        return Path(args.output)
    if args.file_id:
        return Path(str(args.file_id)).with_suffix(".srt")
    if args.file:
        return Path(args.file).with_suffix(".srt")
    return None


def download(args: argparse.Namespace):
    """Download a subtitle by file-id or movie-hash."""
    cfg = Config(args.config)
    api = _get_api(cfg)

    output_file = get_srt_output_file(args)

    if args.file_id:
        with open(output_file, "wb") as fp:
            fp.write(api.download(file_id=args.file_id))
        print(f"Subtitles have been downloaded to: `{output_file}`")
    elif args.file:
        # Given a local file, search for the hash and download the first result,
        # eg "ost download --file mymovie.mp4" will download the subtitle for
        # mymovie.mp4 and save it as mymovie.srt
        mov = Path(args.file)
        fu = FileUtils(mov)
        h = fu.get_hash()
        response = api.search(moviehash=h, languages=cfg.language)
        if not response.data:
            print(f"No subtitles found for {mov}")
            return
        print(f"Found {len(response.data)} subtitles, downloading the first into {output_file}")
        with open(output_file, "wb") as fp:
            fp.write(api.download(file_id=response.data[0].file_id))
    elif args.query:
        # Given a search query, grab the subtitles for the first result
        response = api.search(languages=cfg.language, query=args.query)
        if not response.data:
            print(f"No subtitles found for {args.query}")
            return
        output_file = output_file or response.data[0].file_name
        with open(output_file, "wb") as fp:
            fp.write(api.download(file_id=response.data[0].file_id))
        print(f"Subtitles have been downloaded to: `{output_file}`")


def parse_args(argv: List[str]):
    """Parse command-line arguments for the OpenSubtitles CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", type=Path, default="~/.config/opensubtitlescom/config.json", help="Path to the configuration file"
    )
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity level")

    subparsers = parser.add_subparsers(dest="command")

    set_credentials_parser = subparsers.add_parser("set-cred", help=set_credentials.__doc__)
    set_credentials_parser.set_defaults(command=set_credentials)

    set_credentials_parser = subparsers.add_parser("show-cred", help=show_credentials.__doc__)
    set_credentials_parser.set_defaults(command=show_credentials)

    user_info_parser = subparsers.add_parser("user-info", help=user_info.__doc__)
    user_info_parser.set_defaults(command=user_info)

    search_parser = subparsers.add_parser("search", help=search.__doc__)
    search_parser.set_defaults(command=search)
    search_parser.add_argument("--query", type=str, help="Movie file name or text search")
    search_parser.add_argument("--language", type=str, help="Language for subtitle search")

    download_parser = subparsers.add_parser("download", help=download.__doc__)
    download_parser.set_defaults(command=download)
    download_parser.add_argument("--file-id", type=int, help="Download a specific OSC file by ID")
    download_parser.add_argument("--file", type=Path, help="Download the subtitles for a local file")
    download_parser.add_argument("--query", type=str, help="Download the first subtitle matching the query")
    download_parser.add_argument("--output", type=str, help="Output file name")
    return parser.parse_args(argv)


def main():
    """Parse command line arguments and executes the specified command."""
    argv = sys.argv
    args = parse_args(argv[1:])
    logging.basicConfig(
        level=logging.WARNING - (args.verbose * 10),
        format="%(asctime)s %(message)s",
    )
    if args.command:
        return args.command(args)
    else:
        print("No command given, use --help for usage")
        return 1


if __name__ == "__main__":
    sys.exit(main())
