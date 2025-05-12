import os

RAW_CALLGRAPH = os.environ.get("CALLGRAPH", "/data/input")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/data/output")
CODE_DIR = os.environ.get("CODE_DIR", "/data/code")

STATICCG = (
    "OPAL/RTA",
    "OPAL/CHA",
    "OPAL/0-CFA",
    "WALA/RTA",
    "WALA/CHA",
    "WALA/0-CFA",
    "Soot/CHA",
)
