import os
import sys
import getpass
import logging
import argparse
from typing import List
from pathlib import Path

from opensubtitlescom import OpenSubtitles, FileUtils, Config

from .table import dicts_to_pt

logger = logging.getLogger(__name__)


def set_credentials(args: argparse.Namespace):
    """Set the username and password in the config file
    """
    cfg = Config(args.config)
    entered_appname = input("Enter your app name (leave blank to keep existing): ")
    if entered_appname.strip():
        cfg.app_name = entered_appname
    entered_api_key = input("Enter your app key (leave blank to keep existing): ")
    if entered_api_key.strip():
        cfg.api_key = entered_api_key
    entered_username = input("Enter your username (leave blank to keep existing): ")
    if entered_username.strip():
        cfg.username = entered_username
    entered_password = getpass.getpass("Enter your password (leave blank to keep existing): ")
    if entered_password.strip():
        cfg.password = entered_password
    cfg.save()
    print("Credentials set successfully")


def _get_api(cfg: Config):
    """Create an OpenSubtitles API object and login with the credentials in the config file.
    """
    subtitles = OpenSubtitles(cfg.api_key, cfg.app_full_name)
    if cfg.username and cfg.password:
        subtitles.login(cfg.username, cfg.password)
    return subtitles


def search(args: argparse.Namespace):
    """Search for subtitles by various criteria.
    """
    cfg = Config(args.config)
    api = _get_api(cfg)

    search_params = {
        "query": args.query,
        "languages": args.language or cfg.langauge
    }
    response = api.search(**search_params)
    all_results = []
    for result in response.data:
        all_results.append({
            "title": result.title,
            "imdb-id": result.imdb_id,
            "file-id": result.file_id,
            "file-name": result.file_name
        })
    print(dicts_to_pt(all_results, sort="imdb-id", align="l"))


def download(args: argparse.Namespace):
    """Download a subtitle by file-id or movie-hash.
    """
    cfg = Config(args.config)
    api = _get_api(cfg)

    if args.file_id:
        # Given a file-id, download the subtitle
        file_id = args.file_id
        filename = f"{file_id}.srt"
    elif args.file_path:
        # Given a local file, search for the hash and download the first result,
        # eg "download mymovie.mp4" will download the subtitle for mymovie.mp4
        # and save it as mymovie.srt
        if not os.path.exists(args.key):
            print(f"Failed to find file {args.file_path}")
            return
        mov = Path(args.key)
        response = api.search(moviehash=FileUtils(mov).get_hash(), languages=cfg.langauge)
        if not response.data:
            print(f"Failed to find subtitles for {args.file_path}")
            return
        filename = mov.with_suffix(".srt")
        file_id = response.data[0].file_id
    else:
        print("Missing required search parameters.")
        return

    with open(filename, "wb") as srt:
        srt.write(api.download(file_id=file_id))
    print(f"srt file content downloaded to: {filename}")


def parse_args(argv: List[str]):
    """Parse command-line arguments for the OpenSubtitles CLI.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default="~/.config/opensubtitlescom/cli.json",
                        help="Path to the configuration file")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increase verbosity level")

    subparsers = parser.add_subparsers(dest="command")

    set_credentials_parser = subparsers.add_parser("set-cred", help=set_credentials.__doc__)
    set_credentials_parser.set_defaults(command=set_credentials)

    search_parser = subparsers.add_parser("search", help=search.__doc__)
    search_parser.set_defaults(command=search)
    search_parser.add_argument("--query", type=str, help="Movie file name or text search")
    search_parser.add_argument("--language", type=str, help="Language for subtitle search")

    download_parser = subparsers.add_parser("download", help=download.__doc__)
    download_parser.set_defaults(command=download)
    download_parser.add_argument("--file-id", type=str, help="Subtitles file-id")
    download_parser.add_argument("--file-path", type=str, help="Local movie file to download by movie-hash")

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
