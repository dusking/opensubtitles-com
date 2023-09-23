"""
Copyright (c) 2023 Omer Duskin.

This file is part of Opensubtitles API wrapper.

Opensubtitles API is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published by the Massachusetts
Institute of Technology.

For full details, please see the LICENSE file located in the root
directory of this project.
"""

from pathlib import Path


class FileUtils:
    """Expose file utilities functions."""

    def __init__(self, path: Path):
        """Initialize the File object.

        Args:
            path: The Path of the file.
        """
        self.path = path

    def write(self, content: bytes) -> None:
        """Write bytes to a file Path.

        Args:
            content: The content of the file to be written.
        Raises:
            FileNotFoundError if the Path does not exist.
            PermissionError if the filesystem permissions deny the operation.
        """
        self.path.write_bytes(content)

    def delete(self) -> None:
        """Delete a file Path.

        Raises:
            FileNotFoundError if the Path does not exist.
        """
        self.path.unlink()

    def exists(self) -> bool:
        """Confirm whether a file Path exists or not.

        Raises:
            PermissionError if the filesystem permissions deny the operation.
        """
        return self.path.exists()
