"""
This is the setup module for the opensubtitles wrapper.

It contains the configuration and metadata required for packaging and distributing the project.
"""

from typing import List
from setuptools import setup, find_packages


def parse_requirements(filename) -> List[str]:
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_reqs = parse_requirements("requirements.txt")
requirements = [str(ir) for ir in install_reqs]

setup_kwargs = dict(
    name="opensubtitlescom",
    version="0.0.1",
    license="LICENSE",
    platforms="All",
    description="OpenSubtitles.com new REST API",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
)

setup(**setup_kwargs)
