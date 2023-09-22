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


# install_reqs = parse_requirements("requirements.txt")
# requirements = [str(ir) for ir in install_reqs]
requirements = []

version = "0.0.4"

setup_kwargs = dict(
    name="opensubtitlescom",
    version=version,
    license="MIT",
    platforms="All",
    description="OpenSubtitles.com new REST API",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    keywords=["opensubtitles"],
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.7",
    url="https://github.com/dusking/opensubtitles-com.git",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

setup(**setup_kwargs)
