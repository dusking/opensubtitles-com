"""
Copyright (c) 2023 Omer Duskin.

This file is part of Opensubtitles API wrapper.

Opensubtitles API is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published by the Massachusetts
Institute of Technology.

For full details, please see the LICENSE file located in the root
directory of this project.
"""

import requests
from typing import Optional


class DownloadClient:
    """A client to download files URLs with."""

    def __init__(self, user_agent: str, api_key: str, token: Optional[str] = None):
        """Initialize the DownloadClient object.

        Args:
            user_agent: The user agent string to use in requests.
            api_key: The API key for authentication.
            token: Optional authorization token.
        """
        self.user_agent = user_agent
        self.api_key = api_key
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent,
            "API-Key": api_key,
        })
        if token:
            self.session.headers.update({
                "authorization": token
            })

    def get(self, url: str) -> bytes:
        """Download the subtitle referenced by url.

        Args:
            url: The url of the subtitle to download.

        Returns:
            The subtitles data in bytes.
        """
        download_remote_file = self.session.get(url)

        return download_remote_file.content
