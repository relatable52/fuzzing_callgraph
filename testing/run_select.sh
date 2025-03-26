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
    just --dotenv-path "$program/.env" projects/run_complete
done <"$TO_RUN"
