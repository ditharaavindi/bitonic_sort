#!/usr/bin/env python3
"""
Performance Visualization Tool for Bitonic Sort Implementations

This script creates comprehensive performance visualizations for comparing
Serial, OpenMP, MPI, and CUDA implementations of Bitonic Sort.

Author: Parallel Computing Assignment 3
Date: December 2025

Usage:
    python visualize_performance.py
    
Requirements:
    pip install matplotlib numpy pandas seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class BitonicSortVisualizer:
    def __init__(self):
        """Initialize the visualizer with sample data structure"""
        self.setup_plot_style()
        
    def setup_plot_style(self):
        """Configure matplotlib and seaborn styles"""
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        
    def create_sample_data(self):
        """Create sample performance data for demonstration"""
        # Array sizes (powers of 2)
        array_sizes = [256, 512, 1024, 2048, 4096, 8192, 16384]
        
        # Sample execution times (in milliseconds) - replace with your actual data
        sample_data = {
            'array_size': array_sizes,
            'serial': [0.5, 2.1, 8.5, 34.2, 137.8, 551.2, 2204.8],
            'openmp_1': [0.5, 2.1, 8.5, 34.2, 137.8, 551.2, 2204.8],  # Same as serial
            'openmp_2': [0.4, 1.2, 4.8, 19.1, 76.4, 305.6, 1222.4],
            'openmp_4': [0.3, 0.8, 2.9, 11.7, 46.8, 187.2, 748.8],
            'openmp_8': [0.3, 0.7, 2.5, 9.8, 39.2, 156.8, 627.2],
            'mpi_1': [0.6, 2.3, 9.1, 36.4, 145.6, 582.4, 2329.6],
            'mpi_2': [0.5, 1.4, 5.2, 20.8, 83.2, 332.8, 1331.2],
            'mpi_4': [0.4, 0.9, 3.1, 12.4, 49.6, 198.4, 793.6],
            'mpi_8': [0.4, 0.8, 2.7, 10.8, 43.2, 172.8, 691.2],
            'cuda': [0.1, 0.2, 0.5, 1.2, 2.8, 6.1, 13.5]
        }
        
        return pd.DataFrame(sample_data)
    
    def load_custom_data(self, filename):
        """Load performance data from CSV file
        
        Expected CSV format:
        array_size,serial,openmp_1,openmp_2,openmp_4,openmp_8,mpi_1,mpi_2,mpi_4,mpi_8,cuda
        256,0.5,0.5,0.4,0.3,0.3,0.6,0.5,0.4,0.4,0.1
        ...
        """
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f"File {filename} not found. Using sample data.")
            return self.create_sample_data()
        except Exception as e:
            print(f"Error loading data: {e}. Using sample data.")
            return self.create_sample_data()
    
    def calculate_speedup(self, df, baseline_col='serial'):
        """Calculate speedup relative to baseline implementation"""
        speedup_df = df.copy()
        baseline = df[baseline_col]
        
        for col in df.columns:
            if col != 'array_size' and col != baseline_col:
                speedup_df[f'{col}_speedup'] = baseline / df[col]
        
        return speedup_df
    
    def calculate_efficiency(self, df, baseline_col='serial'):
        """Calculate parallel efficiency"""
        efficiency_df = df.copy()
        baseline = df[baseline_col]
        
        # Define thread/process counts for each implementation
        thread_counts = {
            'openmp_1': 1, 'openmp_2': 2, 'openmp_4': 4, 'openmp_8': 8,
            'mpi_1': 1, 'mpi_2': 2, 'mpi_4': 4, 'mpi_8': 8
        }
        
        for col in df.columns:
            if col in thread_counts:
                speedup = baseline / df[col]
                threads = thread_counts[col]
                efficiency_df[f'{col}_efficiency'] = (speedup / threads) * 100
        
        return efficiency_df
    
    def plot_execution_time_comparison(self, df, save_path='execution_time_comparison.png'):
        """Plot execution time vs array size for all implementations"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Linear scale plot
        implementations = ['serial', 'openmp_4', 'openmp_8', 'mpi_4', 'mpi_8', 'cuda']
        colors = plt.cm.Set1(np.linspace(0, 1, len(implementations)))
        
        for i, impl in enumerate(implementations):
            if impl in df.columns:
                ax1.plot(df['array_size'], df[impl], 'o-', 
                        label=impl.replace('_', ' ').title(), 
                        color=colors[i], linewidth=2, markersize=6)
        
        ax1.set_xlabel('Array Size')
        ax1.set_ylabel('Execution Time (ms)')
        ax1.set_title('Execution Time Comparison (Linear Scale)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Log-log scale plot
        for i, impl in enumerate(implementations):
            if impl in df.columns:
                ax2.loglog(df['array_size'], df[impl], 'o-', 
                          label=impl.replace('_', ' ').title(), 
                          color=colors[i], linewidth=2, markersize=6)
        
        ax2.set_xlabel('Array Size')
        ax2.set_ylabel('Execution Time (ms)')
        ax2.set_title('Execution Time Comparison (Log-Log Scale)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_scalability_analysis(self, df, save_path='scalability_analysis.png'):
        """Plot scalability analysis for OpenMP and MPI"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # OpenMP scalability
        openmp_cols = [col for col in df.columns if col.startswith('openmp_')]
        thread_counts = [int(col.split('_')[1]) for col in openmp_cols]
        
        for size in [1024, 4096, 16384]:
            if size in df['array_size'].values:
                times = []
                for col in openmp_cols:
                    time_val = df[df['array_size'] == size][col].iloc[0]
                    times.append(time_val)
                
                ax1.plot(thread_counts, times, 'o-', label=f'Size {size}', linewidth=2, markersize=6)
        
        ax1.set_xlabel('Number of Threads')
        ax1.set_ylabel('Execution Time (ms)')
        ax1.set_title('OpenMP Thread Scalability')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
        
        # MPI scalability
        mpi_cols = [col for col in df.columns if col.startswith('mpi_')]
        process_counts = [int(col.split('_')[1]) for col in mpi_cols]
        
        for size in [1024, 4096, 16384]:
            if size in df['array_size'].values:
                times = []
                for col in mpi_cols:
                    time_val = df[df['array_size'] == size][col].iloc[0]
                    times.append(time_val)
                
                ax2.plot(process_counts, times, 's-', label=f'Size {size}', linewidth=2, markersize=6)
        
        ax2.set_xlabel('Number of Processes')
        ax2.set_ylabel('Execution Time (ms)')
        ax2.set_title('MPI Process Scalability')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_yscale('log')
        
        # Calculate and plot speedup
        speedup_df = self.calculate_speedup(df)
        
        # OpenMP speedup
        for size in [1024, 4096, 16384]:
            if size in df['array_size'].values:
                speedups = []
                for col in openmp_cols:
                    speedup_col = f'{col}_speedup'
                    if speedup_col in speedup_df.columns:
                        speedup_val = speedup_df[speedup_df['array_size'] == size][speedup_col].iloc[0]
                        speedups.append(speedup_val)
                
                ax3.plot(thread_counts, speedups, 'o-', label=f'Size {size}', linewidth=2, markersize=6)
        
        # Add ideal speedup line
        ax3.plot(thread_counts, thread_counts, 'k--', label='Ideal Speedup', alpha=0.7)
        ax3.set_xlabel('Number of Threads')
        ax3.set_ylabel('Speedup')
        ax3.set_title('OpenMP Speedup')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # MPI speedup
        for size in [1024, 4096, 16384]:
            if size in df['array_size'].values:
                speedups = []
                for col in mpi_cols:
                    speedup_col = f'{col}_speedup'
                    if speedup_col in speedup_df.columns:
                        speedup_val = speedup_df[speedup_df['array_size'] == size][speedup_col].iloc[0]
                        speedups.append(speedup_val)
                
                ax4.plot(process_counts, speedups, 's-', label=f'Size {size}', linewidth=2, markersize=6)
        
        # Add ideal speedup line
        ax4.plot(process_counts, process_counts, 'k--', label='Ideal Speedup', alpha=0.7)
        ax4.set_xlabel('Number of Processes')
        ax4.set_ylabel('Speedup')
        ax4.set_title('MPI Speedup')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_efficiency_analysis(self, df, save_path='efficiency_analysis.png'):
        """Plot parallel efficiency analysis"""
        efficiency_df = self.calculate_efficiency(df)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # OpenMP efficiency
        openmp_eff_cols = [col for col in efficiency_df.columns if col.startswith('openmp_') and col.endswith('_efficiency')]
        thread_counts = [int(col.split('_')[1]) for col in openmp_eff_cols]
        
        for size in [1024, 4096, 16384]:
            if size in df['array_size'].values:
                efficiencies = []
                for col in openmp_eff_cols:
                    eff_val = efficiency_df[efficiency_df['array_size'] == size][col].iloc[0]
                    efficiencies.append(eff_val)
                
                ax1.plot(thread_counts, efficiencies, 'o-', label=f'Size {size}', linewidth=2, markersize=6)
        
        ax1.axhline(y=100, color='k', linestyle='--', alpha=0.7, label='Ideal Efficiency')
        ax1.set_xlabel('Number of Threads')
        ax1.set_ylabel('Efficiency (%)')
        ax1.set_title('OpenMP Parallel Efficiency')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 110)
        
        # MPI efficiency
        mpi_eff_cols = [col for col in efficiency_df.columns if col.startswith('mpi_') and col.endswith('_efficiency')]
        process_counts = [int(col.split('_')[1]) for col in mpi_eff_cols]
        
        for size in [1024, 4096, 16384]:
            if size in df['array_size'].values:
                efficiencies = []
                for col in mpi_eff_cols:
                    eff_val = efficiency_df[efficiency_df['array_size'] == size][col].iloc[0]
                    efficiencies.append(eff_val)
                
                ax2.plot(process_counts, efficiencies, 's-', label=f'Size {size}', linewidth=2, markersize=6)
        
        ax2.axhline(y=100, color='k', linestyle='--', alpha=0.7, label='Ideal Efficiency')
        ax2.set_xlabel('Number of Processes')
        ax2.set_ylabel('Efficiency (%)')
        ax2.set_title('MPI Parallel Efficiency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 110)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_implementation_comparison(self, df, save_path='implementation_comparison.png'):
        """Plot detailed comparison of all implementations"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Select representative array size
        target_size = 4096
        if target_size not in df['array_size'].values:
            target_size = df['array_size'].iloc[-2]  # Second largest size
        
        # Implementation comparison bar chart
        implementations = ['serial', 'openmp_4', 'openmp_8', 'mpi_4', 'mpi_8', 'cuda']
        times = []
        labels = []
        
        for impl in implementations:
            if impl in df.columns:
                time_val = df[df['array_size'] == target_size][impl].iloc[0]
                times.append(time_val)
                labels.append(impl.replace('_', ' ').title())
        
        colors = plt.cm.Set1(np.linspace(0, 1, len(times)))
        bars = ax1.bar(labels, times, color=colors, alpha=0.7, edgecolor='black')
        ax1.set_ylabel('Execution Time (ms)')
        ax1.set_title(f'Implementation Comparison (Array Size: {target_size})')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, time in zip(bars, times):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{time:.2f}', ha='center', va='bottom')
        
        # Speedup comparison
        baseline_time = df[df['array_size'] == target_size]['serial'].iloc[0]
        speedups = [baseline_time / time for time in times]
        
        bars2 = ax2.bar(labels, speedups, color=colors, alpha=0.7, edgecolor='black')
        ax2.set_ylabel('Speedup')
        ax2.set_title(f'Speedup Comparison (Array Size: {target_size})')
        ax2.tick_params(axis='x', rotation=45)
        ax2.axhline(y=1, color='r', linestyle='--', alpha=0.7, label='Baseline')
        
        # Add value labels on bars
        for bar, speedup in zip(bars2, speedups):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{speedup:.2f}x', ha='center', va='bottom')
        
        # CUDA vs Others comparison across sizes
        cuda_speedups = []
        sizes_for_cuda = []
        
        if 'cuda' in df.columns:
            for _, row in df.iterrows():
                if row['cuda'] > 0:  # Valid CUDA data
                    speedup = row['serial'] / row['cuda']
                    cuda_speedups.append(speedup)
                    sizes_for_cuda.append(row['array_size'])
            
            ax3.semilogx(sizes_for_cuda, cuda_speedups, 'ro-', linewidth=3, markersize=8, label='CUDA Speedup')
            ax3.set_xlabel('Array Size')
            ax3.set_ylabel('Speedup vs Serial')
            ax3.set_title('CUDA Speedup Across Array Sizes')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
        
        # Strong scaling analysis
        thread_counts = [1, 2, 4, 8]
        openmp_times = []
        mpi_times = []
        
        target_size_scaling = 8192 if 8192 in df['array_size'].values else df['array_size'].iloc[-1]
        
        for count in thread_counts:
            openmp_col = f'openmp_{count}'
            mpi_col = f'mpi_{count}'
            
            if openmp_col in df.columns:
                time_val = df[df['array_size'] == target_size_scaling][openmp_col].iloc[0]
                openmp_times.append(time_val)
            
            if mpi_col in df.columns:
                time_val = df[df['array_size'] == target_size_scaling][mpi_col].iloc[0]
                mpi_times.append(time_val)
        
        ax4.loglog(thread_counts, openmp_times, 'o-', label='OpenMP', linewidth=2, markersize=6)
        ax4.loglog(thread_counts, mpi_times, 's-', label='MPI', linewidth=2, markersize=6)
        
        # Add ideal scaling line
        ideal_times = [openmp_times[0] / count for count in thread_counts]
        ax4.loglog(thread_counts, ideal_times, 'k--', label='Ideal Scaling', alpha=0.7)
        
        ax4.set_xlabel('Thread/Process Count')
        ax4.set_ylabel('Execution Time (ms)')
        ax4.set_title(f'Strong Scaling Analysis (Size: {target_size_scaling})')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_performance_report(self, df, output_dir='performance_plots'):
        """Generate a comprehensive performance report"""
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print("🔄 Generating Performance Analysis Report...")
        print("=" * 50)
        
        # Generate all plots
        self.plot_execution_time_comparison(df, f'{output_dir}/execution_time_comparison.png')
        print("✅ Execution time comparison plot saved")
        
        self.plot_scalability_analysis(df, f'{output_dir}/scalability_analysis.png')
        print("✅ Scalability analysis plot saved")
        
        self.plot_efficiency_analysis(df, f'{output_dir}/efficiency_analysis.png')
        print("✅ Efficiency analysis plot saved")
        
        self.plot_implementation_comparison(df, f'{output_dir}/implementation_comparison.png')
        print("✅ Implementation comparison plot saved")
        
        # Generate summary statistics
        self.generate_summary_table(df, f'{output_dir}/performance_summary.txt')
        print("✅ Performance summary table saved")
        
        print("=" * 50)
        print(f"🎉 Complete performance report generated in '{output_dir}' directory!")
        print("📊 All plots saved as high-resolution PNG files")
    
    def generate_summary_table(self, df, output_file):
        """Generate a text summary of performance metrics"""
        with open(output_file, 'w') as f:
            f.write("BITONIC SORT PERFORMANCE ANALYSIS SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            
            # Best performance for each array size
            f.write("BEST PERFORMANCE BY ARRAY SIZE:\n")
            f.write("-" * 30 + "\n")
            
            for _, row in df.iterrows():
                size = int(row['array_size'])
                times = {col: row[col] for col in df.columns if col != 'array_size' and not pd.isna(row[col])}
                best_impl = min(times, key=times.get)
                best_time = times[best_impl]
                
                f.write(f"Size {size:6d}: {best_impl:12s} = {best_time:8.2f} ms\n")
            
            # Speedup analysis
            f.write(f"\nSPEEDUP ANALYSIS (vs Serial):\n")
            f.write("-" * 30 + "\n")
            
            speedup_df = self.calculate_speedup(df)
            target_size = 4096 if 4096 in df['array_size'].values else df['array_size'].iloc[-2]
            
            row = speedup_df[speedup_df['array_size'] == target_size].iloc[0]
            
            for col in speedup_df.columns:
                if col.endswith('_speedup'):
                    impl = col.replace('_speedup', '')
                    speedup = row[col]
                    if not pd.isna(speedup):
                        f.write(f"{impl:12s}: {speedup:6.2f}x speedup\n")
            
            # CUDA analysis
            if 'cuda' in df.columns:
                f.write(f"\nCUDA PERFORMANCE HIGHLIGHTS:\n")
                f.write("-" * 30 + "\n")
                
                for _, row in df.iterrows():
                    if not pd.isna(row['cuda']) and row['cuda'] > 0:
                        size = int(row['array_size'])
                        cuda_speedup = row['serial'] / row['cuda']
                        f.write(f"Size {size:6d}: {cuda_speedup:6.2f}x faster than serial\n")


def main():
    """Main function to demonstrate the visualization tool"""
    visualizer = BitonicSortVisualizer()
    
    print("🚀 Bitonic Sort Performance Visualizer")
    print("=" * 40)
    print("\n📌 Instructions:")
    print("1. Run your bitonic sort implementations and collect timing data")
    print("2. Create a CSV file with the format shown in the sample data")
    print("3. Either replace the sample data in this script or load your CSV")
    print("4. Run this script to generate comprehensive performance plots")
    
    # Option to load custom data
    custom_file = input("\n📂 Enter CSV filename (or press Enter for sample data): ").strip()
    
    if custom_file:
        df = visualizer.load_custom_data(custom_file)
    else:
        df = visualizer.create_sample_data()
        print("\n📊 Using sample data for demonstration...")
    
    print(f"\n✅ Loaded data for {len(df)} array sizes")
    print("🎯 Generating comprehensive performance analysis...")
    
    # Generate complete performance report
    visualizer.create_performance_report(df)


if __name__ == "__main__":
    main()