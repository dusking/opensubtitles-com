from pathlib import Path
import json
import logging
import typing as t

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, path: Path):
        self._path: Path = path.expanduser()
        self.username: t.Optional[str] = None
        self.password: t.Optional[str] = None
        self.langauge: str = "en"

        if self._path.exists():
            d = json.loads(self._path.read_text())
            self.__dict__.update(d)

    def save(self):
        """Save the configuration to the specified file."""
        if not self.verify_config_dir():
            logger.error(f"Failed to save config.")
            return False
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        self._path.write_text(json.dumps(data, indent=4))
        return True

    def verify_config_dir(self):
        """Verify the existence of the directory specified by self._path.

        If the directory does not exist, attempts to create it.

        Returns:
            bool: True if the directory exists or is successfully created, False otherwise.
        """
        if self._path.exists():
            return True
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            return True
        except OSError as e:
            if e.errno == 30:
                logger.error(f"Error: {e}. Check if the file system is read-only or permissions are insufficient.")
            else:
                logger.error(f"Error: {e}")
            return False
