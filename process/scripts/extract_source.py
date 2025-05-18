import csv
import json
import os
import re
import subprocess
from argparse import ArgumentParser
from glob import glob

import javalang
from config import CODE_DIR, OUTPUT_DIR, RAW_CALLGRAPH
from parser_utils import extract_source, shorten_jvm_descriptor


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


def get_instrument_pattern(config_path: str) -> str:
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

    # Convert class path pattern to regex
    pattern = (
        instrument_classes_value.replace(".", "/")
        .replace("**", ".*")
        .replace("*", "[^/]*")
    )
    return pattern


def get_jar_path(program: str) -> str:
    jar_dir = os.path.join(RAW_CALLGRAPH, program, "target")
    config_path = os.path.join("../testing/projects", program, "jcg.conf")

    with open(config_path) as config_file:
        config = json.load(config_file)
    cp_list = config.get("cp", [])
    assert len(cp_list) > 0, f"Classpath is empty in {config_path}"

    jar_file = cp_list[0]["path"].strip()[1:]

    jar_path = os.path.join(jar_dir, jar_file)

    if not os.path.exists(jar_path):
        raise FileNotFoundError(f"JAR path {jar_path} does not exist.")
    return jar_path


def get_methods_from_jar(jar_path: str):
    # Run javaq and capture the output
    result = subprocess.run(
        ["./javaq", "--cp", jar_path, "list-methods"],
        check=True,
        capture_output=True,
        text=True,
    )

    matched_methods = set()
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        matched_methods.add(line)

    return matched_methods


def filter_methods_by_pattern(methods: set, pattern: str) -> set:
    filtered_methods = set()
    regex = re.compile(pattern)

    for method in methods:
        # Extract the class name from the method signature
        class_name = method.split(":")[0]
        if regex.match(class_name):
            filtered_methods.add(method)

    return filtered_methods


def write_methods_to_file(methods: set, output_path: str):
    with open(output_path, "w") as f:
        for method in sorted(methods):
            f.write(f"{method}\n")


def write_source_code_to_file(source_code: dict, output_path: str):
    writer = csv.writer(open(output_path, "w", newline=""))
    writer.writerow(["descriptor", "code"])
    for method, code in source_code.items():
        writer.writerow([method, code])


def main():
    args = parse_args()
    program = args.program

    output_dir = os.path.join(OUTPUT_DIR, program)
    os.makedirs(output_dir, exist_ok=True)
    jar_path = get_jar_path(program)
    config_path = os.path.join("../testing/projects", program, ".env")
    methods_output_path = os.path.join(output_dir, "methods.txt")
    filtered_methods_output_path = os.path.join(output_dir, "filtered_methods.txt")

    methods = get_methods_from_jar(jar_path)
    pattern = get_instrument_pattern(config_path)
    filtered_methods = filter_methods_by_pattern(methods, pattern)

    print(f"Found {len(methods)} matched methods.")
    print(f"Found {len(filtered_methods)} filtered methods.")
    write_methods_to_file(methods, methods_output_path)
    write_methods_to_file(filtered_methods, filtered_methods_output_path)

    source_files = glob(
        CODE_DIR + f"/**/src/main/java/{pattern[:-7]}/**/*.java",
        recursive=True,
    )

    source_code = {}

    check_methods = {shorten_jvm_descriptor(m): m for m in filtered_methods}
    for source_file in source_files:
        methods_in_file = extract_source(source_file)
        for method, code in methods_in_file.items():
            if method in check_methods:
                source_code[check_methods[method]] = code

    missing_methods = {
        check_methods[m] for m in (set(check_methods.keys) - set(source_code.keys()))
    }

    write_source_code_to_file(source_code, os.path.join(output_dir, "code.csv"))
    write_methods_to_file(
        missing_methods, os.path.join(output_dir, "missing_methods.txt")
    )


if __name__ == "__main__":
    main()
