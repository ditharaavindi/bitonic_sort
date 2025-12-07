# 3-Minute Demo Video Script - Bitonic Sort (OpenMP + MPI + CUDA)

**Type these commands manually while recording. Read the narrator lines naturally.**

---

## BEFORE YOU START

- Open terminal and navigate to: `/Users/ditharaavindi/Desktop/year\ 3\ sem\ 1/PC/assignment\ 3/dj/bitonic_sort`
- Have Google Colab open in second window/tab for CUDA portion
- Start screen recording (QuickTime/OBS/ScreenFlow)
- Maximize terminal window with large font (16pt+)

---

## SEGMENT 1: INTRODUCTION (0:00-0:25)

Clear the screen and introduce the demo:

```bash
clear
echo "=========================================="
echo "BITONIC SORT - Parallel Computing Demo"
echo "=========================================="
echo ""
echo "Three parallel implementations:"
echo "  1. OpenMP    - Shared-memory (local machine)"
echo "  2. MPI       - Distributed-memory (multiple nodes)"
echo "  3. CUDA      - GPU acceleration (Google Colab)"
echo ""
echo "Input: 50 unsorted integers"
echo "Algorithm: O(n log² n) bitonic sort network"
echo "=========================================="
```

**📺 READ THIS ALOUD:**

> "Welcome! Today I'm demonstrating bitonic sort using three parallel paradigms: OpenMP for shared-memory systems, MPI for distributed clusters, and CUDA for GPU acceleration. Each has different performance characteristics and best-use cases. Let's see them in action!"

---

## SEGMENT 2: OPENMP EXECUTION (0:25-1:35)

Show the OpenMP implementation:

```bash
echo ""
echo "=== OPENMP - Shared Memory Parallelism ==="
echo "Testing with 1, 2, 4, 8, and 16 threads"
echo ""
```

**📺 READ THIS ALOUD (before running):**

> "First is OpenMP. It uses compiler directives to parallelize loops across threads on a shared-memory system. All threads access the same memory, which is ideal for bitonic sort. We'll test with 1 to 16 threads to see scaling efficiency."

Run OpenMP (will take ~1-2 minutes):

```bash
bash run_openmp.sh
```

**📺 READ THIS ALOUD (while it runs):**

> "OpenMP is running with 1, 2, 4, 8, and 16 threads. Notice how execution time doesn't always decrease with more threads on small datasets—that's parallelization overhead. Thread creation and synchronization cost more than the actual work. On larger datasets, this overhead becomes negligible and speedup is excellent."

Show results:

```bash
echo ""
echo "=== SORTED OUTPUT (OpenMP) ==="
cat OutputFiles/openmp_output.txt
echo ""
echo "=== TIMING RESULTS (OpenMP) ==="
cat OutputFiles/openmp_times.txt
```

**📺 READ THIS ALOUD (after results display):**

> "Perfect! All 50 integers are correctly sorted. The timing shows thread overhead on small datasets. This is key: parallelization only pays off when computation work is large. On bigger datasets, OpenMP delivers excellent speedup."

---

## SEGMENT 3: MPI EXECUTION (1:35-2:35)

Show the MPI implementation:

```bash
echo ""
echo "=== MPI - Distributed Memory Parallelism ==="
echo "Testing with 1, 2, 4, 8, and 16 processes"
echo ""
```

**📺 READ THIS ALOUD (before running):**

> "Now MPI—Message Passing Interface. Different from OpenMP: each process has private memory and communicates via explicit messages. Perfect for distributed systems across multiple computers. Data is scattered, each process sorts its portion, then results are merged. MPI has more overhead but scales to thousands of nodes."

Run MPI (will take ~1-2 minutes):

```bash
bash run_mpi.sh
```

**📺 READ THIS ALOUD (while it runs):**

> "MPI is executing with 16 processes. Notice the --oversubscribe flag because we have fewer cores than processes. Communication overhead is higher than OpenMP since messages must cross process boundaries. But MPI's scalability to thousands of nodes across networks is unmatched."

Show results:

```bash
echo ""
echo "=== SORTED OUTPUT (MPI) ==="
cat OutputFiles/mpi_output.txt
echo ""
echo "=== TIMING RESULTS (MPI) ==="
cat OutputFiles/mpi_times.txt
```

**📺 READ THIS ALOUD (after results display):**

> "Excellent! MPI output matches OpenMP—both implementations are correct. Timing shows more variability due to process scheduling overhead. On a real cluster with proper hardware, MPI scales beautifully for massive distributed datasets."

---

## SEGMENT 4: VERIFICATION & COMPARISON (2:35-2:45)

Verify all implementations match:

```bash
echo ""
echo "=== CORRECTNESS VERIFICATION ==="
if [ "$(cat OutputFiles/openmp_output.txt)" = "$(cat OutputFiles/mpi_output.txt)" ]; then
    echo "✓ SUCCESS: OpenMP and MPI outputs are identical!"
else
    echo "✗ ERROR: Outputs differ"
fi
```

**📺 READ THIS ALOUD:**

> "Both implementations produce identical correct results. Different parallelization strategies, same correct solution. Choose based on hardware: OpenMP for shared-memory, MPI for distributed clusters."

---

## SEGMENT 5: CUDA DEMO - GOOGLE COLAB (2:45-3:00)

**Switch to Google Colab window/tab** and show CUDA execution:

Display Colab notebook showing:

```bash
echo ""
echo "=== CUDA - GPU Acceleration (Google Colab) ==="
echo ""
echo "Link to Colab notebook: Untitled7.ipynb"
echo ""
echo "CUDA brings GPU parallelism:"
echo "  - Thousands of threads per GPU block"
echo "  - Massive data parallelism"
echo "  - Optimal for highly parallel algorithms"
echo ""
```

**📺 READ THIS ALOUD (pointing to Colab):**

> "Finally, CUDA for GPU acceleration. GPUs have thousands of processors executing the same code on different data—perfect for bitonic sort. CUDA launches thousands of threads simultaneously across GPU cores for massive throughput. This Colab notebook shows GPU bitonic sort. CUDA trades portability for raw performance on data-parallel algorithms."

**If recording Colab live:**

Run Colab cells showing:

- CUDA setup and version check
- Compilation of CUDA bitonic sort
- Execution on sample data
- Timing comparison with CPU versions

---

## SEGMENT 6: CONCLUSION (2:55-3:00)

```bash
echo ""
echo "=========================================="
echo "SUMMARY"
echo "=========================================="
echo ""
echo "OpenMP:  Shared-memory, simple, best for local systems"
echo "MPI:     Distributed-memory, scalable to clusters"
echo "CUDA:    GPU acceleration, maximum parallelism"
echo ""
echo "Same algorithm, three paradigms"
echo "Different strengths, choose based on resources"
echo ""
echo "=========================================="
```

**📺 READ THIS ALOUD (final conclusion):**

> "That's our parallel bitonic sort demonstration across three paradigms. OpenMP for shared-memory simplicity, MPI for distributed scalability, CUDA for GPU performance. Bitonic sort's deterministic structure makes it ideal for all three. Choose based on your hardware and scale requirements. Thank you for watching!"

---

## TIMING GUIDE

| Segment          | Duration  | Task                                  |
| ---------------- | --------- | ------------------------------------- |
| **Intro**        | 0:00-0:25 | Welcome + introduce 3 paradigms       |
| **OpenMP**       | 0:25-1:35 | Run openMP, show results & timing     |
| **MPI**          | 1:35-2:35 | Run MPI, show results & timing        |
| **Verification** | 2:35-2:45 | Compare outputs, confirm correctness  |
| **CUDA**         | 2:45-3:00 | Show Google Colab CUDA implementation |
| **Conclusion**   | 2:55-3:00 | Summary & final thoughts              |

---

## RECORDING TIPS

1. **Don't rush** - let output appear naturally, pause after commands
2. **Speak clearly** - narration should be calm and professional
3. **Point at screen** - use cursor/pointer when referring to data
4. **Pause for emphasis** - pause briefly before key points
5. **Use terminal zoom** - make code readable (16pt+ font)
6. **Edit in post** - cut long compilation waits, keep narration flowing
7. **Test audio** - record a few seconds before starting to test microphone

---

## GOOGLE COLAB CUDA LINK

Your CUDA notebook is available here:
**File:** `Untitled7.ipynb - Colab.pdf`

To record Colab execution:

1. Open Colab notebook in browser
2. Share your screen with recording software
3. Run cells showing:
   - `!nvcc --version` and `!nvidia-smi` (CUDA setup)
   - Compile and run CUDA bitonic sort
   - Compare execution times with CPU versions

---

## FINAL CHECKLIST

- [ ] Terminal font is large (16pt or bigger)
- [ ] All three implementations compile and run successfully
- [ ] Audio microphone is tested and working
- [ ] Recording resolution is 1080p or higher
- [ ] Google Colab tab ready for CUDA portion
- [ ] Total video length is approximately 3 minutes
- [ ] No background noise or distractions
- [ ] Script saved for reference during recording

**Ready to record! Hit the red button and go! 🎥**
