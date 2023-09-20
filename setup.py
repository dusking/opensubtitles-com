from typing import List
from setuptools import setup, find_packages

from version_helpers import version

def parse_requirements(filename) -> List[str]:
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_reqs = parse_requirements("requirements.txt")
requirements = [str(ir) for ir in install_reqs]

setup_kwargs = dict(
    name="opensubtitles",
    version=version(),
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
