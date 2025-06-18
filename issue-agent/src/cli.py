import argparse
import os


def parse_args():
    """Parse command line arguments for the script.

    Returns:
        argparse.Namespace: Parsed arguments with the following attributes:
            --src (str): Source directory path (default: "data")
            --provider (str): Required provider name
            --model_name (str): Required model name
            --api_key (str): Required API key
            --api_base (str): Optional API base URL (default: None)
            --skip-yaml (bool): Whether to skip YAML processing (default: True)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=str, default="data")
    parser.add_argument("--provider", type=str, required=True)
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--api_key", type=str, required=True)
    parser.add_argument("--api_base", type=str, default=None)
    parser.add_argument("--skip-yaml", type=bool, default=True)
    return parser.parse_args()
