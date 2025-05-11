import logging
import os
from argparse import ArgumentParser
from glob import glob

import pandas as pd
from config import OUTPUT_DIR, RAW_CALLGRAPH, STATICCG
from utils import read_json


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
    logging.warning(f"Processing raw data for program: {program}")

    print(f"Processing raw data for program: {program}")

    output_dir = os.path.join(OUTPUT_DIR, program)
    os.makedirs(output_dir, exist_ok=True)

    fuzzing_dyncg = glob(program_dir + "/**/fuzzing/**/cg.json", recursive=True)[0]
    fuzzing_seed_dyncg = glob(
        program_dir + "/**/fuzzing_seed/**/cg.json", recursive=True
    )[0]
    print(fuzzing_dyncg)
    print(fuzzing_seed_dyncg)
    static_cg = [
        glob(
            os.path.join(program_dir, f"/**/staticcg/**/{alg}/cg.json"),
            recursive=True,
        )[0]
        for alg in STATICCG
    ]
    print(static_cg)

    cg_paths = {
        "Dynamic/fuzzing": fuzzing_dyncg,
        "Dynamic/fuzzingseed": fuzzing_seed_dyncg,
    }
    for alg, path in zip(STATICCG, static_cg):
        cg_paths[alg] = path

    print(cg_paths)

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
                    {"method": caller, "target": callee, "offset": line, "pc": pc}
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
    return df


def main():
    args = parse_args()
    program = args.program
    print(program)

    cg_paths = get_cg_paths(program)
    print(cg_paths)
    if not cg_paths:
        logging.error(f"No call graph paths found for program: {program}")
        return

    # for name, path in cg_paths.items():
    #     output_name = name.lower().replace("/", "_") + ".csv"
    #     output_path = os.path.join(OUTPUT_DIR, program, output_name)
    #     logging.info(f"Processing {name} from {path} to {output_path}")
    #     print(name)

    #     try:
    #         df = process_cg(path, output_path)
    #         df[name] = 1
    #         df = df[["method", "offset", "target", name]]
    #         if combined_df is None:
    #             combined_df = df
    #         else:
    #             combined_df = pd.merge(
    #                 combined_df, df, on=["method", "offset", "target"], how="outer"
    #             )
    #     except Exception as e:
    #         logging.error(f"Error processing {name}: {e}")
    #         continue

    # if combined_df is not None:
    #     combined_df.fillna(0, inplace=True)

    #     analysis_methods = [name for name in cg_paths.keys()]
    #     combined_df[analysis_methods] = combined_df[analysis_methods].astype(int)

    #     combination_path = os.path.join(OUTPUT_DIR, program, "combination.csv")
    #     combined_df.to_csv(combination_path, index=False)
    #     logging.info(f"Combined call graph saved to {combination_path}")
    # else:
    #     logging.warning("No call graph data to combine.")

    # logging.info(f"Processed {name} and saved to {output_path}")


if __name__ == "__main__":
    print("Starting process_raw.py")
    program = "fastcsv"

    cg_paths = get_cg_paths(program)
    print(cg_paths)
    if not cg_paths:
        logging.error(f"No call graph paths found for program: {program}")
