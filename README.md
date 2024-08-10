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
subtitles = OpenSubtitles("MyApp v1.0.0", MY_API_KEY)

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

## Using the CLI

The library is accessible through the CLI, offering various options.
To view all available commands, use the following:

```bash
$> ost -h
positional arguments:
  {set-cred,show-cred,search,download}
    set-cred            Set the API key, username and password in the config file.
    show-cred           Show the username and password in the config file.
    search              Search for subtitles by various criteria.
    download            Download a subtitle by query, file-id or movie-hash.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the configuration file
  -v, --verbose         Increase verbosity level
```

Before executing CLI commands, set your opensubtitles user credentials using the set-cred command:

```bash
$> ost set-cred
Enter your API key (leave blank to keep existing):
Enter your username (leave blank to keep existing):
Enter your password (leave blank to keep existing):
Credentials set successfully!
```

Credentials are stored in the configuration file.
Now you can use CLI commands. For instance, to search for subtitles:

```bash
$> ost search --query "The Matrix"
+----+---------------------------+----------+---------+------------------------------------------------------------------------+
| #  | title                     | imdb-id  | file-id | file-name                                                              |
+----+---------------------------+----------+---------+------------------------------------------------------------------------+
| 1  | The Matrix                | 133093   | 4461104 | The.Matrix.1999.720p.HDDVD.DTS.x264-ESiR.ENG                           |
| 2  | The Matrix                | 133093   | 4477776 | The.Matrix.1999.Subtitles.YIFY                                         |
| 3  | The Matrix                | 133093   | 4465191 | The.Matrix.1999.BluRay.1080p.x264.DTS-WiKi.ENG                         |
| 4  | The Matrix                | 133093   | 4483524 | The.Matrix.1999.1080p.BrRip.x264.YIFY.en                               |
| 5  | The Matrix                | 133093   | 4480638 | The.Matrix.1999.1080p.BluRay.x264-CtrlHD.eng-sdh                       |
```

To download subtitles, use the download command with the specified file-id:

```bash
$> ost download --file-id 4461104
```

By default, the output file name will be the file ID.
You can customize the output file name with the --output option:

```bash
$> ost download --file-id 4461104 --output my_subtitles.srt
```

You can easily download subtitles for a local file using the CLI.
The command will automatically search for the hash and download the first result.
For example, This following command will download the subtitle for "mymovie.mp4" and save it as "mymovie.srt".

```bash
$> ost download --file mymovie.mp4
```

You can combine search and download in a single command:

```bash
$> ost download --query "The Matrix"
```

By default, the output file name will be based on the first search result.
To specify a custom output file name, use the --output argument:

```bash
$> ost download --query "The Matrix" --output my_subtitles.srt
```

## Running Tests

To execute the unit tests, use the following command:

```
python -m unittest
```

Make sure you have the necessary dependencies installed and a valid Python environment set up before running the tests.

## Contributing

Contributions to this project are welcome. If you'd like to contribute, please follow these guidelines:

1. Open an issue to discuss your proposed changes before submitting a pull request.
2. Ensure that your code adheres to the project's coding standards.
3. Write tests for your code and make sure existing tests pass.
4. Document your changes thoroughly, including updating this README if necessary.

Thank you for your interest in improving this project!
