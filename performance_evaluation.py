#!/usr/bin/env python3
# Use the virtual environment: .venv/bin/python
"""
Performance Evaluation Script for Bitonic Sort Implementations
Automated testing and visualization for OpenMP and MPI implementations

Usage:
    python3 performance_evaluation.py --openmp
    python3 performance_evaluation.py --mpi
    python3 performance_evaluation.py --all

Author: Parallel Computing Assignment 3
Date: December 2025
"""

import subprocess
import time
import csv
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
import sys
from datetime import datetime

class PerformanceEvaluator:
    def __init__(self):
        self.results = {}
        self.array_sizes = [1024, 2048, 4096, 8192]
        self.thread_counts = [1, 2, 4, 8, 16]
        self.process_counts = [1, 2, 4, 8, 16]
        self.repetitions = 5  # Number of times to run each test for averaging
        
    def run_openmp_test(self, threads, array_size):
        """Run OpenMP implementation with specified threads and array size"""
        try:
            env = os.environ.copy()
            env['OMP_NUM_THREADS'] = str(threads)
            
            cmd = ['./openmp_bitonic', str(array_size)]
            result = subprocess.run(
                cmd, 
                cwd='OpenMP',
                env=env,
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"OpenMP test failed: {result.stderr}")
                return None
                
            # Parse execution time from output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Execution Time:' in line:
                    time_str = line.split(':')[1].strip().replace('ms', '').strip()
                    return float(time_str)
            return None
            
        except Exception as e:
            print(f"Error running OpenMP test: {e}")
            return None
    
    def run_mpi_test(self, processes, array_size):
        """Run MPI implementation with specified processes and array size"""
        try:
            cmd = ['mpirun', '-np', str(processes), './mpi_bitonic', str(array_size)]
            result = subprocess.run(
                cmd,
                cwd='MPI', 
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"MPI test failed: {result.stderr}")
                return None
                
            # Parse execution time from output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Total Execution Time:' in line or 'Execution Time:' in line:
                    time_str = line.split(':')[1].strip().replace('ms', '').strip()
                    return float(time_str)
            return None
            
        except Exception as e:
            print(f"Error running MPI test: {e}")
            return None
    
    def build_implementations(self):
        """Build all implementations before testing"""
        print("Building implementations...")
        
        # Build OpenMP
        try:
            subprocess.run(['make', 'clean'], cwd='OpenMP', check=True, capture_output=True)
            subprocess.run(['make'], cwd='OpenMP', check=True, capture_output=True)
            print("✓ OpenMP implementation built successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to build OpenMP: {e}")
            return False
            
        # Build MPI
        try:
            subprocess.run(['make', 'clean'], cwd='MPI', check=True, capture_output=True)
            subprocess.run(['make'], cwd='MPI', check=True, capture_output=True)
            print("✓ MPI implementation built successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to build MPI: {e}")
            return False
            
        return True
    
    def evaluate_openmp(self):
        """Comprehensive OpenMP performance evaluation"""
        print("\n=== OpenMP Performance Evaluation ===")
        
        openmp_results = {}
        
        for array_size in self.array_sizes:
            print(f"\nTesting array size: {array_size}")
            openmp_results[array_size] = {}
            
            for threads in self.thread_counts:
                print(f"  Testing {threads} threads...", end=' ')
                
                times = []
                for rep in range(self.repetitions):
                    exec_time = self.run_openmp_test(threads, array_size)
                    if exec_time is not None:
                        times.append(exec_time)
                
                if times:
                    avg_time = np.mean(times)
                    std_time = np.std(times)
                    openmp_results[array_size][threads] = {
                        'avg_time': avg_time,
                        'std_time': std_time,
                        'times': times
                    }
                    print(f"Avg: {avg_time:.2f}ms (±{std_time:.2f})")
                else:
                    print("FAILED")
                    openmp_results[array_size][threads] = None
        
        self.results['openmp'] = openmp_results
        self.save_openmp_results()
        self.plot_openmp_results()
        
    def evaluate_mpi(self):
        """Comprehensive MPI performance evaluation"""
        print("\n=== MPI Performance Evaluation ===")
        
        mpi_results = {}
        
        for array_size in self.array_sizes:
            print(f"\nTesting array size: {array_size}")
            mpi_results[array_size] = {}
            
            for processes in self.process_counts:
                print(f"  Testing {processes} processes...", end=' ')
                
                times = []
                for rep in range(self.repetitions):
                    exec_time = self.run_mpi_test(processes, array_size)
                    if exec_time is not None:
                        times.append(exec_time)
                
                if times:
                    avg_time = np.mean(times)
                    std_time = np.std(times)
                    mpi_results[array_size][processes] = {
                        'avg_time': avg_time,
                        'std_time': std_time,
                        'times': times
                    }
                    print(f"Avg: {avg_time:.2f}ms (±{std_time:.2f})")
                else:
                    print("FAILED")
                    mpi_results[array_size][processes] = None
        
        self.results['mpi'] = mpi_results
        self.save_mpi_results()
        self.plot_mpi_results()
    
    def save_openmp_results(self):
        """Save OpenMP results to CSV"""
        with open('openmp_performance_results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            header = ['Array_Size'] + [f'{t}_threads' for t in self.thread_counts]
            writer.writerow(header)
            
            # Data
            for array_size in self.array_sizes:
                row = [array_size]
                for threads in self.thread_counts:
                    result = self.results['openmp'][array_size].get(threads)
                    if result and result is not None:
                        row.append(f"{result['avg_time']:.2f}")
                    else:
                        row.append('N/A')
                writer.writerow(row)
        
        print("OpenMP results saved to 'openmp_performance_results.csv'")
    
    def save_mpi_results(self):
        """Save MPI results to CSV"""
        with open('mpi_performance_results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            header = ['Array_Size'] + [f'{p}_processes' for p in self.process_counts]
            writer.writerow(header)
            
            # Data
            for array_size in self.array_sizes:
                row = [array_size]
                for processes in self.process_counts:
                    result = self.results['mpi'][array_size].get(processes)
                    if result and result is not None:
                        row.append(f"{result['avg_time']:.2f}")
                    else:
                        row.append('N/A')
                writer.writerow(row)
        
        print("MPI results saved to 'mpi_performance_results.csv'")
    
    def plot_openmp_results(self):
        """Create comprehensive OpenMP performance plots"""
        if 'openmp' not in self.results:
            return
            
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('OpenMP Performance Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Execution Time vs Number of Threads
        for array_size in self.array_sizes:
            threads_list = []
            times_list = []
            errors_list = []
            
            for threads in self.thread_counts:
                result = self.results['openmp'][array_size].get(threads)
                if result and result is not None:
                    threads_list.append(threads)
                    times_list.append(result['avg_time'])
                    errors_list.append(result['std_time'])
            
            if threads_list:
                ax1.errorbar(threads_list, times_list, yerr=errors_list, 
                           marker='o', label=f'Array Size: {array_size}', linewidth=2)
        
        ax1.set_xlabel('Number of Threads')
        ax1.set_ylabel('Execution Time (ms)')
        ax1.set_title('Execution Time vs Number of Threads')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Speedup vs Number of Threads
        for array_size in self.array_sizes:
            threads_list = []
            speedup_list = []
            
            baseline_time = None
            for threads in self.thread_counts:
                result = self.results['openmp'][array_size].get(threads)
                if result and result is not None:
                    if baseline_time is None:  # Use single thread as baseline
                        baseline_time = result['avg_time']
                    
                    threads_list.append(threads)
                    speedup = baseline_time / result['avg_time']
                    speedup_list.append(speedup)
            
            if threads_list:
                ax2.plot(threads_list, speedup_list, marker='o', 
                        label=f'Array Size: {array_size}', linewidth=2)
        
        # Add ideal speedup line
        ax2.plot(self.thread_counts, self.thread_counts, '--', 
                color='red', label='Ideal Speedup', alpha=0.7)
        
        ax2.set_xlabel('Number of Threads')
        ax2.set_ylabel('Speedup')
        ax2.set_title('Speedup vs Number of Threads')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Efficiency vs Number of Threads
        for array_size in self.array_sizes:
            threads_list = []
            efficiency_list = []
            
            baseline_time = None
            for threads in self.thread_counts:
                result = self.results['openmp'][array_size].get(threads)
                if result and result is not None:
                    if baseline_time is None:
                        baseline_time = result['avg_time']
                    
                    threads_list.append(threads)
                    speedup = baseline_time / result['avg_time']
                    efficiency = (speedup / threads) * 100
                    efficiency_list.append(efficiency)
            
            if threads_list:
                ax3.plot(threads_list, efficiency_list, marker='o', 
                        label=f'Array Size: {array_size}', linewidth=2)
        
        ax3.set_xlabel('Number of Threads')
        ax3.set_ylabel('Parallel Efficiency (%)')
        ax3.set_title('Parallel Efficiency vs Number of Threads')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Scalability Analysis
        array_sizes_plot = []
        best_speedups = []
        
        for array_size in self.array_sizes:
            max_speedup = 0
            baseline_time = None
            
            for threads in self.thread_counts:
                result = self.results['openmp'][array_size].get(threads)
                if result and result is not None:
                    if baseline_time is None:
                        baseline_time = result['avg_time']
                    speedup = baseline_time / result['avg_time']
                    max_speedup = max(max_speedup, speedup)
            
            if max_speedup > 0:
                array_sizes_plot.append(array_size)
                best_speedups.append(max_speedup)
        
        ax4.bar(range(len(array_sizes_plot)), best_speedups, color='skyblue', alpha=0.7)
        ax4.set_xlabel('Array Size')
        ax4.set_ylabel('Best Speedup Achieved')
        ax4.set_title('Best Speedup by Array Size')
        ax4.set_xticks(range(len(array_sizes_plot)))
        ax4.set_xticklabels(array_sizes_plot)
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('openmp_performance_analysis.png', dpi=300, bbox_inches='tight')
        print("OpenMP performance plots saved to 'openmp_performance_analysis.png'")
        plt.show()
    
    def plot_mpi_results(self):
        """Create comprehensive MPI performance plots"""
        if 'mpi' not in self.results:
            return
            
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('MPI Performance Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Execution Time vs Number of Processes
        for array_size in self.array_sizes:
            processes_list = []
            times_list = []
            errors_list = []
            
            for processes in self.process_counts:
                result = self.results['mpi'][array_size].get(processes)
                if result and result is not None:
                    processes_list.append(processes)
                    times_list.append(result['avg_time'])
                    errors_list.append(result['std_time'])
            
            if processes_list:
                ax1.errorbar(processes_list, times_list, yerr=errors_list, 
                           marker='s', label=f'Array Size: {array_size}', linewidth=2)
        
        ax1.set_xlabel('Number of Processes')
        ax1.set_ylabel('Execution Time (ms)')
        ax1.set_title('Execution Time vs Number of Processes')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Speedup vs Number of Processes
        for array_size in self.array_sizes:
            processes_list = []
            speedup_list = []
            
            baseline_time = None
            for processes in self.process_counts:
                result = self.results['mpi'][array_size].get(processes)
                if result and result is not None:
                    if baseline_time is None:  # Use single process as baseline
                        baseline_time = result['avg_time']
                    
                    processes_list.append(processes)
                    speedup = baseline_time / result['avg_time']
                    speedup_list.append(speedup)
            
            if processes_list:
                ax2.plot(processes_list, speedup_list, marker='s', 
                        label=f'Array Size: {array_size}', linewidth=2)
        
        # Add ideal speedup line
        ax2.plot(self.process_counts, self.process_counts, '--', 
                color='red', label='Ideal Speedup', alpha=0.7)
        
        ax2.set_xlabel('Number of Processes')
        ax2.set_ylabel('Speedup')
        ax2.set_title('Speedup vs Number of Processes')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Efficiency vs Number of Processes
        for array_size in self.array_sizes:
            processes_list = []
            efficiency_list = []
            
            baseline_time = None
            for processes in self.process_counts:
                result = self.results['mpi'][array_size].get(processes)
                if result and result is not None:
                    if baseline_time is None:
                        baseline_time = result['avg_time']
                    
                    processes_list.append(processes)
                    speedup = baseline_time / result['avg_time']
                    efficiency = (speedup / processes) * 100
                    efficiency_list.append(efficiency)
            
            if processes_list:
                ax3.plot(processes_list, efficiency_list, marker='s', 
                        label=f'Array Size: {array_size}', linewidth=2)
        
        ax3.set_xlabel('Number of Processes')
        ax3.set_ylabel('Parallel Efficiency (%)')
        ax3.set_title('Parallel Efficiency vs Number of Processes')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Communication Overhead Analysis
        array_sizes_plot = []
        comm_overheads = []
        
        for array_size in self.array_sizes:
            if array_size in self.results['mpi']:
                single_proc = self.results['mpi'][array_size].get(1)
                multi_proc = self.results['mpi'][array_size].get(max(self.process_counts))
                
                if single_proc and multi_proc and single_proc is not None and multi_proc is not None:
                    # Estimate communication overhead
                    ideal_time = single_proc['avg_time'] / max(self.process_counts)
                    actual_time = multi_proc['avg_time']
                    overhead = ((actual_time - ideal_time) / actual_time) * 100
                    
                    array_sizes_plot.append(array_size)
                    comm_overheads.append(max(0, overhead))  # Ensure non-negative
        
        if array_sizes_plot:
            ax4.bar(range(len(array_sizes_plot)), comm_overheads, color='lightcoral', alpha=0.7)
            ax4.set_xlabel('Array Size')
            ax4.set_ylabel('Communication Overhead (%)')
            ax4.set_title('Communication Overhead by Array Size')
            ax4.set_xticks(range(len(array_sizes_plot)))
            ax4.set_xticklabels(array_sizes_plot)
            ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('mpi_performance_analysis.png', dpi=300, bbox_inches='tight')
        print("MPI performance plots saved to 'mpi_performance_analysis.png'")
        plt.show()
    
    def generate_performance_report(self):
        """Generate a comprehensive performance report"""
        report_filename = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_filename, 'w') as f:
            f.write("# Bitonic Sort Performance Evaluation Report\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Test Configuration\n\n")
            f.write(f"- Array Sizes Tested: {self.array_sizes}\n")
            f.write(f"- Thread Counts (OpenMP): {self.thread_counts}\n")
            f.write(f"- Process Counts (MPI): {self.process_counts}\n")
            f.write(f"- Repetitions per test: {self.repetitions}\n\n")
            
            # OpenMP Results Summary
            if 'openmp' in self.results:
                f.write("## OpenMP Performance Summary\n\n")
                f.write("| Array Size | Best Thread Count | Best Time (ms) | Best Speedup |\n")
                f.write("|------------|-------------------|----------------|---------------|\n")
                
                for array_size in self.array_sizes:
                    best_time = float('inf')
                    best_threads = 1
                    baseline_time = None
                    
                    for threads in self.thread_counts:
                        result = self.results['openmp'][array_size].get(threads)
                        if result and result is not None:
                            if baseline_time is None:
                                baseline_time = result['avg_time']
                            if result['avg_time'] < best_time:
                                best_time = result['avg_time']
                                best_threads = threads
                    
                    if baseline_time:
                        speedup = baseline_time / best_time
                        f.write(f"| {array_size} | {best_threads} | {best_time:.2f} | {speedup:.2f}x |\n")
                
                f.write("\n")
            
            # MPI Results Summary
            if 'mpi' in self.results:
                f.write("## MPI Performance Summary\n\n")
                f.write("| Array Size | Best Process Count | Best Time (ms) | Best Speedup |\n")
                f.write("|------------|-------------------|----------------|---------------|\n")
                
                for array_size in self.array_sizes:
                    best_time = float('inf')
                    best_processes = 1
                    baseline_time = None
                    
                    for processes in self.process_counts:
                        result = self.results['mpi'][array_size].get(processes)
                        if result and result is not None:
                            if baseline_time is None:
                                baseline_time = result['avg_time']
                            if result['avg_time'] < best_time:
                                best_time = result['avg_time']
                                best_processes = processes
                    
                    if baseline_time:
                        speedup = baseline_time / best_time
                        f.write(f"| {array_size} | {best_processes} | {best_time:.2f} | {speedup:.2f}x |\n")
                
                f.write("\n")
            
            f.write("## Files Generated\n\n")
            f.write("- `openmp_performance_results.csv` - Raw OpenMP performance data\n")
            f.write("- `mpi_performance_results.csv` - Raw MPI performance data\n")
            f.write("- `openmp_performance_analysis.png` - OpenMP performance visualizations\n")
            f.write("- `mpi_performance_analysis.png` - MPI performance visualizations\n")
            f.write("- `screenshot_guide.md` - Guide for taking manual screenshots\n\n")
            
            f.write("## Analysis Notes\n\n")
            f.write("- Speedup is calculated relative to single thread/process performance\n")
            f.write("- Efficiency = (Speedup / Number of threads or processes) × 100%\n")
            f.write("- Each data point is the average of multiple runs with error bars\n")
            f.write("- Communication overhead estimated for MPI based on ideal vs actual performance\n")
        
        print(f"Comprehensive performance report saved to '{report_filename}'")

def main():
    parser = argparse.ArgumentParser(description='Performance Evaluation for Bitonic Sort')
    parser.add_argument('--openmp', action='store_true', help='Evaluate OpenMP implementation')
    parser.add_argument('--mpi', action='store_true', help='Evaluate MPI implementation')
    parser.add_argument('--all', action='store_true', help='Evaluate all implementations')
    
    args = parser.parse_args()
    
    evaluator = PerformanceEvaluator()
    
    # Build implementations
    if not evaluator.build_implementations():
        print("Failed to build implementations. Exiting.")
        sys.exit(1)
    
    # Run evaluations
    if args.all or args.openmp:
        evaluator.evaluate_openmp()
    
    if args.all or args.mpi:
        evaluator.evaluate_mpi()
    
    # Generate report
    evaluator.generate_performance_report()
    
    print("\n=== Performance Evaluation Complete ===")
    print("Check the generated files for detailed results and visualizations.")

if __name__ == "__main__":
    main()