# Bitonic Sort (OpenMP + MPI)

Parallel implementations of bitonic sort in C using OpenMP (shared memory) and MPI (distributed memory). The repo includes scripts to build and benchmark with varying thread/process counts and sample input datasets.

## Repository Layout

- `InputFiles/` — integer datasets (`input1.txt`, `input2.txt`).
- `OutputFiles/` — outputs and timing logs.
  - `openmp_output.txt`, `mpi_output.txt`
  - `openmp_times.txt`, `mpi_times.txt`
- `OpenMP/bitonic_openmp.c` — OpenMP bitonic sort.
- `MPI/bitonic_mpi.c` — MPI bitonic sort.
- `run_openmp.sh` — build + run OpenMP sweep over threads {1,2,4,8,16}.
- `run_mpi.sh` — build + run MPI sweep over processes {1,2,4,8,16}.

## Requirements & Installation

### macOS (with Homebrew)

1. Install Homebrew (if not already installed):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install required packages:

   ```bash
   brew install libomp open-mpi
   ```

3. Verify installation:
   ```bash
   clang --version          # Check clang
   mpicc --version          # Check MPI
   ```

### Linux (Ubuntu/Debian)

1. Update package manager:

   ```bash
   sudo apt-get update
   ```

2. Install OpenMP and MPI:

   ```bash
   sudo apt-get install libomp-dev libopenmpi-dev openmpi-bin
   ```

3. Verify installation:
   ```bash
   gcc --version            # Check GCC (has OpenMP)
   mpicc --version          # Check MPI
   ```

### Linux (Red Hat/CentOS/Fedora)

1. Install packages:

   ```bash
   sudo dnf install libomp-devel open-mpi-devel
   ```

2. Verify installation:
   ```bash
   gcc --version
   mpicc --version
   ```

## Quick Start

1. Ensure compilers are available (see Requirements). On macOS with Homebrew:
   - `brew install libomp open-mpi`
2. Run OpenMP sweep (from repo root):
   - `bash run_openmp.sh InputFiles/input1.txt`
   - Results: `OutputFiles/openmp_output.txt` and timings in `OutputFiles/openmp_times.txt`.
3. Run MPI sweep (from repo root):
   - `bash run_mpi.sh InputFiles/input1.txt`
   - Results: `OutputFiles/mpi_output.txt` and timings in `OutputFiles/mpi_times.txt`.

See `RUN.md` for detailed build/run notes and troubleshooting.
