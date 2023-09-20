"""
Convenient File handling utilities.

This module has some file handling functions.
"""

from pathlib import Path


def write(path: Path, content: bytes) -> None:
    """
    Utility function to write bytes to a file Path.

    Args:
        path: The Path of the file.
        content: The content.
    Raises:
        FileNotFoundError if the Path does not exist.
        PermissionError if the filesystem permissions deny the operation.
    """
    path.write_bytes(content)


def delete(path: Path) -> None:
    """
    Utility function to delete a file Path.

    Args:
        path: The Path of the file.

    Raises:
        FileNotFoundError if the Path does not exist.
    """
    path.unlink()


def exists(path: Path) -> bool:
    """
    Utility function to confirm whether a file Path exists or not.

    Args:
        path: The Path of the file.

    Raises:
        PermissionError if the filesystem permissions deny the operation.
    """
    return path.exists()
