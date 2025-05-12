import csv
import os
import re
from argparse import ArgumentParser

import javalang
from config import OUTPUT_DIR


def parse_args():
    parser = ArgumentParser(description="Process raw call graph data")
    parser.add_argument(
        "-p",
        "--program",
        type=str,
        required=True,
        help="Name of the program to process",
    )
    return parser.parse_args()


def get_methods(combined_csv_path: str, config_path: str) -> set:
    with open(config_path) as config_file:
        config_lines = config_file.readlines()

    instrument_classes_line = next(
        (line for line in config_lines if line.startswith("INSTRUMENT_CLASSES=")), None
    )
    if not instrument_classes_line:
        raise ValueError("INSTRUMENT_CLASSES not found in the configuration file.")

    instrument_classes_value = (
        instrument_classes_line.split("=", 1)[1].strip().strip("'\"")
    )

    # Convert class path to regex
    pattern = (
        instrument_classes_value.replace(".", "/")
        .replace("**", ".*")
        .replace("*", "[^/]*")
    )

    matched_methods = set()
    with open(combined_csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for column in ["method", "target"]:
                value = row.get(column, "")
                if re.search(pattern, value):
                    matched_methods.add(value)

    return matched_methods


def write_methods_to_file(methods: set, output_path: str):
    with open(output_path, "w") as f:
        for method in sorted(methods):
            f.write(f"{method}\n")


def main():
    args = parse_args()
    program = args.program

    output_dir = os.path.join(OUTPUT_DIR, program)
    os.makedirs(output_dir, exist_ok=True)
    combined_csv_path = os.path.join(output_dir, "combined.csv")
    config_path = os.path.join("../testing/projects", program, ".env")
    methods_output_path = os.path.join(output_dir, "methods.txt")

    methods = get_methods(combined_csv_path, config_path)

    print(f"Found {len(methods)} matched methods.")
    write_methods_to_file(methods, methods_output_path)


if __name__ == "__main__":
    main()
