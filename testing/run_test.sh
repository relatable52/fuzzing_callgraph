#!/bin/bash

TO_RUN="projects/to_run.txt"

# Ensure the file exists
if [[ ! -f "$TO_RUN" ]]; then
    echo "Error: $TO_RUN not found!"
    exit 1
fi

# Read and process each program
while IFS= read -r program || [[ -n "$program" ]]; do
    # Trim potential carriage returns
    program=$(echo "$program" | tr -d '\r')

    # Skip empty lines
    [[ -z "$program" ]] && continue

    # Run the just command
    just --dotenv-path "$program/.env" projects/coverage_fuzzing_seed
    just --dotenv-path "$program/.env" projects/dynamic_callgraph_fuzzing_seed
    
done <"$TO_RUN"
