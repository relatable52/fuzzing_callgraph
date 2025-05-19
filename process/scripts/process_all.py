import os
import subprocess

from config import PROGRAMS


def run_one(program: str, script: str):
    env = os.environ.copy()

    print(program, script)

    process = subprocess.Popen(
        ["python", f"scripts/{script}", "-p", program],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    for line in process.stdout:
        print(line, end="")
    process.wait()


def main():
    for p in PROGRAMS:
        run_one(p, "extract_source.py")
    for p in PROGRAMS:
        run_one(p, "process_raw.py")
    for p in PROGRAMS:
        run_one(p, "process_graph.py")


if __name__ == "__main__":
    main()
