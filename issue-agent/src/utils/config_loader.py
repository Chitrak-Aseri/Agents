import os
import yaml
from string import Template

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        raw = f.read()

    substituted = Template(raw).substitute(os.environ)
    return yaml.safe_load(substituted)
