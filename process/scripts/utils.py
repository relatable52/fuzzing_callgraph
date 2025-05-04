import json
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--program",
        type=str,
        required=True,
        help="Name of the program to be process.",
    )
    return parser.parse_args()


def read_json(file_path: str):
    with open(file_path) as f:
        data = json.load(f)
    return data
