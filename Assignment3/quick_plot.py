#!/usr/bin/env python3
"""
Quick Performance Plotter for Bitonic Sort

This is a simplified version that you can easily modify with your own timing data.
Just replace the values in the data dictionary below with your actual measurements.

Author: Parallel Computing Assignment 3
Date: December 2025

Usage:
    python quick_plot.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def create_performance_plots():
    """Create performance plots with manual data entry"""
    
    # 📊 REPLACE THIS DATA WITH YOUR ACTUAL MEASUREMENTS
    # ================================================
    
    # Array sizes tested
    array_sizes = [256, 512, 1024, 2048, 4096, 8192]
    
    # Execution times in milliseconds - REPLACE WITH YOUR DATA
    execution_times = {
        'Serial': [0.5, 2.1, 8.5, 34.2, 137.8, 551.2],        # Replace with your serial times
        'OpenMP_2': [0.4, 1.2, 4.8, 19.1, 76.4, 305.6],       # Replace with OpenMP 2 threads
        'OpenMP_4': [0.3, 0.8, 2.9, 11.7, 46.8, 187.2],       # Replace with OpenMP 4 threads
        'OpenMP_8': [0.3, 0.7, 2.5, 9.8, 39.2, 156.8],        # Replace with OpenMP 8 threads
        'MPI_2': [0.5, 1.4, 5.2, 20.8, 83.2, 332.8],          # Replace with MPI 2 processes
        'MPI_4': [0.4, 0.9, 3.1, 12.4, 49.6, 198.4],          # Replace with MPI 4 processes
        'MPI_8': [0.4, 0.8, 2.7, 10.8, 43.2, 172.8],          # Replace with MPI 8 processes
        'CUDA': [0.1, 0.2, 0.5, 1.2, 2.8, 6.1]                # Replace with CUDA GPU times
    }
    
    # ================================================
    # END OF DATA SECTION - NO NEED TO MODIFY BELOW
    # ================================================
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 12))
    
    # Plot 1: Execution Time Comparison
    ax1 = plt.subplot(2, 3, 1)
    for impl, times in execution_times.items():
        if len(times) == len(array_sizes):
            plt.plot(array_sizes, times, 'o-', label=impl, linewidth=2, markersize=6)
    
    plt.xlabel('Array Size')
    plt.ylabel('Execution Time (ms)')
    plt.title('Execution Time vs Array Size')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.xscale('log')
    
    # Plot 2: Speedup Analysis
    ax2 = plt.subplot(2, 3, 2)
    serial_times = execution_times['Serial']
    
    for impl, times in execution_times.items():
        if impl != 'Serial' and len(times) == len(array_sizes):
            speedup = [serial_times[i] / times[i] for i in range(len(times))]
            plt.plot(array_sizes, speedup, 's-', label=f'{impl} Speedup', linewidth=2, markersize=6)
    
    plt.xlabel('Array Size')
    plt.ylabel('Speedup vs Serial')
    plt.title('Speedup Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    
    # Plot 3: Thread Scaling (OpenMP)
    ax3 = plt.subplot(2, 3, 3)
    thread_counts = [2, 4, 8]
    target_size_idx = 4  # Index for 4096 elements
    
    openmp_times_for_scaling = []
    for threads in thread_counts:
        impl_key = f'OpenMP_{threads}'
        if impl_key in execution_times:
            openmp_times_for_scaling.append(execution_times[impl_key][target_size_idx])
    
    plt.plot(thread_counts, openmp_times_for_scaling, 'ro-', linewidth=2, markersize=8, label='OpenMP')
    plt.xlabel('Number of Threads')
    plt.ylabel('Execution Time (ms)')
    plt.title(f'OpenMP Thread Scaling (Size: {array_sizes[target_size_idx]})')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    # Plot 4: Process Scaling (MPI)
    ax4 = plt.subplot(2, 3, 4)
    process_counts = [2, 4, 8]
    
    mpi_times_for_scaling = []
    for procs in process_counts:
        impl_key = f'MPI_{procs}'
        if impl_key in execution_times:
            mpi_times_for_scaling.append(execution_times[impl_key][target_size_idx])
    
    plt.plot(process_counts, mpi_times_for_scaling, 'bs-', linewidth=2, markersize=8, label='MPI')
    plt.xlabel('Number of Processes')
    plt.ylabel('Execution Time (ms)')
    plt.title(f'MPI Process Scaling (Size: {array_sizes[target_size_idx]})')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    # Plot 5: Implementation Comparison (Bar Chart)
    ax5 = plt.subplot(2, 3, 5)
    target_size_idx = 4  # 4096 elements
    
    impl_names = []
    impl_times = []
    
    for impl, times in execution_times.items():
        impl_names.append(impl.replace('_', ' '))
        impl_times.append(times[target_size_idx])
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(impl_names)))
    bars = plt.bar(impl_names, impl_times, color=colors, alpha=0.7, edgecolor='black')
    
    # Add value labels on bars
    for bar, time in zip(bars, impl_times):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                f'{time:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.ylabel('Execution Time (ms)')
    plt.title(f'Implementation Comparison (Array Size: {array_sizes[target_size_idx]})')
    plt.yscale('log')
    plt.xticks(rotation=45, ha='right')
    
    # Plot 6: CUDA Advantage
    ax6 = plt.subplot(2, 3, 6)
    
    if 'CUDA' in execution_times:
        cuda_speedup = [serial_times[i] / execution_times['CUDA'][i] for i in range(len(array_sizes))]
        plt.plot(array_sizes, cuda_speedup, 'go-', linewidth=3, markersize=8, label='CUDA vs Serial')
        
        # Also plot best CPU implementation
        best_cpu_times = []
        for i in range(len(array_sizes)):
            cpu_times = [execution_times[impl][i] for impl in execution_times.keys() 
                        if impl != 'CUDA' and impl != 'Serial']
            best_cpu_times.append(min(cpu_times))
        
        cuda_vs_best_cpu = [best_cpu_times[i] / execution_times['CUDA'][i] for i in range(len(array_sizes))]
        plt.plot(array_sizes, cuda_vs_best_cpu, 'ro-', linewidth=3, markersize=8, label='CUDA vs Best CPU')
    
    plt.xlabel('Array Size')
    plt.ylabel('Speedup')
    plt.title('CUDA Performance Advantage')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    
    plt.tight_layout()
    plt.savefig('bitonic_sort_performance.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print summary statistics
    print("\n📊 PERFORMANCE ANALYSIS SUMMARY")
    print("=" * 40)
    
    target_size = array_sizes[target_size_idx]
    print(f"\nExecution times for array size {target_size}:")
    for impl, times in execution_times.items():
        print(f"  {impl:12s}: {times[target_size_idx]:8.2f} ms")
    
    print(f"\nSpeedup vs Serial (array size {target_size}):")
    serial_time = execution_times['Serial'][target_size_idx]
    for impl, times in execution_times.items():
        if impl != 'Serial':
            speedup = serial_time / times[target_size_idx]
            print(f"  {impl:12s}: {speedup:6.2f}x")
    
    if 'CUDA' in execution_times:
        print(f"\nCUDA performance highlights:")
        for i, size in enumerate(array_sizes):
            cuda_speedup = execution_times['Serial'][i] / execution_times['CUDA'][i]
            print(f"  Size {size:5d}: {cuda_speedup:6.1f}x faster than serial")


def main():
    """Main function"""
    print("🎯 Quick Performance Plotter for Bitonic Sort")
    print("=" * 45)
    print("\n📝 To use this script:")
    print("1. Run your bitonic sort implementations")
    print("2. Record the execution times")
    print("3. Replace the data in the 'execution_times' dictionary")
    print("4. Run this script to generate plots")
    print("\n🔄 Generating plots with sample data...")
    
    create_performance_plots()
    
    print("\n✅ Performance plots generated!")
    print("📈 Plot saved as 'bitonic_sort_performance.png'")


if __name__ == "__main__":
    main()