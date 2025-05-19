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


def get_raw_paths(program: str) -> dict:
    """
    Get the paths to the raw call graphs for a given program.
    """
    program_dir = os.path.join(OUTPUT_DIR, program)

    if not os.path.exists(program_dir):
        print(f"Program directory {program_dir} does not exist.")
        return
    print(f"Processing raw data for program: {program}")

    cg_paths = []
    for alg in STATICCG:
        alg_name = alg.replace("/", "-").lower()
        raw_cg_path = os.path.join(program_dir, alg_name, "raw.csv")
        if os.path.exists(raw_cg_path):
            cg_paths.append(raw_cg_path)
        else:
            print(f"Raw call graph for {alg} not found in {program_dir}")

    return cg_paths


def main():
    args = parse_args()
    program = args.program

    cg_paths = get_raw_paths(program)
    if not cg_paths:
        print(f"No raw call graphs found for {program}.")
        return

    output_dir = os.path.join(OUTPUT_DIR, program)
    os.makedirs(output_dir, exist_ok=True)
    methods_file = os.path.join(output_dir, "filtered_methods.txt")

    for cg_path in cg_paths:
        edges_removed_file = os.path.join(output_dir, cg_path, "edges_removed.csv")
        extra_info_file = os.path.join(output_dir, cg_path, "callgraph.csv")

        os.system(
            f"python3 scripts/remove_stdlib_edges.py {cg_path} {methods_file} {edges_removed_file}"
        )
        os.system(
            f"python3 scripts/add_extra_information.py {edges_removed_file} {extra_info_file}"
        )


if __name__ == "__main__":
    main()
