import unittest
from unittest.mock import patch, call, Mock, MagicMock

from opensubtitles import OpenSubtitles
from opensubtitles.exceptions import OpenSubtitlesException


class TestOpenSubtitlesAPI(unittest.TestCase):

    def setUp(self):
        mock_download_client = Mock()
        mock_download_client.get.return_value = bytes()

        self.mock_download_client = mock_download_client
        self.api = OpenSubtitles("api-key")
        self.api.download_client = self.mock_download_client

    @patch('opensubtitles.OpenSubtitles.send_api')
    def test_successful_login(self, mock_login_req):
        # Mock the 'login_request' method to simulate a successful login response
        valid_response = {'user': {'allowed_translations': 1,
                                   'allowed_downloads': 20,
                                   'level': 'Sub leecher',
                                   'user_id': 123456,
                                   'ext_installed': False,
                                   'vip': False},
                          'token': 'thegeneratedapitoken',
                          'status': 200}
        mock_login_req.return_value = valid_response

        # Replace these with any values since the network request is mocked
        username = "mocked_username"
        password = "mocked_password"

        # Attempt to log in
        login_response = self.api.login(username, password)

        # Assert that the response is as expected
        self.assertEqual(login_response, valid_response)

    @patch('opensubtitles.OpenSubtitles.send_api')
    def test_failed_login(self, mock_login_req):
        # Mock the 'login_request' method to simulate a failed login response
        mock_login_req.return_value = {"error": "Unauthorized"}
        mock_login_req.side_effect = OpenSubtitlesException("Failed with HTTP Error: 401 Client Error: Unauthorized")

        # Replace these with any values since the network request is mocked
        username = "mocked_invalid_username"
        password = "mocked_invalid_password"

        # Attempt to log in and expect an OpenSubtitlesException
        with self.assertRaises(OpenSubtitlesException) as context:
            self.api.login(username, password)

        # Assert that the error message contains "Unauthorized"
        self.assertTrue("Unauthorized" in str(context.exception))

    @patch('opensubtitles.OpenSubtitles.send_api')
    def test_search_response_parsing(self, mock_login_req):
        # Mock the search response data
        search_response_data = {
            'total_pages': 5,
            'total_count': 100,
            'per_page': 20,
            'page': 1,
            'data': [
                {'id': '7061050', 'type': 'subtitle', 'attributes': {
                    "subtitle_id": "7061050",
                    "language": "en"
                }},
                {'id': '7061050', 'type': 'subtitle', 'attributes': {
                    "subtitle_id": "7061050",
                    "language": "en"
                }},
            ]
        }
        mock_login_req.return_value = search_response_data

        # Call the search method with any parameters you want to test
        search_result = self.api.search(query="example_query")

        # Perform assertions to verify the parsing of the response
        self.assertEqual(search_result.total_pages, 5)
        self.assertEqual(search_result.total_count, 100)
        self.assertEqual(search_result.per_page, 20)
        self.assertEqual(search_result.page, 1)
        self.assertEqual(len(search_result.data), 2)  # Assuming 2 items in data
