# Performance Evaluation Instructions

## Quick Start Guide

### 1. Run Automated Performance Tests

For **OpenMP only**:
```bash
"/Users/ditharaavindi/Desktop/year 3 sem 1/PC/assignment 3/dj/bitonic_sort/.venv/bin/python" performance_evaluation.py --openmp
```

For **MPI only**:
```bash
"/Users/ditharaavindi/Desktop/year 3 sem 1/PC/assignment 3/dj/bitonic_sort/.venv/bin/python" performance_evaluation.py --mpi
```

For **Both OpenMP and MPI**:
```bash
"/Users/ditharaavindi/Desktop/year 3 sem 1/PC/assignment 3/dj/bitonic_sort/.venv/bin/python" performance_evaluation.py --all
```

### 2. Take Manual Screenshots

Run the screenshot helper:
```bash
"/Users/ditharaavindi/Desktop/year 3 sem 1/PC/assignment 3/dj/bitonic_sort/.venv/bin/python" capture_screenshots.py
```

Or follow the manual guide in `screenshot_guide.md`

### 3. Generated Files

After running the performance evaluation, you'll get:

#### OpenMP Results:
- `openmp_performance_results.csv` - Raw data
- `openmp_performance_analysis.png` - Performance graphs
- Performance report with analysis

#### MPI Results:
- `mpi_performance_results.csv` - Raw data  
- `mpi_performance_analysis.png` - Performance graphs
- Performance report with analysis

### 4. What You'll Get for Your Report

#### OpenMP Section (6 marks):
1. **Execution Time vs Threads Graph** - Shows how performance changes with thread count
2. **Speedup vs Threads Graph** - Shows parallel efficiency 
3. **Screenshots** - Terminal outputs for different thread counts
4. **Analysis** - Automated performance analysis and recommendations

#### MPI Section (6 marks):
1. **Execution Time vs Processes Graph** - Shows how performance scales with processes
2. **Speedup vs Processes Graph** - Shows distributed computing efficiency
3. **Screenshots** - Terminal outputs for different process counts  
4. **Analysis** - Communication overhead and scalability analysis

### 5. Quick Manual Test

Test OpenMP quickly:
```bash
cd OpenMP
export OMP_NUM_THREADS=1 && ./openmp_bitonic 2048
export OMP_NUM_THREADS=4 && ./openmp_bitonic 2048
export OMP_NUM_THREADS=8 && ./openmp_bitonic 2048
```

Test MPI quickly:
```bash
cd MPI
mpirun -np 1 ./mpi_bitonic 2048
mpirun -np 4 ./mpi_bitonic 2048  
mpirun -np 8 ./mpi_bitonic 2048
```

### 6. Troubleshooting

If you get Python errors, use the full path:
```bash
"/Users/ditharaavindi/Desktop/year 3 sem 1/PC/assignment 3/dj/bitonic_sort/.venv/bin/python" performance_evaluation.py --all
```

If builds fail:
```bash
cd OpenMP && make clean && make
cd ../MPI && make clean && make
```

### 7. Expected Results

**Good OpenMP Performance:**
- Speedup should increase with threads up to your CPU core count
- Best performance typically at 4-8 threads on most systems
- Efficiency should be 70%+ for small thread counts

**Good MPI Performance:**
- Should show scaling benefits up to 4-8 processes
- Communication overhead becomes visible with more processes
- Efficiency depends on problem size and network latency

The automated system will generate all the data and graphs you need for a comprehensive performance evaluation!