import argparse
import logging
import os
import subprocess
from pathlib import Path


# Function to run a just target
def run_just(program, target):
    env = os.environ.copy()
    try:
        subprocess.run(
            ["just", "--dotenv-path", f"{program}/.env", target], check=True, env=env
        )
        logging.info(f"Ran target: {target} for {program}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed target: {target} for {program} | {e}")


# Argument parsing
parser = argparse.ArgumentParser(
    description="Run coverage and fuzzing targets for programs listed in a file."
)
parser.add_argument(
    "--fuzzing",
    type=int,
    default=6,
    help="Number of times to run coverage_fuzzing (default: 5)",
)
parser.add_argument(
    "--fuzzing-seed",
    type=int,
    default=6,
    help="Number of times to run coverage_fuzzing_seed (default: 12)",
)
args = parser.parse_args()

FUZZING_RUNS = args.fuzzing
FUZZING_SEED_RUNS = args.fuzzing_seed

# Paths
to_run_path = Path("projects/to_run.txt")
callgraph_path = os.environ.get("CALLGRAPH")
log_path = Path(callgraph_path) / "run_select.log"

# Configure logging
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Start script
if not to_run_path.exists():
    logging.error(f"{to_run_path} not found!")
    exit(1)

logging.info("Script started")

# Process programs
with to_run_path.open() as f:
    for line in f:
        program = line.strip()
        if not program:
            continue

        logging.info(f"Running: {program}")

        # Run all commands in the justfile
        run_just(program, "projects/coverage_seed")
        run_just(program, "projects/static_callgraphs")

        for i in range(1, FUZZING_RUNS + 1):
            logging.info(f"Fuzzing iteration {i}/{FUZZING_RUNS} for {program}")
            run_just(program, "projects/coverage_fuzzing")

        for i in range(1, FUZZING_SEED_RUNS + 1):
            logging.info(
                f"Fuzzing seed iteration {i}/{FUZZING_SEED_RUNS} for {program}"
            )
            run_just(program, "projects/coverage_fuzzing_seed")

        run_just(program, "projects/dynamic_callgraph_fuzzing")
        run_just(program, "projects/dynamic_callgraph_fuzzing_seed")

        logging.info(f"Finished program: {program}")

logging.info("Script ended")
