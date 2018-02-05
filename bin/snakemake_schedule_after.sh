#!/usr/bin/env bash

if [ "$#" -eq 0 ]; then
    echo "Schedule a snakemake job after the running snakemake process has "
    echo "completed. Must be run from the same directory as the Snakefile."
    echo "Usage: $0 <snakemake_command>"
    exit 1;
fi

# Loop until the snakemake locks are removed
while [ "$(ls -A .snakemake/locks)" ]; do
    sleep 60
done

# Run the new snakemake command
eval "$@"
