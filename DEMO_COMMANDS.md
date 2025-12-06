# Demo Commands for 3-Minute Video

# Copy-paste these commands in sequence to show the project

## TERMINAL SESSION SETUP

```bash
cd /Users/ditharaavindi/Desktop/year 3 sem 1/PC/assignment 3/dj/bitonic_sort
clear
```

## SEGMENT 1: SHOW PROJECT STRUCTURE (0:00 - 0:30)

```bash
echo "=== BITONIC SORT - OPENMP & MPI IMPLEMENTATION ==="
echo ""
echo "Repository Structure:"
ls -la
```

## SEGMENT 2: DISPLAY SOURCE CODE (0:30 - 1:00)

```bash
echo ""
echo "=== OpenMP Implementation (First 30 lines) ==="
head -30 OpenMP/bitonic_openmp.c
```

```bash
echo ""
echo "=== MPI Implementation (First 30 lines) ==="
head -30 MPI/bitonic_mpi.c
```

## SEGMENT 3: RUN OPENMP DEMO (1:00 - 1:45)

```bash
echo ""
echo "=== RUNNING OPENMP BITONIC SORT ==="
echo "Building OpenMP version..."
clang -O2 -std=c11 -Xpreprocessor -fopenmp \
  -I/opt/homebrew/opt/libomp/include \
  -L/opt/homebrew/opt/libomp/lib -lomp \
  OpenMP/bitonic_openmp.c -o OpenMP/bitonic_openmp
```

```bash
echo ""
echo "Sorting with 1 thread:"
OMP_NUM_THREADS=1 ./OpenMP/bitonic_openmp InputFiles/input_small.txt
cat OutputFiles/openmp_output.txt
```

```bash
echo ""
echo "Sorting with 4 threads:"
OMP_NUM_THREADS=4 ./OpenMP/bitonic_openmp InputFiles/input_small.txt
cat OutputFiles/openmp_output.txt
```

```bash
echo ""
echo "Sorting with 16 threads:"
OMP_NUM_THREADS=16 ./OpenMP/bitonic_openmp InputFiles/input_small.txt
cat OutputFiles/openmp_output.txt
```

## SEGMENT 4: RUN MPI DEMO (1:45 - 2:30)

```bash
echo ""
echo "=== RUNNING MPI BITONIC SORT ==="
echo "Building MPI version..."
mpicc -O2 -std=c11 MPI/bitonic_mpi.c -o MPI/bitonic_mpi
```

```bash
echo ""
echo "Sorting with 1 process:"
mpirun --oversubscribe -np 1 MPI/bitonic_mpi InputFiles/input_small.txt
cat OutputFiles/mpi_output.txt
```

```bash
echo ""
echo "Sorting with 4 processes:"
mpirun --oversubscribe -np 4 MPI/bitonic_mpi InputFiles/input_small.txt
cat OutputFiles/mpi_output.txt
```

```bash
echo ""
echo "Sorting with 16 processes:"
mpirun --oversubscribe -np 16 MPI/bitonic_mpi InputFiles/input_small.txt
cat OutputFiles/mpi_output.txt
```

## SEGMENT 5: SHOW TIMING RESULTS (2:30 - 3:00)

```bash
echo ""
echo "=== PERFORMANCE RESULTS ==="
echo ""
echo "OpenMP Execution Times (thread count vs time):"
cat OutputFiles/openmp_times.txt
```

```bash
echo ""
echo "MPI Execution Times (process count vs time):"
cat OutputFiles/mpi_times.txt
```

```bash
echo ""
echo "=== CORRECTNESS VERIFICATION ==="
echo "Both implementations produce identical sorted output:"
echo "OpenMP: $(cat OutputFiles/openmp_output.txt)"
echo "MPI:    $(cat OutputFiles/mpi_output.txt)"
```

---

## GOOGLE COLAB SETUP FOR CUDA VERSION (Optional reference)

If you plan to implement CUDA later, here's a Colab notebook template:

```python
# Google Colab Bitonic Sort CUDA Demo
# Run this in a Colab cell

!git clone https://github.com/yourusername/bitonic_sort.git
%cd bitonic_sort

# Check GPU
!nvidia-smi

# Compile CUDA version (if you implement it)
!nvcc -O2 CUDA/bitonic_cuda.cu -o CUDA/bitonic_cuda

# Run CUDA demo
!./CUDA/bitonic_cuda < InputFiles/input_small.txt
!cat OutputFiles/cuda_output.txt

# Show timing comparisons
!echo "CUDA Execution Times:"
!cat OutputFiles/cuda_times.txt
```

---

## QUICK 3-MIN DEMO USING AUTO SCRIPT

If you want everything automated:

```bash
chmod +x demo.sh
./demo.sh
```

This will run through all segments with pauses so you can record smoothly.
