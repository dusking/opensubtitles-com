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


def write(path: Path, content: bytes) -> None:
    """Write bytes to a file Path.

    Args:
        path: The Path of the file.
        content: The content.
    Raises:
        FileNotFoundError if the Path does not exist.
        PermissionError if the filesystem permissions deny the operation.
    """
    path.write_bytes(content)


def delete(path: Path) -> None:
    """Delete a file Path.

    Args:
        path: The Path of the file.

    Raises:
        FileNotFoundError if the Path does not exist.
    """
    path.unlink()


def exists(path: Path) -> bool:
    """Confirm whether a file Path exists or not.

    Args:
        path: The Path of the file.

    Raises:
        PermissionError if the filesystem permissions deny the operation.
    """
    return path.exists()
