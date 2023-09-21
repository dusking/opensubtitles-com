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


class DownloadClient:
    """A client to download files URLs with."""

    def __init__(self):
        """Initialize the DownloadClient object."""
        pass

    def get(self, url: str) -> bytes:
        """Download the subtitle referenced by url.

        Args:
            url: The url of the subtitle to download.

        Returns:
            The subtitles data in bytes.
        """
        download_remote_file = requests.get(url)

        return download_remote_file.content
