import os
import json
import uuid
import logging
import requests
from pathlib import Path
from collections import Counter

from typing import Literal, Union, Optional

from .srt import parse
from .files import write
from .exceptions import OpenSubtitlesException
from .responses import SearchResult, DownloadResponse, Subtitle
from .download_client import DownloadClient

logger = logging.getLogger(__name__)

language_codes = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "he": "Hebrew",
}


class OpenSubtitles:
    """
    OpenSubtitles REST API Wrapper.
    """
    def __init__(self, api_key: str):
        self.download_client = DownloadClient()
        self.base_url = "https://api.opensubtitles.com/api/v1"
        self.token = None
        self.api_key = api_key
        self.user_agent = "duolex v0.0.1"
        self.downloads_dir = "."

    def send_api(self, cmd: str, body: Optional[dict] = None) -> dict:
        """
        Wrapper to the API request.
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "API-Key": self.api_key,
            "User-Agent": self.user_agent
        }
        if self.token:
            headers["authorization"] = self.token
        try:
            if body:
                response = requests.post(f"{self.base_url}/{cmd}", data=json.dumps(body), headers=headers)
            else:
                response = requests.get(f"{self.base_url}/{cmd}", headers=headers)
            response.raise_for_status()
            json_response = response.json()
            return json_response
        except requests.exceptions.HTTPError as http_err:
            raise OpenSubtitlesException(f"Failed with HTTP Error: {http_err}")
        except requests.exceptions.RequestException as req_err:
            raise OpenSubtitlesException(f"Failed to send request: {req_err}")
        except ValueError as ex:
            raise OpenSubtitlesException(f"Failed to parse login JSON response: {ex}")

    def login(self, username: str, password: str):
        """
        Login request - needed to obtain session token.
        """
        body = {'username': username, 'password': password}
        login_response = self.send_api("login", body)
        self.token = login_response['token']
        self.user_downloads_remaining = login_response['user']['allowed_downloads']
        return login_response

    def user_info(self):
        """
        Get user data.
        """
        response = self.send_api("infos/user")
        self.user_downloads_remaining = response['data']['remaining_downloads']
        return response

    def search(self, *,
               ai_translated: Union[str, Literal["exclude", "include"]]  = None,
               episode_number: Optional[int] = None,
               foreign_parts_only: Union[str, Literal["exclude", "include"]]  = None,
               hearing_impaired: Union[str, Literal["exclude", "include"]]  = None,
               id: Optional[int] = None,
               imdb_id: Optional[int] = None,
               languages: Optional[str] = None,
               machine_translated: Union[str, Literal["exclude", "include"]]  = None,
               moviehash: Optional[str] = None,
               moviehash_match: Union[str, Literal["include", "only"]]  = None,
               order_by: Optional[str] = None,
               order_direction: Union[str, Literal["asc", "desc"]]  = None,
               page: Optional[int] = None,
               parent_feature_id: Optional[int] = None,
               parent_imdb_id: Optional[int] = None,
               parent_tmdb_id: Optional[int] = None,
               query: Optional[str] = None,
               season_number: Optional[int] = None,
               tmdb_id: Optional[int] = None,
               trusted_sources: Union[str, Literal["include", "only"]]  = None,
               type: Union[str, Literal["movie", "episode", "all"]]  = None,
               user_id: Optional[int] = None,
               year: Optional[int] = None,
               ) -> SearchResult:
        """
        Search for subtitles.

        Docs: https://opensubtitles.stoplight.io/docs/opensubtitles-api/a172317bd5ccc-search-for-subtitles
        """
        query_params = []

        # Helper function to add a parameter to the query_params list
        def add_param(name, value):
            if value is not None:
                query_params.append(f"{name}={value}")

        # Add parameters to the query_params list
        add_param("ai_translated", ai_translated)
        add_param("episode_number", episode_number)
        add_param("foreign_parts_only", foreign_parts_only)
        add_param("hearing_impaired", hearing_impaired)
        add_param("id", id)
        add_param("imdb_id", imdb_id)
        add_param("languages", languages)
        add_param("machine_translated", machine_translated)
        add_param("moviehash", moviehash)
        add_param("moviehash_match", moviehash_match)
        add_param("order_by", order_by)
        add_param("order_direction", order_direction)
        add_param("page", page)
        add_param("parent_feature_id", parent_feature_id)
        add_param("parent_imdb_id", parent_imdb_id)
        add_param("parent_tmdb_id", parent_tmdb_id)
        add_param("query", query)
        add_param("season_number", season_number)
        add_param("tmdb_id", tmdb_id)
        add_param("trusted_sources", trusted_sources)
        add_param("type", type)
        add_param("user_id", user_id)
        add_param("year", year)

        if languages is not None:
            assert languages in language_codes, f"Invalid language code: {languages}"
        assert query_params, f"Missing subtitles search parameters"
        query_string = "&".join(query_params)

        search_response_data = self.send_api(f"subtitles?{query_string}")
        search_result = SearchResult(**search_response_data, query_string=query_string)
        return search_result

    def download(self, subtitle: Union[str, Subtitle]) -> bytes:
        """
        download a single subtitle file using the file_no
        """
        subtitle_id = subtitle.file_id if isinstance(subtitle, Subtitle) else subtitle
        if not subtitle_id:
            logger.warning(f"Missing subtitle file id.")
            return

        download_body = {'file_id': subtitle_id}

        if self.user_downloads_remaining == 0:
            logger.warning("Download limit reached. "
                           "Please upgrade your account or wait for your quota to reset (~24hrs)")
            return

        search_response_data = DownloadResponse(self.send_api(f"download", download_body))
        self.user_downloads_remaining = search_response_data.remaining

        content = self.download_client.get(search_response_data.link)
        return content

    def save_content_locally(self, content: bytes, filename: Optional[str] = None) -> str:
        local_filename = f'{filename or uuid.uuid4()}.srt'
        srt_path = Path(self.downloads_dir).joinpath(local_filename)
        write(srt_path, content)
        return srt_path

    def download_and_save(self, subtitle: Union[str, Subtitle]) -> str:
        content = self.download(subtitle)
        return self.save_content_locally(content, subtitle_id)

    def parse_srt(self, content):
        parsed_content = parse(content)
        return list(parsed_content)

    def bytes_to_str(self, content: bytes) -> str:
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        return content

    def str_to_bytes(self, content: str) -> bytes:
        if isinstance(content, str):
            content = content.decode("utf-8")
        return content
