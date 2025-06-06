import os

RAW_CALLGRAPH = os.environ.get("CALLGRAPH", "/data/input")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/data/output")
CODE_DIR = os.environ.get("CODE_DIR", "/data/code")

STATICCG = ("OPAL/RTA", "OPAL/0-CFA", "WALA/0-CFA")

PROGRAMS = (
    "apache-commons-jxpath",
    "metadata-extractor",
    "jsoup",
    "json-sanitizer",
    "json-flattener",
    "json-simple",
    "fastcsv",
    "rome",
    "zip4j",
    "jettison",
    "fastjson2",
    "json-smart-v2",
    "xstream",
    "woodstox",
    "dom4j",
    "zt-zip",
    "apache-commons-csv",
    "apache-commons-imaging",
    "itext7",
)
