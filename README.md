# Python OpenSubtitles.com API Wrapper

![GitHub](https://img.shields.io/github/license/dusking/opensubtitles-com)
![PyPI](https://img.shields.io/pypi/v/opensubtitlescom)
![Python](https://img.shields.io/pypi/pyversions/opensubtitlescom)

A Python wrapper for the OpenSubtitles REST API, providing easy access to subtitle data.
This library allows you to interact with OpenSubtitles.com programmatically,
making it simple to search for and download subtitles for your favorite movies and TV shows.

## Installation

You can install the package using `pip` directly from PyPI or by cloning the repository from GitHub.

**Install from PyPI:**

```bash
pip install opensubtitlescom
```

**Install from GitHub (latest development version):**

```bash
pip install git+ssh://git@github.com/dusking/opensubtitles-com.git --upgrade
```

## Usage

Using this wrapper is straightforward.
It follows the OpenSubtitles API documentation closely and converts responses into Python objects.
Here's an example of how to use it:

```python
from opensubtitlescom import OpenSubtitles

# Initialize the OpenSubtitles client
subtitles = OpenSubtitles(MY_API_KEY, "MyApp v1.0.0")

# Log in (retrieve auth token)
subtitles.login(MY_USERNAME, MY_PASSWORD)

# Search for subtitles
response = subtitles.search(query="breaking bad", season_number=1, episode_number=1, languages="en")

# Convert the response to a Python dictionary
response_dict = response.to_dict()
print(response_dict)

# Convert the response to a Json format
response_json = response.to_json()
print(response_json)

# Get first response subtitles
srt = subtitles.download_and_parse(response.data[0])
```

Here's another simple example:
```python
# Get latest uploaded subtitles
latest_uploads = subtitles.discover_latest()

# Convert the response to a Python dictionary
latest_uploads_dict = latest_uploads.to_dict()
```


For more information on available methods and options,
refer to the [OpenSubtitles API documentation](https://api.opensubtitles.com/).

## Command Line Interface (CLI)

### Installation

Ensure you've followed the library installation steps outlined at the top of this README. 
Once the library is installed, you can access the `ost` command-line interface.

### Usage

To explore the available options, run:

```bash
ost --help
```

Before utilizing the library, set up the credentials configuration file using:

```bash
ost set-cred
```

Searching for existing subtitles is straightforward:

```bash
ost search --query fightclub
```

Downloading existing subtitles can be done in two ways:

If you have the file ID (obtained from the search response):

```bash
ost download --file-id 1234567
```

If you have the movie file and prefer to search by the movie hash:

```bash
ost download --file-path movie
```

Feel free to explore additional functionalities and options using the provided --help command 
or refer to the documentation for more details.

## Running Tests

To execute the unit tests, use the following command:

```
$ python -m unittest
```

Make sure you have the necessary dependencies installed and a valid Python environment set up before running the tests.

## Contributing

Contributions to this project are welcome. If you'd like to contribute, please follow these guidelines:

1. Open an issue to discuss your proposed changes before submitting a pull request.
2. Ensure that your code adheres to the project's coding standards.
3. Write tests for your code and make sure existing tests pass.
4. Document your changes thoroughly, including updating this README if necessary.

Thank you for your interest in improving this project!
