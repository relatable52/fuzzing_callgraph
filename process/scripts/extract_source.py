import csv
import json
import os
import re
import subprocess
from argparse import ArgumentParser
from glob import glob

import javalang
from config import CODE_DIR, OUTPUT_DIR, RAW_CALLGRAPH
from parser_utils import get_method_start_end, get_method_text, type_to_descriptor


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
    print(jar_dir, jar_path)

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


def get_matched_methods(
    method_name: str,
    class_name: str,
    package_name: str,
    params: list,
    return_type: str,
    methods: set,
) -> list:
    matched_methods = []
    for method in methods:
        method_parts = method.split(":")[0]
        params = method.split(":")[1].split(")")[0][1:]
        return_type = method.split(":")[1].split(")")[1]
        check = True
        if f"{class_name}.{method_name}" not in method_parts:
            check = False
        if package_name and package_name not in method_parts:
            check = False
        for param in params:
            if param not in method_parts:
                check = False
        if return_type not in method_parts:
            check = False
        if check:
            matched_methods.append(method)
    return matched_methods


def get_method_parameters(method_node):
    params = []
    for param in method_node.parameters:
        params.append(type_to_descriptor(param.type))
    return params


def extract_method_from_source(source_file: str, methods: set):
    with open(source_file) as f:
        codelines = f.readlines()
        code_text = "".join(codelines)

    lex = None
    tree = javalang.parse.parse(code_text)
    package_name = tree.package.name if tree.package else ""
    methods = {}
    for path, class_node in tree.filter(javalang.tree.ClassDeclaration):
        class_name = class_node.name
        for method_node in class_node.methods:
            method_name = method_node.name
            startpos, endpos, startline, endline = get_method_start_end(
                tree, method_node
            )
            method_text, startline, endline, lex = get_method_text(
                codelines, startpos, endpos, startline, endline, lex
            )
            params = get_method_parameters(method_node)
            return_type = type_to_descriptor(method_node.return_type)
            matched_methods = get_matched_methods(
                method_name, class_name, package_name, params, return_type, methods
            )
            assert (
                len(matched_methods) == 1
            ), f"Multiple matched methods found for {method_name} in {class_name}"
            methods[matched_methods[0]] = method_text
        for method_node in class_node.constructors:
            method_name = "<init>"
            startpos, endpos, startline, endline = get_method_start_end(method_node)
            method_text, startline, endline, lex = get_method_text(
                startpos, endpos, startline, endline, lex
            )
            params = get_method_parameters(method_node)
            return_type = type_to_descriptor(method_node.return_type)
            matched_methods = get_matched_methods(
                method_name, class_name, package_name, params, return_type, methods
            )
            assert (
                len(matched_methods) == 1
            ), f"Multiple matched methods found for {method_name} in {class_name}"
            methods[matched_methods[0]] = method_text
    return methods


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
        CODE_DIR + f"/**/{pattern[:-7]}/**/*.java",
        recursive=True,
    )

    print(CODE_DIR + f"/**/{pattern[:-7]}/**/*.java")

    methods = {}
    for source_file in source_files:
        methods.update(extract_method_from_source(source_file, filtered_methods))

    source_code_output_path = os.path.join(output_dir, "source_code.csv")
    with open(source_code_output_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["method", "source_code"])
        for method, code in methods.items():
            writer.writerow([method, code])
    print(f"Extracted source code for {len(filtered_methods)} methods.")


if __name__ == "__main__":
    main()
