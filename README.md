# Bitonic Sort - Parallel Computing Implementations

This repository contains comprehensive implementations of the Bitonic Sort algorithm using various parallel computing paradigms: Serial C, OpenMP, MPI, and CUDA GPU.

## Table of Contents

- [Algorithm Overview](#algorithm-overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Build Instructions](#detailed-build-instructions)
- [Usage Examples](#usage-examples)
- [Performance Analysis](#performance-analysis)
- [Implementation Details](#implementation-details)
- [Troubleshooting](#troubleshooting)

## Algorithm Overview

Bitonic Sort is a parallel sorting algorithm that works by recursively constructing bitonic sequences (sequences that first increase then decrease) and then sorting them. It has the following characteristics:

- **Time Complexity**: O(n log²n)
- **Space Complexity**: O(n)
- **Parallelizability**: Highly parallel, suitable for GPU implementation
- **Constraint**: Array size must be a power of 2

## Project Structure

```
Assignment3/
├── Serial/
│   ├── serial_bitonic.c     # Sequential implementation
│   └── Makefile            # Build configuration
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

### For Serial and OpenMP implementations:

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

### Performance benchmark:

```bash
make benchmark
```

## Detailed Build Instructions

### Serial Implementation

```bash
cd Serial/
gcc serial_bitonic.c -o serial_bitonic
# Or use Makefile
make
```

**Usage:**

```bash
./serial_bitonic 1024
```

### OpenMP Implementation

```bash
cd OpenMP/
gcc -fopenmp openmp_bitonic.c -o openmp_bitonic
# Or use Makefile
make
```

**Usage:**

```bash
# Set number of threads
export OMP_NUM_THREADS=4
./openmp_bitonic 1024

# Or inline
OMP_NUM_THREADS=8 ./openmp_bitonic 2048
```

### MPI Implementation

```bash
cd MPI/
mpicc mpi_bitonic.c -o mpi_bitonic
# Or use Makefile
make
```

**Usage:**

```bash
# Run with 4 processes
mpirun -np 4 ./mpi_bitonic 1024

# Run with 8 processes
mpirun -np 8 ./mpi_bitonic 2048
```

### CUDA Implementation

```bash
cd CUDA/
nvcc cuda_bitonic.cu -o cuda_bitonic
# Or use Makefile
make
```

**Usage:**

```bash
./cuda_bitonic 1024
```

## Usage Examples

### Basic Usage

All implementations follow the same command-line interface:

```bash
./program_name <array_size>
```

Where `array_size` must be a power of 2 (e.g., 256, 512, 1024, 2048, 4096, etc.).

### Example Outputs

```
=== Serial Bitonic Sort ===
Array Size: 1024

Before sorting:
First 10 elements: 7845 3421 9876 1234 5678 2345 8901 6789 4567 3210
Last 10 elements:  9999 1111 5555 3333 7777 2222 6666 4444 8888 0000

After sorting:
First 10 elements: 1 5 12 23 34 45 56 67 78 89
Last 10 elements:  9876 9890 9901 9912 9923 9934 9945 9956 9967 9999

=== Results ===
Array Size: 1024
Execution Time: 15.2 ms
Sorted correctly: YES
```

### Testing Different Configurations

#### OpenMP Thread Scaling:

```bash
cd OpenMP/
make test-threads  # Tests with 1, 2, 4, 8 threads
```

#### MPI Process Scaling:

```bash
cd MPI/
make test-procs    # Tests with 1, 2, 4, 8 processes
```

#### Array Size Scaling:

```bash
cd Serial/
make test          # Tests with sizes 256, 512, 1024, 2048
```

## Performance Analysis

### Expected Performance Characteristics

1. **Serial Implementation**: Baseline performance
2. **OpenMP Implementation**: Speedup proportional to number of cores
3. **MPI Implementation**: Good scalability across nodes
4. **CUDA Implementation**: Highest performance for large arrays

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
array_size,serial,openmp_1,openmp_2,openmp_4,openmp_8,mpi_1,mpi_2,mpi_4,mpi_8,cuda
256,0.50,0.50,0.40,0.30,0.30,0.60,0.50,0.40,0.40,0.10
512,2.10,2.10,1.20,0.80,0.70,2.30,1.40,0.90,0.80,0.20
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

### Serial Implementation Features

- Clean, well-commented recursive bitonic sort
- Dynamic memory allocation
- Comprehensive error checking
- Performance timing using `clock()`

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
gcc -DDEBUG -g serial_bitonic.c -o serial_bitonic_debug
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
