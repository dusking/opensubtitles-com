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

import os
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from opensubtitlescom import OpenSubtitles
from opensubtitlescom.file_utils import FileUtils
from opensubtitlescom.exceptions import OpenSubtitlesException
from opensubtitlescom.srt import parse


class TestOpenSubtitlesAPI(unittest.TestCase):
    """Test cases for the OpenSubtitlesAPI class."""

    def setUp(self):
        """Set up test environment."""
        mock_download_client = Mock()
        mock_download_client.get.return_value = bytes()

        self.mock_download_client = mock_download_client
        self.api = OpenSubtitles("api-key", "MyAp v1.0.0")
        self.api.download_client = self.mock_download_client

        self.api.downloads_dir = "test_downloads"
        os.makedirs(self.api.downloads_dir, exist_ok=True)

    def tearDown(self):
        """
        Clean up the test downloads directory by removing all files and the directory itself.

        This method is automatically called after each test case to ensure that the test environment is clean.
        """
        for file in Path(self.api.downloads_dir).iterdir():
            if file.is_file():
                file.unlink()
        os.rmdir(self.api.downloads_dir)

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

    def test_save_content_locally_with_filename(self):
        """
        Test saving content with a specified filename.

        This test ensures that the function correctly saves content to a file with a specified filename.
        """
        content = b"This is some test content."
        filename = "test_file.srt"

        result = self.api.save_content_locally(content, filename)

        assert Path(result).exists()
        assert Path(result).name == filename
        assert content == Path(result).read_bytes()

    def test_save_content_locally_without_filename(self):
        """
        Test saving content without a specified filename.

        This test ensures that the function correctly saves content to a file with a generated filename (UUID-based).
        """
        content = b"This is some test content."

        result = self.api.save_content_locally(content)

        assert Path(result).exists()
        assert result.endswith(".srt")
        assert content == Path(result).read_bytes()

    def test_get_hash(self):
        """
        Test the get_hash method by creating a fake MOV file and comparing the calculated hash with the expected hash.

        Steps:
        1. Create a Path object for a temporary fake MOV file.
        2. Create a fake file of size 65536 * 2 and write all zeros to it.
        3. Call the get_hash method on the fake file and calculate the actual hash.
        4. Compare the actual hash with the expected hash "0000000000020000".

        This test ensures that the get_hash method correctly calculates the hash for the fake file.
        """
        # Create Path for temporary fake mov file
        temp_file_path = Path(self.api.downloads_dir) / "fake_file_2.mov"

        # Create a fake file of size 65536 * 2
        file_size = 65536 * 2
        with open(temp_file_path, "wb") as fake_file:
            fake_file.write(b"\x00" * file_size)

        # Call the get_hash method and compare the result with the expected hash
        actual_hash = FileUtils(temp_file_path).get_hash()
        assert "0000000000020000" == actual_hash

    def test_get_md5(self):
        """
        Test the get_md5 method by creating a fake file and comparing the calculated MD5 hash with the expected hash.

        Steps:
        1. Create a Path object for a temporary fake MOV file.
        2. Create a fake file of size 65536 * 2 and write all zeros to it.
        3. Call the get_md5 method on the fake file and calculate the actual MD5 hash.
        4. Compare the actual MD5 hash with the expected MD5 hash "0dfbe8aa4c20b52e1b8bf3cb6cbdf193".

        This test ensures that the get_md5 method correctly calculates the MD5 hash for the fake file.
        """
        # Create Path for temporary fake mov file
        temp_file_path = Path(self.api.downloads_dir) / "fake_file_1.mov"

        # Create a fake file of size 65536 * 2
        file_size = 65536 * 2
        with open(temp_file_path, "wb") as fake_file:
            fake_file.write(b"\x00" * file_size)

        actual_md5 = FileUtils(temp_file_path).get_md5()
        assert "0dfbe8aa4c20b52e1b8bf3cb6cbdf193" == actual_md5

    def test_download_and_parse(self):
        """Test download and parse function."""
        # Create a mock download response (replace with your sample SRT content)
        mock_srt_content = (
            b"1\n00:00:10,500 --> 00:00:14,000\nSubtitle Line 1\n\n2\n00:00:15,000 --> 00:00:18,500\nSubtitle Line 2\n"
        )

        # Create a mock OpenSubtitles instance
        self.api.download = Mock(return_value=mock_srt_content)

        # Call the download_and_parse function with any arguments you want to test
        subtitles = self.api.download_and_parse(file_id="sample_file_id", sub_format="srt")

        # Assert that the mock download function was called with the expected arguments
        self.api.download.assert_called_with(file_id="sample_file_id", sub_format="srt")

        # Define the expected parsed subtitles (adjust according to your mock SRT content)
        expected_subtitles = list(parse(self.api.bytes_to_str(mock_srt_content)))

        # Assert that the parsed subtitles match the expected result
        assert subtitles == expected_subtitles
