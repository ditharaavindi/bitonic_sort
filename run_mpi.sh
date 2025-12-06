#!/usr/bin/env bash
set -euo pipefail

INPUT=${1:-InputFiles/input1.txt}
EXE=MPI/bitonic_mpi
RESULTS=OutputFiles/mpi_times.txt
MPI_RUN_OPTS=${MPI_RUN_OPTS:---oversubscribe}

mkdir -p OutputFiles

echo "Building MPI version..."
mpicc -O2 -std=c11 MPI/bitonic_mpi.c -o "$EXE"

echo "Input file: $INPUT" > "$RESULTS"
for p in 1 2 4 8 16; do
    echo "Running with $p process(es)..."
    run_output=$(mpirun $MPI_RUN_OPTS -np "$p" "$EXE" "$INPUT")
    echo "$run_output"
    exec_time=$(echo "$run_output" | awk '/Execution time/ {print $4}')
    echo "$p $exec_time" >> "$RESULTS"
done

echo "Execution times saved to $RESULTS"
