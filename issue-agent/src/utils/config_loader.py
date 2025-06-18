import os
from string import Template

import yaml


def load_config(config_path="issuer-config.yaml"):
    """Load and parse a YAML configuration file with environment variable substitution.

    Args:
        config_path (str, optional): Path to the YAML configuration file. 
            Defaults to "issuer-config.yaml".

    Returns:
        dict: Parsed configuration data with environment variables substituted.
    """
    with open(config_path, "r") as f:
        raw = f.read()

    # Substitute environment variables using string.Template
    substituted = Template(raw).substitute(os.environ)
    return yaml.safe_load(substituted)