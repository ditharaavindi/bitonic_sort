# Screenshot Guide for Performance Evaluation

## Overview

This guide provides step-by-step instructions for taking screenshots of OpenMP and MPI performance runs for the assignment documentation.

## Prerequisites

- Make sure both OpenMP and MPI implementations are built:
  ```bash
  cd OpenMP && make clean && make
  cd ../MPI && make clean && make
  ```

## OpenMP Screenshots

### Screenshot 1: Single Thread Execution

```bash
cd OpenMP
export OMP_NUM_THREADS=1
./openmp_bitonic 4096
```

**What to capture:** Terminal showing the execution with 1 thread, including execution time and "Number of threads: 1"

### Screenshot 2: Two Threads Execution

```bash
export OMP_NUM_THREADS=2
./openmp_bitonic 4096
```

**What to capture:** Terminal showing execution with 2 threads, performance improvement visible

### Screenshot 3: Four Threads Execution

```bash
export OMP_NUM_THREADS=4
./openmp_bitonic 4096
```

**What to capture:** Terminal showing execution with 4 threads, further performance improvement

### Screenshot 4: Eight Threads Execution

```bash
export OMP_NUM_THREADS=8
./openmp_bitonic 4096
```

**What to capture:** Terminal showing execution with 8 threads, peak performance (if available)

### Screenshot 5: Sixteen Threads Execution (if applicable)

```bash
export OMP_NUM_THREADS=16
./openmp_bitonic 4096
```

**What to capture:** Terminal showing execution with 16 threads, possible performance degradation due to over-subscription

### Screenshot 6: OpenMP Thread Scaling Test

```bash
make test-threads
```

**What to capture:** Terminal showing automated testing with different thread counts for comparison

### Screenshot 7: OpenMP Performance Graphs

Run the performance evaluation script and capture the generated graphs:

```bash
python3 performance_evaluation.py --openmp
```

**What to capture:** Screenshot of the generated OpenMP performance analysis graphs showing:

- Execution time vs threads
- Speedup vs threads
- Efficiency vs threads
- Scalability analysis

## MPI Screenshots

### Screenshot 8: Single Process Execution

```bash
cd MPI
mpirun -np 1 ./mpi_bitonic 4096
```

**What to capture:** Terminal showing execution with 1 process (baseline performance)

### Screenshot 9: Two Processes Execution

```bash
mpirun -np 2 ./mpi_bitonic 4096
```

**What to capture:** Terminal showing execution with 2 processes, communication patterns visible

### Screenshot 10: Four Processes Execution

```bash
mpirun -np 4 ./mpi_bitonic 4096
```

**What to capture:** Terminal showing execution with 4 processes, optimal performance expected

### Screenshot 11: Eight Processes Execution

```bash
mpirun -np 8 ./mpi_bitonic 4096
```

**What to capture:** Terminal showing execution with 8 processes, communication overhead may become visible

### Screenshot 12: MPI Process Scaling Test

```bash
make test-procs
```

**What to capture:** Terminal showing automated testing with different process counts

### Screenshot 13: MPI Performance Graphs

```bash
python3 performance_evaluation.py --mpi
```

**What to capture:** Screenshot of the generated MPI performance analysis graphs showing:

- Execution time vs processes
- Speedup vs processes
- Efficiency vs processes
- Communication overhead analysis

## Additional Screenshots for Analysis

### Screenshot 14: System Information

```bash
# Show system specifications
echo "CPU Information:"
sysctl -n machdep.cpu.brand_string
sysctl -n hw.ncpu
sysctl -n hw.logicalcpu
echo "Memory Information:"
sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}'

# Show MPI configuration
mpirun --version
```

**What to capture:** Terminal showing system specifications and MPI version

### Screenshot 15: Large Array Size Performance

```bash
# OpenMP with large array
export OMP_NUM_THREADS=4
./openmp_bitonic 16384

# MPI with large array
mpirun -np 4 ./mpi_bitonic 16384
```

**What to capture:** Performance comparison with larger workloads

### Screenshot 16: Complete Performance Report

```bash
python3 performance_evaluation.py --all
```

**What to capture:** Terminal showing the complete automated performance evaluation process

## Screenshot Best Practices

### Terminal Setup

1. **Font Size:** Increase terminal font size to 14-16pt for readability
2. **Window Size:** Use full-screen or large window to show complete output
3. **Color Scheme:** Use high contrast scheme (dark background recommended)
4. **Clear Screen:** Run `clear` before each command to avoid clutter

### Content Guidelines

1. **Include Command:** Always show the command being executed
2. **Full Output:** Capture the complete program output including timing information
3. **Multiple Runs:** For consistency, you may want to run each test 2-3 times
4. **Error Handling:** If any errors occur, capture them for troubleshooting

### File Naming Convention

Save screenshots with descriptive names:

- `openmp_1_thread.png`
- `openmp_2_threads.png`
- `openmp_4_threads.png`
- `openmp_8_threads.png`
- `openmp_scaling_test.png`
- `openmp_performance_graphs.png`
- `mpi_1_process.png`
- `mpi_2_processes.png`
- `mpi_4_processes.png`
- `mpi_8_processes.png`
- `mpi_scaling_test.png`
- `mpi_performance_graphs.png`
- `system_info.png`
- `large_array_performance.png`

## Organization for Report

### For OpenMP Section:

1. Include screenshots 1-7
2. Add the generated CSV data tables
3. Include analysis of performance trends
4. Discuss optimal thread count findings

### For MPI Section:

1. Include screenshots 8-13
2. Add the generated CSV data tables
3. Include analysis of communication overhead
4. Discuss scaling efficiency

### Analysis Points to Address:

1. **Speedup Analysis:** Compare actual vs theoretical speedup
2. **Efficiency Trends:** Explain why efficiency decreases with more threads/processes
3. **Optimal Configuration:** Identify best thread/process count for different array sizes
4. **Scalability Limitations:** Discuss when adding more parallelism hurts performance
5. **Communication Overhead:** For MPI, analyze the impact of inter-process communication

## Automated Screenshot Script (Optional)

If you want to automate screenshot capture (macOS):

```bash
# Create automated screenshot script
cat > capture_screenshots.sh << 'EOF'
#!/bin/bash

# Function to take screenshot with delay
take_screenshot() {
    sleep 2
    screencapture -x "$1"
    sleep 1
}

echo "Starting automated screenshot capture..."
echo "Switch to terminal window in 5 seconds..."
sleep 5

# Take screenshots for each test
echo "Taking OpenMP screenshots..."
# You would need to manually run commands and trigger this script

EOF

chmod +x capture_screenshots.sh
```

## Final Notes

- **Resolution:** Use high resolution screenshots (at least 1920x1080)
- **Format:** Save as PNG for best quality in reports
- **Organization:** Create folders for `openmp_screenshots` and `mpi_screenshots`
- **Backup:** Keep original screenshots and create annotated versions for the report
- **Documentation:** For each screenshot, note the key observations and performance metrics

Remember to run the automated performance evaluation script to generate the quantitative data and graphs to complement your manual screenshots!
