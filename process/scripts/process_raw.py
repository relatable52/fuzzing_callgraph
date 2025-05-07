import logging
import os
from argparse import ArgumentParser
from glob import glob

import pandas as pd

from .config import OUTPUT_DIR, RAW_CALLGRAPH, STATICCG
from .utils import read_json


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


def get_cg_paths(program: str) -> dict:
    """
    Get the paths to the call graphs for a given program.
    """
    program_dir = os.path.join(RAW_CALLGRAPH, program)

    if not os.path.exists(program_dir):
        logging.error(f"Program directory {program_dir} does not exist.")
        return
    logging.info(f"Processing raw data for program: {program}")

    output_dir = os.path.join(OUTPUT_DIR, program)
    os.makedirs(output_dir, exist_ok=True)

    fuzzing_dyncg = glob(program_dir + "**/fuzzing/**/cg.json", recursive=True)[0]
    fuzzing_seed_dyncg = glob(
        program_dir + "**/fuzzing_seed/**/cg.json", recursive=True
    )[0]
    static_cg = [
        glob(
            os.path.join(program_dir, f"staticcg/**/{alg}/**/cg.json"), recursive=True
        )[0]
        for alg in STATICCG
    ]

    cg_paths = {
        "Dynamic/fuzzing": fuzzing_dyncg,
        "Dynamic/fuzzing_seed": fuzzing_seed_dyncg,
    }
    for alg, path in zip(STATICCG, static_cg):
        cg_paths[alg] = path

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


def convert_cg(data: dict) -> pd.DataFrame:
    """
    Process the call graph data into a DataFrame.
    """
    raw_edges = []

    for m in data["reachableMethods"]:
        caller = format_method(m["method"])
        for cs in m.get("callSites", []):
            line = cs.get("line", -1)
            pc = cs.get("pc", -1)
            for tgt in cs.get("targets", []):
                callee = format_method(tgt)

                raw_edges.append(
                    {"caller": caller, "callee": callee, "line": line, "pc": pc}
                )

    df = pd.DataFrame(raw_edges)
    return df


def process_cg(json_path: str, output_path: str) -> None:
    """
    Process the call graph JSON file and save it as a CSV file.
    """
    data = read_json(json_path)
    df = convert_cg(data)
    df.to_csv(output_path, index=False)


def main():
    args = parse_args()
    program = args.program

    cg_paths = get_cg_paths(program)
    if not cg_paths:
        return

    for name, path in cg_paths.items():
        output_name = name.lower().replace("/", "_") + ".csv"
        output_path = os.path.join(OUTPUT_DIR, program, output_name)
        logging.info(f"Processing {name} from {path} to {output_path}")
        try:
            process_cg(path, output_path)
        except Exception as e:
            logging.error(f"Error processing {name}: {e}")
            continue
        logging.info(f"Processed {name} and saved to {output_path}")
