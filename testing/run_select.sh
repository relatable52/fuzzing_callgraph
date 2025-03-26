while read program; do \
    echo "Running $program"; \
    just \
    --justfile projects/justfile \
    --dotenv-path "projects/$program/.env" \
    run_complete; \
done < projects/to_run.txt