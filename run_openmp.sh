#!/usr/bin/env bash
set -euo pipefail

INPUT=${1:-InputFiles/input.txt}
EXE=OpenMP/bitonic_openmp
RESULTS=OutputFiles/openmp_times.txt

mkdir -p OutputFiles

echo "Building OpenMP version..."
CC=${CC:-clang}
OMP_FLAGS="-Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp"
"$CC" -O2 -std=c11 $OMP_FLAGS OpenMP/bitonic_openmp.c -o "$EXE"

echo "Input file: $INPUT" > "$RESULTS"
for t in 1 2 4 8 16; do
    export OMP_NUM_THREADS=$t
    echo "Running with $t thread(s)..."
    run_output=$("$EXE" "$INPUT")
    echo "$run_output"
    exec_time=$(echo "$run_output" | awk '/Execution time/ {print $4}')
    echo "$t $exec_time" >> "$RESULTS"
done

echo "Execution times saved to $RESULTS"
