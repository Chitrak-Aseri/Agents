import os

import yaml
from dotenv import load_dotenv

load_dotenv()


class Config:
    """A configuration manager that loads and processes YAML configuration files with environment variable substitution."""

    def __init__(self, path="issuer-config.yaml", skip_yaml=False):
        """Initialize the Config instance.

        Args:
            path (str): Path to the YAML configuration file. Defaults to "issuer-config.yaml".
            skip_yaml (bool): If True, initializes with empty config instead of loading from file.
        """
        if skip_yaml:
            self.config = {}
        else:
            with open(path, "r") as f:
                raw = yaml.safe_load(f)
            self.config = self._substitute_env_vars(raw)

    def _substitute_env_vars(self, obj):
        """Recursively substitute environment variables in configuration values.

        Args:
            obj: The configuration object (dict, list, or str) to process.

        Returns:
            The processed object with environment variables substituted.
        """
        if isinstance(obj, dict):
            return {k: self._substitute_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_env_vars(i) for i in obj]
        elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            # Replace ${VAR} pattern with corresponding environment variable
            return os.environ.get(obj[2:-1], "")
        return obj

    def get(self, key, default=None):
        """Get a configuration value by key.

        Args:
            key: The configuration key to retrieve.
            default: Default value to return if key is not found.

        Returns:
            The configuration value or default if key doesn't exist.
        """
        return self.config.get(key, default)
