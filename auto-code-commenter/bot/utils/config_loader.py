# bot/utils/config_loader.py
import os
import yaml
import re
from dotenv import load_dotenv

"""Module for loading and processing configuration files with environment variable substitution."""

# Load environment variables from .env file
load_dotenv()

# Regex pattern to match ${ENV_VAR} in configuration values
env_var_pattern = re.compile(r'\${(\w+)}')

def replace_env_vars(value: str) -> str:
    """Replace environment variable placeholders (${VAR}) with their actual values.
    
    Args:
        value: String potentially containing environment variable placeholders
        
    Returns:
        String with placeholders replaced by environment variable values
    """
    return env_var_pattern.sub(lambda match: os.getenv(match.group(1), ""), value)

def substitute_env_vars(obj):
    """Recursively process a configuration object to substitute environment variables.
    
    Handles dictionaries, lists, and strings. Other types are returned unchanged.
    
    Args:
        obj: Configuration object (dict, list, str, or other)
        
    Returns:
        Processed object with all environment variables substituted
    """
    if isinstance(obj, dict):
        return {k: substitute_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [substitute_env_vars(i) for i in obj]
    elif isinstance(obj, str):
        return replace_env_vars(obj)
    else:
        return obj

def load_config(path: str = "config.yaml"):
    """Load and process a YAML configuration file with environment variable substitution.
    
    Args:
        path: Path to the YAML configuration file (default: 'config.yaml')
        
    Returns:
        Dictionary containing the processed configuration with environment variables resolved
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)
        return substitute_env_vars(data)