import os

import yaml
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self, path="issuer-config.yaml", skip_yaml=False):
        if skip_yaml:
            self.config = {}
        else:
            with open(path, "r") as f:
                raw = yaml.safe_load(f)
            self.config = self._substitute_env_vars(raw)

    def _substitute_env_vars(self, obj):
        if isinstance(obj, dict):
            return {k: self._substitute_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_env_vars(i) for i in obj]
        elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            return os.environ.get(obj[2:-1], "")
        return obj

    def get(self, key, default=None):
        return self.config.get(key, default)
