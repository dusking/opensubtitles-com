"""
Copyright (c) 2023 Omer Duskin.

This file is part of Opensubtitles API wrapper.

Opensubtitles API is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published by the Massachusetts
Institute of Technology.

For full details, please see the LICENSE file located in the root
directory of this project.
"""
import struct
import hashlib

from pathlib import Path

from .exceptions import OpenSubtitlesFileException


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

    def get_hash(self):
        """Return the hash code of a file.

        Original from: https://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes.

        Returns:
            - hash - hash code of a file
        """
        if not self.exists():
            raise OpenSubtitlesFileException(f"File not exists: {self.path}")
        size = self.path.stat().st_size
        longlongformat = "q"  # long long
        bytesize = struct.calcsize(longlongformat)

        if int(size) < 65536 * 2:
            raise OpenSubtitlesFileException("SizeError")

        with open(self.path, "rb") as file_obj:
            hash = size
            for _ in range(65536 // bytesize):
                buffer = file_obj.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

            file_obj.seek(max(0, int(size) - 65536), 0)
            for _ in range(65536 // bytesize):
                buffer = file_obj.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF

        return str("%016x" % hash)

    def get_md5(self):
        """Return the md5 of a file."""
        return hashlib.md5(self.path.read_bytes()).hexdigest()
