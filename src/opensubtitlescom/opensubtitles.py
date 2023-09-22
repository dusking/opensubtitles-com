"""
Copyright (c) 2023 Omer Duskin.

This file is part of Opensubtitles API wrapper.

Opensubtitles API is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published by the Massachusetts
Institute of Technology.

For full details, please see the LICENSE file located in the root
directory of this project.

This is the main module for the opensubtitles wrapper.
It contains wrpper functoins for the opensubtitles.com REST API.
"""

import json
import uuid
import logging
import requests
from pathlib import Path

from typing import Literal, Union, Optional

from .srt import parse
from .files import write
from .exceptions import OpenSubtitlesException
from .responses import (
    SearchResponse,
    DownloadResponse,
    Subtitle,
    DiscoverLatestResponse,
    DiscoverMostDownloadedResponse,
)
from .download_client import DownloadClient
from .languages import language_codes

logger = logging.getLogger(__name__)


class OpenSubtitles:
    """OpenSubtitles REST API Wrapper."""

    def __init__(self, api_key: str, user_agent: str):
        """Initialize the OpenSubtitles object.

        :param api_key:
        :param user_agent: a string representing the user agent, like: "MyApp v0.0.1"
        """
        self.download_client = DownloadClient()
        self.base_url = "https://api.opensubtitles.com/api/v1"
        self.token = None
        self.api_key = api_key
        self.user_agent = user_agent
        self.downloads_dir = "."

    def send_api(
        self, cmd: str, body: Optional[dict] = None, method: Union[str, Literal["GET", "POST", "DELETE"]] = None
    ) -> dict:
        """Send the API request."""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "API-Key": self.api_key,
            "User-Agent": self.user_agent,
        }
        if self.token:
            headers["authorization"] = self.token
        try:
            if method == "DELETE":
                response = requests.delete(f"{self.base_url}/{cmd}", headers=headers)
            elif body:
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

        Docs: https://opensubtitles.stoplight.io/docs/opensubtitles-api/73acf79accc0a-login
        """
        body = {"username": username, "password": password}
        login_response = self.send_api("login", body)
        self.token = login_response["token"]
        self.user_downloads_remaining = login_response["user"]["allowed_downloads"]
        return login_response

    def logout(self, username: str, password: str):
        """
        Destroy a user token to end a session.

        Docs: https://opensubtitles.stoplight.io/docs/opensubtitles-api/9fe4d6d078e50-logout
        """
        response = self.send_api("logout", method="DELETE")
        return response

    def user_info(self):
        """
        Get user data.

        Docs: https://opensubtitles.stoplight.io/docs/opensubtitles-api/ea912bb244ef0-user-informations
        """
        response = self.send_api("infos/user")
        self.user_downloads_remaining = response["data"]["remaining_downloads"]
        return response

    def languages_info(self):
        """
        Get the languages information.

        Docs: https://opensubtitles.stoplight.io/docs/opensubtitles-api/1de776d20e873-languages
        """
        response = self.send_api("infos/languages")
        return response

    def formats_info(self):
        """
        Get the languages information.

        Docs: https://opensubtitles.stoplight.io/docs/opensubtitles-api/69b286fc7506e-subtitle-formats
        """
        response = self.send_api("infos/formats")
        return response

    def discover_latest(self):
        """
        Get 60 latest uploaded subtitles.

        Docs: https://opensubtitles.stoplight.io/docs/opensubtitles-api/f36cef28efaa9-latest-subtitles
        """
        response = self.send_api("discover/latest")
        return DiscoverLatestResponse(**response)

    def discover_most_downloaded(
        self, languages: Optional[str] = None, type: Union[str, Literal["movie", "tvshow"]] = None
    ):
        """
        Get popular subtitles, according to last 30 days downloads on opensubtitles.com.

        Docs: https://opensubtitles.stoplight.io/docs/opensubtitles-api/3a149b956fcab-most-downloaded-subtitles
        """
        response = self.send_api("discover/most_downloaded")
        return DiscoverMostDownloadedResponse(**response)

    def search(
        self,
        *,
        ai_translated: Union[str, Literal["exclude", "include"]] = None,
        episode_number: Optional[int] = None,
        foreign_parts_only: Union[str, Literal["exclude", "include"]] = None,
        hearing_impaired: Union[str, Literal["exclude", "include"]] = None,
        id: Optional[int] = None,
        imdb_id: Optional[int] = None,
        languages: Optional[str] = None,
        machine_translated: Union[str, Literal["exclude", "include"]] = None,
        moviehash: Optional[str] = None,
        moviehash_match: Union[str, Literal["include", "only"]] = None,
        order_by: Optional[str] = None,
        order_direction: Union[str, Literal["asc", "desc"]] = None,
        page: Optional[int] = None,
        parent_feature_id: Optional[int] = None,
        parent_imdb_id: Optional[int] = None,
        parent_tmdb_id: Optional[int] = None,
        query: Optional[str] = None,
        season_number: Optional[int] = None,
        tmdb_id: Optional[int] = None,
        trusted_sources: Union[str, Literal["include", "only"]] = None,
        type: Union[str, Literal["movie", "episode", "all"]] = None,
        user_id: Optional[int] = None,
        year: Optional[int] = None,
    ) -> SearchResponse:
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
        assert query_params, "Missing subtitles search parameters"
        query_string = "&".join(query_params)

        search_response_data = self.send_api(f"subtitles?{query_string}")
        return SearchResponse(**search_response_data, query_string=query_string)

    def download(
        self,
        file_id: Union[str, Subtitle],
        sub_format: Optional[int] = None,
        file_name: Optional[int] = None,
        in_fps: Optional[int] = None,
        out_fps: Optional[int] = None,
        timeshift: Optional[int] = None,
        force_download: Optional[bool] = None,
    ) -> bytes:
        """
        Download a single subtitle file using the file_no.

        Docs: https://opensubtitles.stoplight.io/docs/opensubtitles-api/6be7f6ae2d918-download
        """
        subtitle_id = file_id.file_id if isinstance(file_id, Subtitle) else file_id
        if not subtitle_id:
            logger.warning("Missing subtitle file id.")
            return

        download_body = {"file_id": subtitle_id}

        # Helper function to add a parameter to the query_params list
        def add_param(name, value):
            if value is not None:
                download_body[name] = value

        add_param("sub_format", sub_format)
        add_param("file_name", file_name)
        add_param("in_fps", in_fps)
        add_param("out_fps", out_fps)
        add_param("timeshift", timeshift)
        add_param("force_download", force_download)

        if self.user_downloads_remaining <= 0:
            logger.warning(
                "Download limit reached. " "Please upgrade your account or wait for your quota to reset (~24hrs)"
            )
            return

        search_response_data = DownloadResponse(self.send_api("download", download_body))
        self.user_downloads_remaining = search_response_data.remaining

        return self.download_client.get(search_response_data.link)

    def save_content_locally(self, content: bytes, filename: Optional[str] = None) -> str:
        """
        Save content locally.

        :param content: content of dubtitle file.
        :param filename:  target local filename.
        :return: the path of the local file containing the content.
        """
        local_filename = f"{filename or uuid.uuid4()}.srt"
        srt_path = Path(self.downloads_dir).joinpath(local_filename)
        write(srt_path, content)
        return srt_path

    def download_and_save(self, file_id: Union[str, Subtitle], **kwargs) -> str:
        """Call the download function to get rge subtitle content, then save the content to a local file.

        :param file_id: file_id or subtitles object.
        :return: local file path.
        """
        subtitle_id = file_id.file_id if isinstance(file_id, Subtitle) else file_id
        content = self.download(subtitle_id, **kwargs)
        if not content:
            logger.warning(f"Failed to get content for: {file_id}")
            return
        return self.save_content_locally(content, subtitle_id)

    def parse_srt(self, content):
        """
        Parse subtitles in SRT format.

        Args:
            content (str): The content of the subtitles SRT file.

        Returns:
            list: A list of parsed subtitle entries.
        """
        parsed_content = parse(content)
        return list(parsed_content)

    def bytes_to_str(self, content: bytes) -> str:
        """
        Convert bytes content to a string.

        Args:
            content (bytes): The bytes content to be converted.

        Returns:
            str: The content as a UTF-8 encoded string.
        """
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        return content

    def str_to_bytes(self, content: str) -> bytes:
        """
        Convert string content to bytes.

        Args:
            content (str): The string content to be converted.

        Returns:
            bytes: The content as bytes, encoded in UTF-8.
        """
        if isinstance(content, str):
            content = content.decode("utf-8")
        return content
