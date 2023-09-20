"""
This module contains functions to use for automated versioning
"""

VERSION_FILE = "VERSION"

PATCH = 10
MINOR = 20
MAJOR = 30


def get_new_version(current_version, level=PATCH):
    """
    This function applies the version bumping on the given version
    :param current_version: the existing version
    :type current_version: str
    :param level: bump level
    :type level: int
    :return: updated version
    :rtype: str
    """
    parts = current_version.split(".")
    major_index, minor_index, patch_index = [int(x) for x in parts]
    if level == MAJOR:
        major_index, minor_index, patch_index = major_index + 1, 0, 0
    if level == MINOR:
        minor_index, patch_index = minor_index + 1, 0
    if level == PATCH:
        patch_index = patch_index + 1
    return f"{major_index}.{minor_index}.{patch_index}"


def bump_version(level=PATCH):
    """
    This function bumps the version file
    :param level: bump level
    :type level: int
    """
    current = version()
    with open(VERSION_FILE, "w") as file:
        new = get_new_version(current_version=current, level=level)
        file.write(new)


def patch():
    """This function bumps a patch version"""
    bump_version(PATCH)


def minor():
    """This function bumps a minor version"""
    bump_version(MINOR)


def major():
    """This function bumps a major version"""
    bump_version(MAJOR)


def version():
    """
    This function gets the package version
    :return: version
    :rtype: str
    """
    with open(VERSION_FILE) as file:
        return file.readline()
