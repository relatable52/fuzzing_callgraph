from pathlib import Path
import subprocess
from datetime import datetime
import os

to_run_path = Path("projects/to_run.txt")
callgraph_path = os.environ.get("CALLGRAPH")
log_path = Path(os.path.join(callgraph_path, "run_test.log"))

if not to_run_path.exists():
    print(f"Error: {to_run_path} not found!")
    log_path.write_text(f"Error: {to_run_path} not found!\n")
    exit(1)

with log_path.open("a") as log, to_run_path.open() as f:
    log.write(f"Script started at {datetime.now()}\n")
    for line in f:
        program = line.strip()
        if not program:
            continue

        log.write(f"Running program: {program} at {datetime.now()}\n")
        try:
            subprocess.run(["just", "--dotenv-path", f"{program}/.env", "projects/coverage_seed"], check=True)
        except subprocess.CalledProcessError as e:
            log.write(f"Error running {program}: {e}\n")
        log.write(f"Finished program: {program} at {datetime.now()}\n")
    log.write(f"Script ended at {datetime.now()}\n")
