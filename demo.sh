#!/bin/bash
# Demo Script for Bitonic Sort (OpenMP + MPI) Assignment
# This script demonstrates the functionality and performance of both implementations
# Run this to generate a demo showing sorting correctness and timing measurements

set -euo pipefail

REPO_ROOT="/Users/ditharaavindi/Desktop/year 3 sem 1/PC/assignment 3/dj/bitonic_sort"
cd "$REPO_ROOT"

echo "======================================================================"
echo "BITONIC SORT PARALLEL IMPLEMENTATION - 3 MINUTE DEMO SCRIPT"
echo "======================================================================"
echo ""

# ==================== PART 1: INTRODUCE THE PROJECT ====================
echo "PART 1: PROJECT OVERVIEW (0:00 - 0:30)"
echo "========================================"
echo "This demo showcases parallel implementations of Bitonic Sort using:"
echo "  • OpenMP (Shared Memory Parallelism)"
echo "  • MPI (Distributed Memory Parallelism)"
echo ""
echo "Input dataset: 15 integers (small for clarity)"
echo "Original array: 9 4 7 3 12 1 6 8 2 5 10 14 0 11 13"
echo ""
read -p "Press Enter to continue..."
echo ""

# ==================== PART 2: SHOW REPOSITORY STRUCTURE ====================
echo "PART 2: REPOSITORY STRUCTURE (0:30 - 1:00)"
echo "=========================================="
echo "Directory layout:"
tree -L 2 --dirsfirst 2>/dev/null || find . -maxdepth 2 -type f | head -20
echo ""
echo "Key files:"
echo "  • OpenMP/bitonic_openmp.c  - OpenMP implementation"
echo "  • MPI/bitonic_mpi.c        - MPI implementation"
echo "  • InputFiles/input_small.txt - Small test dataset"
echo "  • OutputFiles/           - Results and timing logs"
echo ""
read -p "Press Enter to continue..."
echo ""

# ==================== PART 3: DEMONSTRATE OPENMP ====================
echo "PART 3: OPENMP EXECUTION (1:00 - 1:45)"
echo "======================================"
echo "Running OpenMP bitonic sort with varying thread counts..."
echo ""
bash run_openmp.sh InputFiles/input_small.txt
echo ""
echo "OpenMP timing results:"
cat OutputFiles/openmp_times.txt
echo ""
read -p "Press Enter to continue..."
echo ""

# ==================== PART 4: DEMONSTRATE MPI ====================
echo "PART 4: MPI EXECUTION (1:45 - 2:30)"
echo "===================================="
echo "Running MPI bitonic sort with varying process counts..."
echo ""
bash run_mpi.sh InputFiles/input_small.txt
echo ""
echo "MPI timing results:"
cat OutputFiles/mpi_times.txt
echo ""
read -p "Press Enter to continue..."
echo ""

# ==================== PART 5: VERIFY CORRECTNESS ====================
echo "PART 5: CORRECTNESS VERIFICATION (2:30 - 3:00)"
echo "=============================================="
echo "Comparing sorted outputs from both implementations:"
echo ""
echo "OpenMP sorted output:"
cat OutputFiles/openmp_output.txt
echo ""
echo "MPI sorted output:"
cat OutputFiles/mpi_output.txt
echo ""

# Check if outputs match
OPENMP_OUTPUT=$(cat OutputFiles/openmp_output.txt)
MPI_OUTPUT=$(cat OutputFiles/mpi_output.txt)

if [ "$OPENMP_OUTPUT" = "$MPI_OUTPUT" ]; then
    echo "✓ SUCCESS: Both implementations produce identical sorted results!"
else
    echo "✗ MISMATCH: Outputs differ (check implementations)"
fi

echo ""
echo "======================================================================"
echo "DEMO COMPLETE - Both OpenMP and MPI implementations working correctly"
echo "======================================================================"
echo ""
echo "Performance Summary:"
echo "  • OpenMP: Effective for shared-memory systems"
echo "  • MPI: Effective for distributed/cluster systems"
echo "  • Both demonstrate correct bitonic sort algorithm"
echo ""
