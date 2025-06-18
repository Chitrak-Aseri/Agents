import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=str, default="data")
    parser.add_argument("--provider", type=str, required=True)
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--api_key", type=str, required=True)
    parser.add_argument("--api_base", type=str, default=None)
    parser.add_argument("--skip-yaml", type=bool, default=True)
    return parser.parse_args()
