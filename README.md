# Bitonic Sort - Parallel Computing Implementations

This repository contains comprehensive implementations of the Bitonic Sort algorithm using various parallel computing paradigms: OpenMP, MPI, and CUDA GPU.

## Table of Contents

- [Algorithm Overview](#algorithm-overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Build and Run Instructions](#build-and-run-instructions)
- [Usage Examples and Testing](#usage-examples-and-testing)
- [Performance Analysis](#performance-analysis)
- [Performance Visualization](#performance-visualization)
- [Implementation Details](#implementation-details)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## Algorithm Overview

Bitonic Sort is a parallel sorting algorithm that works by recursively constructing bitonic sequences (sequences that first increase then decrease) and then sorting them. It has the following characteristics:

- **Time Complexity**: O(n log²n)
- **Space Complexity**: O(n)
- **Parallelizability**: Highly parallel, suitable for GPU implementation
- **Constraint**: Array size must be a power of 2

## Project Structure

```
Assignment3/
├── OpenMP/
│   ├── openmp_bitonic.c     # OpenMP parallel implementation
│   └── Makefile            # Build configuration
├── MPI/
│   ├── mpi_bitonic.c        # MPI distributed implementation
│   └── Makefile            # Build configuration
├── CUDA/
│   ├── cuda_bitonic.cu      # CUDA GPU implementation
│   └── Makefile            # Build configuration
├── visualize_performance.py   # Performance visualization tool
├── collect_performance_data.py # Automated data collection
├── quick_plot.py             # Simple manual plotting tool
├── sample_performance_data.csv # Example data format
├── Makefile                # Master build file
└── README.md               # This file
```

## Prerequisites

### For OpenMP implementations:

- GCC compiler with C99 support
- OpenMP support (usually included with GCC)

### For MPI implementation:

- MPI implementation (OpenMPI or MPICH)
- MPI compiler wrapper (mpicc)

### For CUDA implementation:

- NVIDIA CUDA Toolkit (version 8.0+)
- NVIDIA GPU with compute capability 3.5+
- NVCC compiler

### For Performance Visualization:

- Python 3.7+
- Required packages: matplotlib, numpy, pandas, seaborn

### Installation on Ubuntu/WSL:

```bash
# Install GCC and OpenMP
sudo apt update
sudo apt install gcc

# Install OpenMPI
sudo apt install openmpi-bin openmpi-common openmpi-doc libopenmpi-dev

# For CUDA (requires NVIDIA GPU)
# Follow NVIDIA's official CUDA installation guide
```

## Quick Start

### Build all implementations:

```bash
make all
```

### Run a quick test of all implementations:

```bash
make run-all
```

### Quick individual tests:

**OpenMP (4 threads):**

```bash
cd OpenMP/ && make && OMP_NUM_THREADS=4 ./openmp_bitonic 1024
```

**MPI (4 processes):**

```bash
cd MPI/ && make && mpirun -np 4 ./mpi_bitonic 1024
```

**CUDA:**

```bash
cd CUDA/ && make && ./cuda_bitonic 1024
```

### Performance benchmark:

```bash
make benchmark
```

## Build and Run Instructions

### OpenMP Implementation

#### Build:

```bash
cd OpenMP/
make
# Or manually: gcc -Wall -Wextra -O3 -std=c99 -fopenmp openmp_bitonic.c -o openmp_bitonic
```

#### Run Commands:

**Basic execution:**

```bash
# Default run (4 threads, size 1024)
make run

# Manual execution with specific thread count
OMP_NUM_THREADS=4 ./openmp_bitonic 1024
OMP_NUM_THREADS=8 ./openmp_bitonic 2048
```

**Thread scaling tests:**

```bash
# Test with different thread counts (1, 2, 4, 8 threads on array size 2048)
make test-threads

# Manual thread scaling
OMP_NUM_THREADS=1 ./openmp_bitonic 2048
OMP_NUM_THREADS=2 ./openmp_bitonic 2048
OMP_NUM_THREADS=4 ./openmp_bitonic 2048
OMP_NUM_THREADS=8 ./openmp_bitonic 2048
```

**Array size scaling tests:**

```bash
# Test with different array sizes (256, 512, 1024, 2048, 4096)
make test-sizes

# Manual array size tests with 4 threads
OMP_NUM_THREADS=4 ./openmp_bitonic 256
OMP_NUM_THREADS=4 ./openmp_bitonic 512
OMP_NUM_THREADS=4 ./openmp_bitonic 1024
OMP_NUM_THREADS=4 ./openmp_bitonic 2048
OMP_NUM_THREADS=4 ./openmp_bitonic 4096
```

**Comprehensive testing:**

```bash
# Run all tests (thread scaling + array size scaling)
make test

# Performance benchmark (parallel implementations)
make benchmark
```

### MPI Implementation

#### Build:

```bash
cd MPI/
make
# Or manually: mpicc -Wall -Wextra -O3 -std=c99 mpi_bitonic.c -o mpi_bitonic
```

#### Run Commands:

**Basic execution:**

```bash
# Default run (4 processes, size 1024)
make run

# Manual execution with specific process count
mpirun -np 4 ./mpi_bitonic 1024
mpirun -np 8 ./mpi_bitonic 2048
```

**Process scaling tests:**

```bash
# Test with different process counts (1, 2, 4, 8 processes on array size 2048)
make test-procs

# Manual process scaling
mpirun -np 1 ./mpi_bitonic 2048
mpirun -np 2 ./mpi_bitonic 2048
mpirun -np 4 ./mpi_bitonic 2048
mpirun -np 8 ./mpi_bitonic 2048
```

**Array size scaling tests:**

```bash
# Test with different array sizes (256, 512, 1024, 2048, 4096)
make test-sizes

# Manual array size tests with 4 processes
mpirun -np 4 ./mpi_bitonic 256
mpirun -np 4 ./mpi_bitonic 512
mpirun -np 4 ./mpi_bitonic 1024
mpirun -np 4 ./mpi_bitonic 2048
mpirun -np 4 ./mpi_bitonic 4096
```

**Comprehensive testing:**

```bash
# Run all tests (process scaling + array size scaling)
make test

# Performance benchmark (1 vs 4 vs 8 processes)
make benchmark
```

**Advanced MPI execution:**

```bash
# Run on specific hosts (for distributed systems)
mpirun -np 4 -H node1,node2,node3,node4 ./mpi_bitonic 4096

# Run with process binding (for NUMA systems)
mpirun -np 4 --bind-to core ./mpi_bitonic 2048

# Run with detailed output
mpirun -np 4 --verbose ./mpi_bitonic 1024
```

### CUDA Implementation

#### Build:

```bash
cd CUDA/
make
# Or manually: nvcc -O3 cuda_bitonic.cu -o cuda_bitonic
```

#### Run:

```bash
./cuda_bitonic 1024
./cuda_bitonic 2048
./cuda_bitonic 4096
```

## Usage Examples and Testing

### Basic Command Line Interface

All implementations follow the same command-line interface:

```bash
./program_name <array_size>
```

Where `array_size` must be a power of 2 (e.g., 256, 512, 1024, 2048, 4096, etc.).

### Comprehensive Testing Commands

#### OpenMP Testing:

**Thread Scaling Analysis:**

```bash
cd OpenMP/
# Quick thread scaling test
make test-threads

# Manual thread scaling for detailed analysis
for threads in 1 2 4 8 16; do
    echo "Testing with $threads threads:"
    OMP_NUM_THREADS=$threads ./openmp_bitonic 2048
done
```

**Array Size Scaling:**

```bash
cd OpenMP/
# Quick size scaling test
make test-sizes

# Manual size scaling with 4 threads
for size in 256 512 1024 2048 4096 8192; do
    echo "Testing size $size:"
    OMP_NUM_THREADS=4 ./openmp_bitonic $size
done
```

#### MPI Testing:

**Process Scaling Analysis:**

```bash
cd MPI/
# Quick process scaling test
make test-procs

# Manual process scaling for detailed analysis
for procs in 1 2 4 8 16; do
    echo "Testing with $procs processes:"
    mpirun -np $procs ./mpi_bitonic 2048
done
```

**Array Size Scaling:**

```bash
cd MPI/
# Quick size scaling test
make test-sizes

# Manual size scaling with 4 processes
for size in 256 512 1024 2048 4096 8192; do
    echo "Testing size $size:"
    mpirun -np 4 ./mpi_bitonic $size
done
```

#### Cross-Implementation Performance Comparison:

```bash
# Test all implementations with the same array size
SIZE=2048

echo "=== OpenMP Implementation (4 threads) ==="
cd ../OpenMP/ && OMP_NUM_THREADS=4 ./openmp_bitonic $SIZE

echo "=== MPI Implementation (4 processes) ==="
cd ../MPI/ && mpirun -np 4 ./mpi_bitonic $SIZE

echo "=== CUDA Implementation ==="
cd ../CUDA/ && ./cuda_bitonic $SIZE
```

### Example Outputs

```
=== OpenMP Bitonic Sort ===
Array Size: 1024
Number of Threads: 4

Before sorting:
First 10 elements: 7845 3421 9876 1234 5678 2345 8901 6789 4567 3210
Last 10 elements:  9999 1111 5555 3333 7777 2222 6666 4444 8888 0000

After sorting:
First 10 elements: 1 5 12 23 34 45 56 67 78 89
Last 10 elements:  9876 9890 9901 9912 9923 9934 9945 9956 9967 9999

=== Results ===
Array Size: 1024
Number of Threads: 4
Execution Time: 8.3 ms
Sorted correctly: YES
```

```
=== MPI Bitonic Sort ===
Array Size: 2048
Number of Processes: 4

Process 0: Local array size = 512
Process 1: Local array size = 512
Process 2: Local array size = 512
Process 3: Local array size = 512

=== Results ===
Array Size: 2048
Number of Processes: 4
Execution Time: 12.7 ms
Communication Time: 3.2 ms
Computation Time: 9.5 ms
Sorted correctly: YES
```

## Performance Analysis

### Expected Performance Characteristics

1. **OpenMP Implementation**: Speedup proportional to number of cores
2. **MPI Implementation**: Good scalability across nodes
3. **CUDA Implementation**: Highest performance for large arrays

### Benchmarking Commands

```bash
# Compare all implementations with size 4096
make benchmark

# Individual detailed testing
cd OpenMP && make benchmark
cd MPI && make benchmark
cd CUDA && make benchmark
```

### Performance Tips

- **Array Size**: Larger arrays show better parallel efficiency
- **Thread Count**: Optimal thread count usually equals CPU core count
- **Process Count**: For MPI, use powers of 2 for best performance
- **GPU Memory**: CUDA performance depends on GPU memory bandwidth

## Performance Visualization

### Automated Data Collection

Use the provided Python script to automatically collect performance data from all implementations:

```bash
# Install Python dependencies
pip install matplotlib numpy pandas seaborn

# Run automated data collection
python collect_performance_data.py
```

This script will:

- Build all implementations automatically
- Run tests with various array sizes and configurations
- Save results to `performance_results.csv`

### Manual Data Collection

If you prefer to collect data manually, follow this format in a CSV file:

```csv
array_size,openmp_1,openmp_2,openmp_4,openmp_8,mpi_1,mpi_2,mpi_4,mpi_8,cuda
256,0.50,0.40,0.30,0.30,0.60,0.50,0.40,0.40,0.10
512,2.10,1.20,0.80,0.70,2.30,1.40,0.90,0.80,0.20
...
```

### Creating Visualizations

#### Option 1: Comprehensive Analysis

```bash
# Generate complete performance report with multiple plots
python visualize_performance.py
```

This creates:

- Execution time comparison (linear and log scale)
- Scalability analysis (threads vs performance)
- Speedup and efficiency plots
- Implementation comparison charts

#### Option 2: Quick Manual Plotting

```bash
# Simple plotting with manual data entry
python quick_plot.py
```

Edit the `execution_times` dictionary in `quick_plot.py` with your measured values, then run to generate plots.

#### Option 3: Custom CSV Data

```bash
# Use your own CSV file
python visualize_performance.py your_data.csv
```

### Example Plots Generated

The visualization tools create:

1. **Execution Time Comparison**: Linear and logarithmic plots showing performance across array sizes
2. **Scalability Analysis**: Thread/process count vs execution time for OpenMP and MPI
3. **Speedup Analysis**: Speedup curves compared to ideal scaling
4. **Efficiency Analysis**: Parallel efficiency percentages
5. **Implementation Comparison**: Bar charts and comparative analysis
6. **CUDA Performance**: GPU vs CPU performance advantages

All plots are saved as high-resolution PNG files suitable for reports and presentations.

## Implementation Details

### OpenMP Implementation Features

- Parallelized compare-and-swap operations
- Parallel sections for independent recursive calls
- Adaptive parallelization (avoids overhead for small segments)
- Thread count control via `OMP_NUM_THREADS`

### MPI Implementation Features

- Distributed array processing
- Local bitonic sort with merge-split communication
- Collective communication patterns
- Scalable across multiple nodes

### CUDA Implementation Features

- Kernel-based parallel compare-and-swap
- Shared memory optimization for cache efficiency
- CUDA events for precise kernel timing
- Adaptive thread/block configuration
- CPU vs GPU performance comparison

## Troubleshooting

### Common Issues

1. **Array size not power of 2**

   ```
   Error: Array size must be a positive power of 2
   ```

   Solution: Use sizes like 256, 512, 1024, 2048, 4096, etc.

2. **MPI process count not power of 2**

   ```
   Error: Number of processes must be a power of 2
   ```

   Solution: Use `-np` values like 1, 2, 4, 8, 16, etc.

3. **OpenMP not working**

   ```
   Number of threads: 1 (even when OMP_NUM_THREADS=4)
   ```

   Solution: Ensure `-fopenmp` flag is used during compilation.

4. **CUDA compilation errors**

   ```
   nvcc: command not found
   ```

   Solution: Install NVIDIA CUDA Toolkit and add to PATH.

5. **Memory allocation failures**
   ```
   Error: Memory allocation failed
   ```
   Solution: Reduce array size or increase available system memory.

### Performance Issues

1. **Poor OpenMP scaling**

   - Check CPU core count: `nproc`
   - Monitor CPU usage: `htop` while running
   - Try different thread counts

2. **MPI communication overhead**

   - Use larger array sizes (≥2048)
   - Ensure processes run on different cores
   - Check network latency for distributed execution

3. **CUDA underperformance**
   - Verify GPU is being used: `nvidia-smi`
   - Check compute capability compatibility
   - Monitor GPU memory usage

### Debug Mode

To enable additional debugging output:

```bash
# Add debug flag to any implementation
gcc -DDEBUG -g -fopenmp openmp_bitonic.c -o openmp_bitonic_debug
```

## Advanced Usage

### Custom Compilation Flags

```bash
# High optimization
gcc -O3 -march=native -fopenmp openmp_bitonic.c -o openmp_bitonic

# Debug build
gcc -g -O0 -DDEBUG -fopenmp openmp_bitonic.c -o openmp_bitonic_debug

# CUDA with specific architecture
nvcc -arch=sm_70 -O3 cuda_bitonic.cu -o cuda_bitonic
```

### Environment Variables

```bash
# OpenMP configuration
export OMP_NUM_THREADS=8
export OMP_SCHEDULE=static
export OMP_PROC_BIND=true

# MPI configuration
export OMPI_MCA_btl_vader_single_copy_mechanism=none  # For some systems
```

## Contributing

To extend or modify the implementations:

1. Follow the existing code style and commenting conventions
2. Ensure all memory allocations have corresponding deallocations
3. Maintain the same command-line interface
4. Add appropriate error checking
5. Update relevant Makefiles and documentation

## License

This code is provided for educational purposes as part of a Parallel Computing course assignment.

## Authors

- Parallel Computing Assignment 3
- December 2025

---

For additional questions or issues, please refer to the course materials or contact the instructor.
