"""
Copyright (c) 2023 Omer Duskin.

This file is part of Opensubtitles API wrapper.

Opensubtitles API is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published by the Massachusetts
Institute of Technology.

For full details, please see the LICENSE file located in the root
directory of this project.

This module define responses for the opensubtitles REST API.
"""

import logging
from datetime import datetime

from .responses_base import BaseResponse

logger = logging.getLogger(__name__)


class LoginResponse(BaseResponse):
    """Response class for the login results."""

    def __init__(self, user, token, status):
        """
        Initialize a LoginResponse object with user data, token, and status.

        Args:
            user (User): An dict representing the user data.
            token (str): The authentication token.
            status (int): The status code of the login response (e.g., 200 for success).


        Example:
            # Create a LoginResponse object
            user_data = {allowed_translations=1, allowed_downloads=20, level='Sub leecher', user_id=502210,
                             ext_installed=False, vip=False}
            login_response = LoginResponse(user=user_data, token='eyJ0eXAiOiJKV1Qi...', status=200)
        """
        self.user = user
        self.token = token
        self.status = status

    class Meta:
        """Meta class for LoginResponse."""

        main_field = "status"


class SearchResponse(BaseResponse):
    """Response class for search results."""

    def __init__(self, total_pages, total_count, per_page, page, data, query_string=None):
        """Initialize the SearchResponse object with search-related data.

        Args:
            total_pages (int): The total number of pages in the search results.
            total_count (int): The total number of search results.
            per_page (int): The number of results per page.
            page (int): The current page number.
            data (list): A list of data items for each search result.
            query_string (str): The search query string.
        """
        self.total_pages = total_pages
        self.total_count = total_count
        self.per_page = per_page
        self.page = page
        self.data = [Subtitle(item) for item in data]
        self.query_string = query_string

    class Meta:
        """Meta class for SearchResponse."""

        main_field = "query_string"


class DiscoverLatestResponse(BaseResponse):
    """Response class for discover latest results."""

    def __init__(self, total_pages, total_count, page, data):
        """Initialize the DiscoverLatestResponse object with latest discovery data.

        Args:
            total_pages (int): The total number of pages in the discovery results.
            total_count (int): The total number of discovery results.
            page (int): The current page number.
            data (list): A list of data items for each discovery result.
        """
        self.total_pages = total_pages
        self.total_count = total_count
        self.page = page
        self.data = [Subtitle(item) for item in data]
        self.created_at = datetime.now()
        self.created_at_str = self.created_at.strftime("%Y-%m-%d %H:%M%z")

    class Meta:
        """Meta class for DiscoverLatestResponse."""

        main_field = "created_at_str"


class DiscoverMostDownloadedResponse(DiscoverLatestResponse):
    """Response class for the discovre most downloaded results."""

    pass


class DownloadResponse(BaseResponse):
    """Response class for the download subtitles results."""

    def __init__(self, response_data):
        """Initialize the DownloadResponse object with download-related data.

        Args:
            response_data (dict): A dictionary containing download-related information.
        """
        self.link = response_data.get("link")
        self.file_name = response_data.get("file_name")
        self.requests = response_data.get("requests")
        self.remaining = response_data.get("remaining")
        self.message = response_data.get("message")
        self.reset_time = response_data.get("reset_time")
        self.reset_time_utc = response_data.get("reset_time_utc")
        self.uk = response_data.get("uk")
        self.uid = response_data.get("uid")
        self.ts = response_data.get("ts")

    class Meta:
        """Meta class for DownloadResponse."""

        main_field = "file_name"


class Subtitle(BaseResponse):
    """Object representing a subtitle data given from API."""

    def __init__(self, data_dict):
        """Initialize the Subtitle object with subtitle-related data.

        Args:
            data_dict (dict): A dictionary containing subtitle-related information.
        """
        self.id = data_dict.get("id")
        self.type = data_dict.get("type")
        self.subtitle_id = data_dict.get("attributes", {}).get("subtitle_id")
        self.language = data_dict.get("attributes", {}).get("language")
        self.download_count = data_dict.get("attributes", {}).get("download_count")
        self.new_download_count = data_dict.get("attributes", {}).get("new_download_count")
        self.hearing_impaired = data_dict.get("attributes", {}).get("hearing_impaired")
        self.hd = data_dict.get("attributes", {}).get("hd")
        self.fps = data_dict.get("attributes", {}).get("fps")
        self.votes = data_dict.get("attributes", {}).get("votes")
        self.ratings = data_dict.get("attributes", {}).get("ratings")
        self.from_trusted = data_dict.get("attributes", {}).get("from_trusted")
        self.foreign_parts_only = data_dict.get("attributes", {}).get("foreign_parts_only")
        self.upload_date = data_dict.get("attributes", {}).get("upload_date")
        self.ai_translated = data_dict.get("attributes", {}).get("ai_translated")
        self.machine_translated = data_dict.get("attributes", {}).get("machine_translated")
        self.release = data_dict.get("attributes", {}).get("release")
        self.comments = data_dict.get("attributes", {}).get("comments")
        self.legacy_subtitle_id = data_dict.get("attributes", {}).get("legacy_subtitle_id")
        self.uploader_id = data_dict.get("attributes", {}).get("uploader", {}).get("uploader_id")
        self.uploader_name = data_dict.get("attributes", {}).get("uploader", {}).get("name")
        self.uploader_rank = data_dict.get("attributes", {}).get("uploader", {}).get("rank")
        self.feature_id = data_dict.get("attributes", {}).get("feature_details", {}).get("feature_id")
        self.feature_type = data_dict.get("attributes", {}).get("feature_details", {}).get("feature_type")
        self.year = data_dict.get("attributes", {}).get("feature_details", {}).get("year")
        self.title = data_dict.get("attributes", {}).get("feature_details", {}).get("title")
        self.movie_name = data_dict.get("attributes", {}).get("feature_details", {}).get("movie_name")
        self.imdb_id = data_dict.get("attributes", {}).get("feature_details", {}).get("imdb_id")
        self.tmdb_id = data_dict.get("attributes", {}).get("feature_details", {}).get("tmdb_id")
        self.season_number = data_dict.get("attributes", {}).get("feature_details", {}).get("season_number")
        self.episode_number = data_dict.get("attributes", {}).get("feature_details", {}).get("episode_number")
        self.parent_imdb_id = data_dict.get("attributes", {}).get("feature_details", {}).get("parent_imdb_id")
        self.parent_title = data_dict.get("attributes", {}).get("feature_details", {}).get("parent_title")
        self.parent_tmdb_id = data_dict.get("attributes", {}).get("feature_details", {}).get("parent_tmdb_id")
        self.parent_feature_id = data_dict.get("attributes", {}).get("feature_details", {}).get("parent_feature_id")
        self.url = data_dict.get("attributes", {}).get("url")
        self.related_links = data_dict.get("attributes", {}).get("related_links", [])
        self.files = data_dict.get("attributes", {}).get("files", [])

        self.file_id = self.files[0].get("file_id") if self.files else None
        self.file_name = self.files[0].get("file_name") if self.files else None

    class Meta:
        """Meta class for Subtitle."""

        main_field = "release"
