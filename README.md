# Python OpenSubtitles API Wrapper

This is a Python wrapper to the OpenSubtitles REST API,
As documented in https://opensubtitles.stoplight.io/

## Installation

You can clone and install it locally or use direct install from GitHub.

```bash
pip install git+ssh://git@github.com/dusking/opensubtitles-api.git --upgrade
```

## Usage

The following is a simple example:

```python
from opensubtitles import OpenSubtitles

subtitles = OpenSubtitles(MY_API_KEY)
subtitles.login(MY_USERNAME, MY_PASSWORD)

response = subtitles.search(query="one of us is lying", season_number=1, episode_number=1, languages="en")
subtitles.download_and_save(response.data[0])
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
