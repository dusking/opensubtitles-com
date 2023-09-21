"""
Copyright (c) 2023 Omer Duskin.

This file is part of Opensubtitles API wrapper.

Opensubtitles API is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published by the Massachusetts
Institute of Technology.

For full details, please see the LICENSE file located in the root
directory of this project.

This is the test module for the opensubtitles wrapper.
"""

import unittest
from unittest.mock import patch, Mock

from opensubtitlescom import OpenSubtitles
from opensubtitlescom.exceptions import OpenSubtitlesException


class TestOpenSubtitlesAPI(unittest.TestCase):
    """Test cases for the OpenSubtitlesAPI class."""

    def setUp(self):
        """Set up test environment."""
        mock_download_client = Mock()
        mock_download_client.get.return_value = bytes()

        self.mock_download_client = mock_download_client
        self.api = OpenSubtitles("api-key")
        self.api.download_client = self.mock_download_client

    @patch("opensubtitlescom.OpenSubtitles.send_api")
    def test_successful_login(self, mock_login_req):
        """Test successful login."""
        # Mock the 'login_request' method to simulate a successful login response
        valid_response = {
            "user": {
                "allowed_translations": 1,
                "allowed_downloads": 20,
                "level": "Sub leecher",
                "user_id": 123456,
                "ext_installed": False,
                "vip": False,
            },
            "token": "thegeneratedapitoken",
            "status": 200,
        }
        mock_login_req.return_value = valid_response

        # Replace these with any values since the network request is mocked
        username = "mocked_username"
        password = "mocked_password"

        # Attempt to log in
        login_response = self.api.login(username, password)

        # Assert that the response is as expected
        assert login_response == valid_response

    @patch("opensubtitlescom.OpenSubtitles.send_api")
    def test_failed_login(self, mock_login_req):
        """Test failed login."""
        # Mock the 'login_request' method to simulate a failed login response
        mock_login_req.return_value = {"error": "Unauthorized"}
        mock_login_req.side_effect = OpenSubtitlesException("Failed with HTTP Error: 401 Client Error: Unauthorized")

        # Replace these with any values since the network request is mocked
        username = "mocked_invalid_username"
        password = "mocked_invalid_password"

        # Attempt to log in and catch OpenSubtitlesException
        try:
            self.api.login(username, password)
        except OpenSubtitlesException as e:
            # Assert that the error message contains "Unauthorized"
            assert "Unauthorized" in str(e)

    @patch("opensubtitlescom.OpenSubtitles.send_api")
    def test_search_response_parsing(self, mock_login_req):
        """Test parsing of search response."""
        # Mock the search response data
        search_response_data = {
            "total_pages": 5,
            "total_count": 100,
            "per_page": 20,
            "page": 1,
            "data": [
                {"id": "7061050", "type": "subtitle", "attributes": {"subtitle_id": "7061050", "language": "en"}},
                {"id": "7061050", "type": "subtitle", "attributes": {"subtitle_id": "7061050", "language": "en"}},
            ],
        }
        mock_login_req.return_value = search_response_data

        # Call the search method with any parameters you want to test
        search_result = self.api.search(query="example_query")

        # Perform assertions to verify the parsing of the response
        assert search_result.total_pages == 5
        assert search_result.total_count == 100
        assert search_result.per_page == 20
        assert search_result.page == 1
        assert len(search_result.data) == 2  # Assuming 2 items in data
