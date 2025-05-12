import csv
import os
import re
from argparse import ArgumentParser

from config import OUTPUT_DIR


def parse_args():
    parser = ArgumentParser(description="Process raw call graph data")
    parser.add_argument(
        "-p",
        "--program",
        type=str,
        required=True,
        help="Name of the program to process (e.g., 'jython', 'javac', etc.)",
    )
    return parser.parse_args()


def glob_to_regex(pattern):
    # Escape special regex characters
    pattern = re.escape(pattern)
    # Replace escaped glob wildcards with regex equivalents
    pattern = pattern.replace(r"\*\*", ".*")  # '**' -> '.*'
    pattern = pattern.replace(r"\*", "[^.]*")  # '*' -> '[^.]*'
    # Match the entire string
    return "^" + pattern + "$"


def get_methods(combined_csv_path: str, config_path: str) -> set:
    # Read the configuration file
    with open(config_path) as config_file:
        config_lines = config_file.readlines()

    # Extract INSTRUMENT_CLASSES value
    instrument_classes_line = next(
        (line for line in config_lines if line.startswith("INSTRUMENT_CLASSES=")), None
    )
    if not instrument_classes_line:
        raise ValueError("INSTRUMENT_CLASSES not found in the configuration file.")

    # Remove the key and any surrounding quotes
    instrument_classes_value = (
        instrument_classes_line.split("=", 1)[1].strip().strip("'\"")
    )

    # Split multiple patterns if separated by commas
    patterns = [
        pattern.strip()
        for pattern in instrument_classes_value.split(",")
        if pattern.strip()
    ]

    # Convert glob patterns to regular expressions
    regex_patterns = [re.compile(glob_to_regex(pat)) for pat in patterns]

    matched_methods = set()

    # Read and filter the CSV file
    with open(combined_csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for column in ["method", "target"]:
                value = row.get(column, "")
                if any(regex.match(value) for regex in regex_patterns):
                    matched_methods.add(value)

    return matched_methods


def write_methods_to_file(methods: set, output_path: str):
    with open(output_path, "w") as f:
        for method in sorted(methods):
            f.write(f"{method}\n")


def main():
    args = parse_args()
    program = args.program

    # Get the paths to the call graphs
    output_dir = os.path.join(OUTPUT_DIR, program)
    os.makedirs(output_dir, exist_ok=True)
    combined_csv_path = os.path.join(output_dir, "combined.csv")
    config_path = os.path.join("../testing/projects", program, ".env")
    methods_output_path = os.path.join(output_dir, "methods.txt")

    # Get the methods from the CSV file
    methods = get_methods(combined_csv_path, config_path)

    # Write the matched methods to methods.txt
    write_methods_to_file(methods, methods_output_path)
