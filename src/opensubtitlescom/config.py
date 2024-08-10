"""
This file is part of Opensubtitles API wrapper.

Opensubtitles API is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published by the Massachusetts
Institute of Technology.

For full details, please see the LICENSE file located in the root
directory of this project.
"""
import os
import json
import logging
from typing import Optional
from pathlib import Path


logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = "~/.config/opensubtitlescom/config.json"


class Config:
    """Represents the configuration for the OpenSubtitles CLI."""

    def __init__(self, path: Optional[Path] = None):
        """Initialize the Config object.

        Args:
            path (Path): The path to the configuration file.

        Note:
            If the configuration file exists, the class is initialized with its content.
            If not, the class creates the necessary directory structure for the configuration file.
        """
        self._path: Path = (Path(path or DEFAULT_CONFIG_PATH)).expanduser()
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.api_key: Optional[str] = None
        self.language: str = "en"

        if self._path.exists():
            data = json.loads(self._path.read_text())
            self.__dict__.update(data)

    def verify_config_dir(self):
        """Verify the existence of the directory specified by self._path.

        If the directory does not exist, attempts to create it.

        Returns:
            bool: True if the directory exists or is successfully created, False otherwise.
        """
        if self._path.exists():
            return True
        path = self._path.parent
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except OSError as e:
            if e.errno == 30:
                logger.error(f"Error: {e}. Check if the file system is read-only or permissions are insufficient.")
            else:
                logger.error(f"Error: {e}")
            return False

    def save(self):
        """Save the configuration to the specified file."""
        if not self.verify_config_dir():
            logger.error("Failed to save config.")
            return False
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        self._path.write_text(json.dumps(data, indent=4))
        return True
