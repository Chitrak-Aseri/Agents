import os
from string import Template

import yaml


def load_config(config_path="issuer-config.yaml"):
    with open(config_path, "r") as f:
        raw = f.read()

    substituted = Template(raw).substitute(os.environ)
    return yaml.safe_load(substituted)
