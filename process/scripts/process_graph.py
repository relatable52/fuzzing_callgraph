import csv
import os
from argparse import ArgumentParser

from config import OUTPUT_DIR, STATICCG


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


def get_raw_paths(program: str, file_name: str) -> dict:
    """
    Get the paths to the raw call graphs for a given program.
    """
    program_dir = os.path.join(OUTPUT_DIR, program)

    if not os.path.exists(program_dir):
        print(f"Program directory {program_dir} does not exist.")
        return
    print(f"Processing raw data for program: {program}")

    cg_paths = {}
    for alg in STATICCG:
        alg_name = alg.replace("/", "-").lower()
        raw_cg_path = os.path.join(program_dir, alg_name, file_name)
        if os.path.exists(raw_cg_path):
            cg_paths[alg_name] = raw_cg_path
        else:
            print(f"Raw call graph for {alg} not found in {program_dir}")

    return cg_paths


def process_file(program: str, file_name: str) -> list:
    cg_paths = get_raw_paths(program, file_name)
    if not cg_paths:
        print(f"No raw {file_name} found for {program}.")
        return

    output_dir = os.path.join(OUTPUT_DIR, program)
    os.makedirs(output_dir, exist_ok=True)
    methods_file = os.path.join(output_dir, "filtered_methods.txt")

    for alg_name, cg_path in cg_paths.items():
        base_name = file_name.split(".")[0]
        edges_removed_file = os.path.join(
            output_dir, alg_name, f"{base_name}_edges_removed.csv"
        )
        # extra_info_file = os.path.join(output_dir, alg_name, f"{base_name}_callgraph.csv")
        print(f"Processing {alg_name} for {program}...")

        os.system(
            f"python3 scripts/remove_stdlib_edges.py {cg_path} {methods_file} {edges_removed_file}"
        )


def merge_dynamic_static(folder):
    static_file = os.path.join(folder, "static_edges_removed.csv")
    dynamic_file = os.path.join(folder, "dynamic_edges_removed.csv")
    output_file = os.path.join(folder, "merged.csv")

    edges = {}

    # Read static.csv
    with open(static_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["method"], row["target"], row["offset"])
            edges[key] = {
                "trans": int(row["trans"]),
                "direct": int(row["direct"]),
                "dynamic": 0,
            }

    # Read dynamic.csv
    with open(dynamic_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["method"], row["target"], row["offset"])
            if key not in edges:
                edges[key] = {"trans": 0, "direct": 0, "dynamic": 1}
            else:
                edges[key]["dynamic"] = 1

    # Write merged.csv
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["method", "target", "offset", "trans", "direct", "dynamic"])
        for (method, target, offset), values in edges.items():
            writer.writerow(
                [
                    method,
                    target,
                    offset,
                    values["trans"],
                    values["direct"],
                    values["dynamic"],
                ]
            )

    print(f"Merged CSV saved to: {output_file}")


def main():
    args = parse_args()
    program = args.program

    process_file(program, "static.csv")
    process_file(program, "dynamic.csv")

    # Merge static and dynamic files
    for alg in STATICCG:
        alg_name = alg.replace("/", "-").lower()
        folder = os.path.join(OUTPUT_DIR, program, alg_name)
        if os.path.exists(folder):
            merge_dynamic_static(folder)
        else:
            print(f"Folder {folder} does not exist.")

    # Generate extra info files
    for alg in STATICCG:
        alg_name = alg.replace("/", "-").lower()
        combinded_file = os.path.join(OUTPUT_DIR, program, alg_name, "merged.csv")
        extra_info_file = os.path.join(OUTPUT_DIR, program, alg_name, "callgraph.csv")
        os.system(
            f"python3 scripts/add_extra_information.py {combinded_file} {extra_info_file}"
        )


if __name__ == "__main__":
    main()
