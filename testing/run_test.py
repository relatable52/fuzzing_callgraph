from pathlib import Path
import subprocess
from datetime import datetime
import os
import logging

# Paths
to_run_path = Path("projects/to_run.txt")
callgraph_path = os.environ.get("CALLGRAPH")
log_path = Path(callgraph_path) / "run_test.log"

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
        try:
            subprocess.run(
                ["just", "--dotenv-path", f"{program}/.env", "projects/coverage_seed"],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed: {program} | {e}")
        else:
            logging.info(f"Finished: {program}")

logging.info("Script ended")
