#!/usr/bin/env python3
"""
Data Collection Helper for Bitonic Sort Performance Analysis

This script helps you systematically collect performance data from
all bitonic sort implementations and saves it in CSV format for visualization.

Author: Parallel Computing Assignment 3
Date: December 2025

Usage:
    python collect_performance_data.py
"""

import subprocess
import csv
import time
import os
import sys
from pathlib import Path

class PerformanceCollector:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.results = []
        self.array_sizes = [256, 512, 1024, 2048, 4096, 8192]
        
    def run_command(self, command, cwd=None, timeout=60):
        """Run a command and capture its output"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                cwd=cwd
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", -1
        except Exception as e:
            return "", str(e), -1
    
    def extract_execution_time(self, output):
        """Extract execution time from program output"""
        lines = output.split('\n')
        for line in lines:
            if 'Execution Time:' in line or 'GPU Kernel Time:' in line:
                try:
                    # Extract number before 'ms'
                    parts = line.split(':')[1].strip()
                    time_str = parts.split('ms')[0].strip()
                    return float(time_str)
                except (ValueError, IndexError):
                    continue
        return None
    
    def collect_serial_data(self):
        """Collect data from serial implementation"""
        print("🔄 Collecting Serial implementation data...")
        serial_dir = self.base_dir / "Serial"
        
        # Build if needed
        if not (serial_dir / "serial_bitonic").exists():
            print("  📦 Building serial implementation...")
            stdout, stderr, code = self.run_command("make", cwd=serial_dir)
            if code != 0:
                print(f"  ❌ Build failed: {stderr}")
                return {}
        
        results = {}
        for size in self.array_sizes:
            print(f"  🧮 Testing size {size}...")
            stdout, stderr, code = self.run_command(
                f"./serial_bitonic {size}", 
                cwd=serial_dir
            )
            
            if code == 0:
                exec_time = self.extract_execution_time(stdout)
                if exec_time is not None:
                    results[size] = exec_time
                    print(f"    ✅ {exec_time:.2f} ms")
                else:
                    print(f"    ⚠️ Could not parse execution time")
            else:
                print(f"    ❌ Execution failed: {stderr}")
        
        return results
    
    def collect_openmp_data(self):
        """Collect data from OpenMP implementation"""
        print("\n🔄 Collecting OpenMP implementation data...")
        openmp_dir = self.base_dir / "OpenMP"
        
        # Build if needed
        if not (openmp_dir / "openmp_bitonic").exists():
            print("  📦 Building OpenMP implementation...")
            stdout, stderr, code = self.run_command("make", cwd=openmp_dir)
            if code != 0:
                print(f"  ❌ Build failed: {stderr}")
                return {}
        
        thread_counts = [1, 2, 4, 8]
        results = {}
        
        for threads in thread_counts:
            print(f"  🧵 Testing with {threads} thread(s)...")
            thread_results = {}
            
            for size in self.array_sizes:
                print(f"    🧮 Size {size}...")
                env = os.environ.copy()
                env['OMP_NUM_THREADS'] = str(threads)
                
                stdout, stderr, code = self.run_command(
                    f"./openmp_bitonic {size}",
                    cwd=openmp_dir
                )
                
                if code == 0:
                    exec_time = self.extract_execution_time(stdout)
                    if exec_time is not None:
                        thread_results[size] = exec_time
                        print(f"      ✅ {exec_time:.2f} ms")
                    else:
                        print(f"      ⚠️ Could not parse execution time")
                else:
                    print(f"      ❌ Execution failed")
            
            results[threads] = thread_results
        
        return results
    
    def collect_mpi_data(self):
        """Collect data from MPI implementation"""
        print("\n🔄 Collecting MPI implementation data...")
        mpi_dir = self.base_dir / "MPI"
        
        # Build if needed
        if not (mpi_dir / "mpi_bitonic").exists():
            print("  📦 Building MPI implementation...")
            stdout, stderr, code = self.run_command("make", cwd=mpi_dir)
            if code != 0:
                print(f"  ❌ Build failed: {stderr}")
                return {}
        
        process_counts = [1, 2, 4, 8]
        results = {}
        
        for procs in process_counts:
            print(f"  🔀 Testing with {procs} process(es)...")
            proc_results = {}
            
            for size in self.array_sizes:
                print(f"    🧮 Size {size}...")
                stdout, stderr, code = self.run_command(
                    f"mpirun -np {procs} ./mpi_bitonic {size}",
                    cwd=mpi_dir
                )
                
                if code == 0:
                    exec_time = self.extract_execution_time(stdout)
                    if exec_time is not None:
                        proc_results[size] = exec_time
                        print(f"      ✅ {exec_time:.2f} ms")
                    else:
                        print(f"      ⚠️ Could not parse execution time")
                else:
                    print(f"      ❌ Execution failed")
            
            results[procs] = proc_results
        
        return results
    
    def collect_cuda_data(self):
        """Collect data from CUDA implementation"""
        print("\n🔄 Collecting CUDA implementation data...")
        cuda_dir = self.base_dir / "CUDA"
        
        # Check if NVCC is available
        stdout, stderr, code = self.run_command("nvcc --version")
        if code != 0:
            print("  ⚠️ NVCC not found. Skipping CUDA data collection.")
            return {}
        
        # Build if needed
        if not (cuda_dir / "cuda_bitonic").exists():
            print("  📦 Building CUDA implementation...")
            stdout, stderr, code = self.run_command("make", cwd=cuda_dir)
            if code != 0:
                print(f"  ❌ Build failed: {stderr}")
                return {}
        
        results = {}
        for size in self.array_sizes:
            print(f"  🎮 Testing size {size}...")
            stdout, stderr, code = self.run_command(
                f"./cuda_bitonic {size}",
                cwd=cuda_dir
            )
            
            if code == 0:
                # Look for GPU Kernel Time specifically for CUDA
                lines = stdout.split('\n')
                for line in lines:
                    if 'GPU Kernel Time:' in line:
                        try:
                            time_str = line.split(':')[1].strip().split('ms')[0].strip()
                            exec_time = float(time_str)
                            results[size] = exec_time
                            print(f"    ✅ {exec_time:.2f} ms")
                            break
                        except (ValueError, IndexError):
                            continue
                else:
                    print(f"    ⚠️ Could not parse GPU kernel time")
            else:
                print(f"    ❌ Execution failed")
        
        return results
    
    def save_results_to_csv(self, serial_data, openmp_data, mpi_data, cuda_data, filename="performance_results.csv"):
        """Save all collected data to CSV file"""
        print(f"\n💾 Saving results to {filename}...")
        
        # Prepare CSV data
        csv_data = []
        header = ['array_size', 'serial']
        
        # Add OpenMP columns
        for threads in sorted(openmp_data.keys()):
            header.append(f'openmp_{threads}')
        
        # Add MPI columns  
        for procs in sorted(mpi_data.keys()):
            header.append(f'mpi_{procs}')
        
        # Add CUDA column
        if cuda_data:
            header.append('cuda')
        
        # Compile data rows
        for size in self.array_sizes:
            row = [size]
            
            # Serial data
            row.append(serial_data.get(size, ''))
            
            # OpenMP data
            for threads in sorted(openmp_data.keys()):
                row.append(openmp_data[threads].get(size, ''))
            
            # MPI data
            for procs in sorted(mpi_data.keys()):
                row.append(mpi_data[procs].get(size, ''))
            
            # CUDA data
            if cuda_data:
                row.append(cuda_data.get(size, ''))
            
            csv_data.append(row)
        
        # Write CSV file
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(csv_data)
        
        print(f"✅ Results saved to {filename}")
        
        # Print summary
        print("\n📊 Data Collection Summary:")
        print("-" * 30)
        print(f"Serial data points:    {len([v for v in serial_data.values() if v])}")
        print(f"OpenMP configurations: {len(openmp_data)}")
        print(f"MPI configurations:    {len(mpi_data)}")
        print(f"CUDA data points:      {len([v for v in cuda_data.values() if v])}")
        
    def run_collection(self):
        """Run complete data collection process"""
        print("🚀 Bitonic Sort Performance Data Collection")
        print("=" * 50)
        print("This script will:")
        print("• Build all implementations if needed")
        print("• Run tests with different array sizes")
        print("• Collect execution time data")
        print("• Save results to CSV for visualization")
        print()
        
        # Collect data from all implementations
        serial_data = self.collect_serial_data()
        openmp_data = self.collect_openmp_data()
        mpi_data = self.collect_mpi_data()
        cuda_data = self.collect_cuda_data()
        
        # Save to CSV
        self.save_results_to_csv(serial_data, openmp_data, mpi_data, cuda_data)
        
        print("\n🎉 Data collection complete!")
        print("📈 You can now run 'python visualize_performance.py' to create plots.")


def main():
    """Main function"""
    collector = PerformanceCollector()
    
    # Check if we're in the right directory
    if not Path("Serial").exists() or not Path("OpenMP").exists():
        print("❌ Error: Please run this script from the Assignment3 directory")
        print("   The script expects Serial/, OpenMP/, MPI/, and CUDA/ subdirectories")
        sys.exit(1)
    
    try:
        collector.run_collection()
    except KeyboardInterrupt:
        print("\n\n⏹️ Collection interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during collection: {e}")


if __name__ == "__main__":
    main()