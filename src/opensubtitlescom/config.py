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
from typing import Optional
from pathlib import Path


DEFAULT_CONFIG_PATH = "~/.config/opensubtitlescom/cli.json"


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
        self.api_key: Optional[str] = None
        self.app_name: Optional[str] = None
        self.app_version: Optional[str] = "0.0.1"
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.langauge: str = "en"

        if self._path.exists():
            data = json.loads(self._path.read_text())
            self.__dict__.update(data)
        else:
            os.makedirs(self._path.parent, exist_ok=True)

    def save(self):
        """Save the configuration to the specified file."""
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        self._path.write_text(json.dumps(data, indent=4))

    @property
    def app_full_name(self):
        """Get the full name of the application including version."""
        return f"{self.app_name} v{self.app_version}"
