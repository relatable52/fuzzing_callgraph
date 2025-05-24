from scripts.extract_source import (
    filter_methods_by_pattern,
    get_methods_from_jar,
    write_methods_to_file,
)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description="Extract methods from a JAR file.")
    parser.add_argument(
        "--jar_path", type=str, required=True, help="Path to the JAR file."
    )
    parser.add_argument(
        "--pattern", type=str, required=True, help="Regex pattern to filter methods."
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="filtered_methods.txt",
        help="Output file to write filtered methods.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    jar_path = args.jar_path
    pattern = args.pattern

    # Extract methods from the JAR file
    methods = get_methods_from_jar(jar_path)

    # Filter methods by the provided regex pattern
    filtered_methods = filter_methods_by_pattern(methods, pattern)

    # Write the filtered methods to a file
    output_file = "filtered_methods.txt"
    write_methods_to_file(filtered_methods, output_file)
