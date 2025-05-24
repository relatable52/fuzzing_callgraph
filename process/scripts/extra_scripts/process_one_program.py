import csv
import logging
import os
from argparse import ArgumentParser
from collections import defaultdict
from glob import glob

from config import OUTPUT_DIR, STATICCG
from utils import read_json

ROOT_METHOD = "<boot>"


def parse_args():
    parser = ArgumentParser(description="Process raw call graph data")
    parser.add_argument(
        "-p",
        "--program",
        type=str,
        required=True,
        help="Name of the program to process (e.g., 'jython', 'javac', etc.)",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        required=True,
        help="Output directory for processed data",
    )
    parser.add_argument(
        "--dyncg_path",
        type=str,
        required=True,
        help="Path to the dynamic call graph JSON file",
    )
    parser.add_argument(
        "--staticcg_dir",
        type=str,
        required=True,
        help="Paths to the static call graph JSON files",
    )
    return parser.parse_args()


def get_cg_paths(dynamic_path: str, static_dir: str) -> dict:
    """
    Get the paths to the call graphs for a given program.
    """
    # print(fuzzing_seed_dyncg)
    static_cg = [
        glob(
            static_dir + f"/**/{alg}/cg.json",
            recursive=True,
        )[0]
        for alg in STATICCG
    ]
    # print(static_cg)

    cg_paths = {
        "Dynamic": dynamic_path,
    }
    for alg, path in zip(STATICCG, static_cg):
        cg_paths[alg] = path

    # print(cg_paths)

    return cg_paths


def format_method(method: dict) -> str:
    """
    Format the method name from the call graph data.
    The method name is formatted as: class_name.method_name:(parameter_types)return_type

    Sample input:
    {
        "name": "put"
        "declaringClass": "Ljava/util/TreeMap;"
        "returnType": "Ljava/lang/Object;"
        "parameterTypes":[
            "Ljava/lang/Object;"
            "Ljava/lang/Object;"
        ]
    }
    Sample output: java.util.TreeMap.put:(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    """
    class_name = method["declaringClass"][1:-1]
    return (
        f"{class_name}.{method['name']}:"
        + "("
        + "".join(method["parameterTypes"])
        + ")"
        + method["returnType"]
    )


def convert_cg_to_rows(data: dict):
    rows = []

    for m in data["reachableMethods"]:
        caller = format_method(m["method"])
        for cs in m.get("callSites", []):
            line = cs.get("line", -1)
            pc = cs.get("pc", -1)
            for tgt in cs.get("targets", []):
                callee = format_method(tgt)
                rows.append([caller, line, callee, pc])

    # Inject <boot> → methods that are never called (no incoming edges)
    callers = {row[0] for row in rows}
    callees = {row[2] for row in rows}

    # These methods are in caller position but never in callee position → roots
    root_methods = callers - callees

    for method in sorted(root_methods):
        rows.append(["<boot>", -1, method, -1])

    return rows


def process_cg(json_path: str):
    data = read_json(json_path)

    rows = convert_cg_to_rows(data)

    return rows


def main():
    args = parse_args()
    program = args.program
    print(program)

    cg_paths = get_cg_paths(program)
    if not cg_paths:
        logging.error(f"No call graph paths found for program: {program}")
        return

    combined_dict = defaultdict(
        dict
    )  # key: (method, offset, target), value: dict of sources

    for name, path in cg_paths.items():
        # print(name)
        try:
            rows = process_cg(path)

            for row in rows:
                method, offset, target, pc = row
                key = (method, offset, target)
                combined_dict[key][name] = 1

        except Exception as e:
            logging.error(f"Error processing {name}: {e}")
            continue

    # Optionally write combined_dict to CSV
    output_combined = os.path.join(OUTPUT_DIR, program, "combined.csv")
    all_sources = sorted(cg_paths.keys())
    with open(output_combined, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["method", "offset", "target"] + all_sources
        writer.writerow(header)

        for (method, offset, target), sources in combined_dict.items():
            row = [method, offset, target]
            row += [sources.get(src, 0) for src in all_sources]
            writer.writerow(row)

    # Step: Create separate CSV for each static analysis
    dynamic_sources = ["Dynamic"]
    for static_alg in STATICCG:
        save_dir = static_alg.replace("/", "-").lower()
        static_path = os.path.join(OUTPUT_DIR, program, save_dir, f"static.csv")
        dynamic_path = os.path.join(OUTPUT_DIR, program, save_dir, f"dynamic.csv")
        os.makedirs(os.path.dirname(static_path), exist_ok=True)
        os.makedirs(os.path.dirname(dynamic_path), exist_ok=True)
        with open(static_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["method", "target", "offset", "static"])

            for (method, offset, target), sources in combined_dict.items():
                static_val = sources.get(static_alg, 0)

                if static_val:
                    writer.writerow([method, target, offset, static_val])

        with open(dynamic_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["method", "target", "offset", "dynamic"])

            for (method, offset, target), sources in combined_dict.items():
                dyn_val = any(sources.get(src, 0) for src in dynamic_sources)

                if dyn_val:
                    writer.writerow([method, target, offset, dyn_val])


if __name__ == "__main__":
    main()
