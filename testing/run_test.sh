#!/bin/bash

TO_RUN="projects/to_run.txt"
LOG_FILE="$CALLGRAPH/test_run_log.txt"

# Ensure the file exists
if [[ ! -f "$TO_RUN" ]]; then
    echo "Error: $TO_RUN not found!" | tee -a "$LOG_FILE"
    exit 1
fi

# Log the start of the script
echo "Script started at $(date)" | tee -a "$LOG_FILE"

# Read and process each program
while IFS= read -r program || [[ -n "$program" ]]; do
    # Trim potential carriage returns
    program=$(echo "$program" | tr -d '\r')

    # Skip empty lines
    [[ -z "$program" ]] && continue

    # Log the program being run
    echo "Running program: $program at $(date)" | tee -a "$LOG_FILE"

    # Run the just command
    just --dotenv-path "$program/.env" projects/build_jar

    # Log completion of the program
    echo "Finished program: $program at $(date)" | tee -a "$LOG_FILE"

done <"$TO_RUN"

# Log the end of the script
echo "Script ended at $(date)" | tee -a "$LOG_FILE"
