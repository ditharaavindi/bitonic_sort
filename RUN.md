# Run & Build Guide

## Prerequisites Installation

### macOS

```bash
# Install Homebrew package manager (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install OpenMP (libomp) and MPI (Open MPI)
brew install libomp open-mpi

# Verify installation
clang --version
mpicc --version
```

### Ubuntu/Debian (Linux)

```bash
sudo apt-get update
sudo apt-get install libomp-dev libopenmpi-dev openmpi-bin

# Verify
gcc --version
mpicc --version
```

### Red Hat/CentOS/Fedora (Linux)

```bash
sudo dnf install libomp-devel open-mpi-devel

# Verify
gcc --version
mpicc --version
```

---

## OpenMP Version

- Build and sweep threads (default input `InputFiles/input1.txt`):
  ```bash
  bash run_openmp.sh InputFiles/input1.txt
  ```
- Output:
  - Sorted data: `OutputFiles/openmp_output.txt`
  - Timings: `OutputFiles/openmp_times.txt` (thread count, seconds)
- macOS compiler note:
  - Uses `clang` with Homebrew `libomp`. Install via `brew install libomp`.
  - Custom compiler: `CC=gcc bash run_openmp.sh ...` (if GCC has OpenMP enabled).

## MPI Version

- Build and sweep processes (default input `InputFiles/input1.txt`):
  ```bash
  bash run_mpi.sh InputFiles/input1.txt
  ```
- Output:
  - Sorted data: `OutputFiles/mpi_output.txt`
  - Timings: `OutputFiles/mpi_times.txt` (process count, seconds)
- Notes:
  - Script passes `--oversubscribe` to allow more ranks than physical cores.
  - Requires `mpicc`/`mpirun` (e.g., `brew install open-mpi` on macOS).

## Inputs

- Place integer data in `InputFiles/` (space- or newline-separated). Samples:
  - `input1.txt` (1024 ints)
  - `input2.txt` (2048 ints)

## Environment Variables

- `OMP_NUM_THREADS` — overrides thread count if you run the OpenMP binary manually.
- `CC` — compiler for OpenMP build (default `clang`).
- `MPI_RUN_OPTS` — extra args to `mpirun` (defaults to `--oversubscribe`).

## Manual Builds (optional)

- OpenMP (clang + libomp on macOS):
  ```bash
  clang -O2 -std=c11 -Xpreprocessor -fopenmp \
    -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp \
    OpenMP/bitonic_openmp.c -o OpenMP/bitonic_openmp
  ```
- MPI:
  ```bash
  mpicc -O2 -std=c11 MPI/bitonic_mpi.c -o MPI/bitonic_mpi
  ```

## Viewing Results

- Timings: `OutputFiles/openmp_times.txt`, `OutputFiles/mpi_times.txt`.
- Sorted outputs: `OutputFiles/openmp_output.txt`, `OutputFiles/mpi_output.txt`.

## Troubleshooting

- "unsupported option -fopenmp" (macOS): install `libomp` and use the provided clang flags.
- "not enough slots" from `mpirun`: reduce `-np` or keep `--oversubscribe`.
- Permission denied on scripts: `chmod +x run_openmp.sh run_mpi.sh`.
