# utils/config_loader.py

"""Module for loading and processing configuration files with environment variable substitution."""

import os
import yaml
import re
from dotenv import load_dotenv

load_dotenv()

env_var_pattern = re.compile(r'\${(\w+)}')

def replace_env_vars(value: str) -> str:
    """Replace environment variable placeholders in a string with their actual values.
    
    Args:
        value: String potentially containing environment variable placeholders (${VAR_NAME}).
    
    Returns:
        String with placeholders replaced by environment variable values.
    """
    return env_var_pattern.sub(lambda match: os.getenv(match.group(1), ""), value)

def substitute_env_vars(obj):
    """Recursively substitute environment variables in a data structure.
    
    Args:
        obj: Data structure (dict, list, str) to process.
    
    Returns:
        New data structure with all string values processed for env var substitution.
    """
    if isinstance(obj, dict):
        return {k: substitute_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [substitute_env_vars(i) for i in obj]
    elif isinstance(obj, str):
        return replace_env_vars(obj)
    else:
        return obj

def load_config(path: str = "ai-reviewer.yaml", overrides: dict = None):
    """Load and process a YAML configuration file with optional overrides.
    
    Args:
        path: Path to YAML configuration file.
        overrides: Dictionary of values to override in the loaded config.
    
    Returns:
        Dictionary containing the merged configuration with environment variables substituted
        and overrides applied.
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)
        config = substitute_env_vars(data)

    overrides = overrides or {}

    # Apply overrides only if the value is not None
    for key, value in overrides.items():
        if value is not None:
            config[key] = value

    return config