#!/usr/bin/env python3
"""
Automated Screenshot Helper Script
Runs performance tests and provides prompts for manual screenshot capture

Usage: python3 capture_screenshots.py
"""

import subprocess
import time
import os

class ScreenshotHelper:
    def __init__(self):
        self.screenshot_dir = "screenshots"
        self.delay = 3  # seconds to wait between commands
        
    def setup(self):
        """Create screenshot directory and build implementations"""
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
            print(f"Created directory: {self.screenshot_dir}")
        
        print("Building implementations...")
        try:
            subprocess.run(['make', 'clean'], cwd='OpenMP', check=True, capture_output=True)
            subprocess.run(['make'], cwd='OpenMP', check=True, capture_output=True)
            subprocess.run(['make', 'clean'], cwd='MPI', check=True, capture_output=True)
            subprocess.run(['make'], cwd='MPI', check=True, capture_output=True)
            print("✓ All implementations built successfully")
            return True
        except Exception as e:
            print(f"✗ Build failed: {e}")
            return False
    
    def wait_for_screenshot(self, description, filename):
        """Wait for user to take screenshot"""
        print(f"\n{'='*60}")
        print(f"SCREENSHOT REQUIRED: {description}")
        print(f"Suggested filename: {filename}")
        print(f"{'='*60}")
        input("Press ENTER after taking the screenshot to continue...")
    
    def run_openmp_tests(self):
        """Run OpenMP tests with screenshot prompts"""
        print("\n🔥 STARTING OPENMP SCREENSHOT SEQUENCE 🔥\n")
        
        os.chdir('OpenMP')
        
        thread_counts = [1, 2, 4, 8, 16]
        array_size = 4096
        
        for threads in thread_counts:
            print(f"\n📊 Running OpenMP test with {threads} thread(s)")
            print(f"Command: OMP_NUM_THREADS={threads} ./openmp_bitonic {array_size}")
            print("Ready to execute. Take screenshot after running this command:")
            print(f"OMP_NUM_THREADS={threads} ./openmp_bitonic {array_size}")
            
            self.wait_for_screenshot(
                f"OpenMP execution with {threads} thread(s)",
                f"openmp_{threads}_thread{'s' if threads > 1 else ''}.png"
            )
        
        # Thread scaling test
        print(f"\n📊 Running OpenMP thread scaling test")
        print("Command: make test-threads")
        print("Ready to execute. Take screenshot after running this command:")
        print("make test-threads")
        
        self.wait_for_screenshot(
            "OpenMP thread scaling test results",
            "openmp_scaling_test.png"
        )
        
        os.chdir('..')
    
    def run_mpi_tests(self):
        """Run MPI tests with screenshot prompts"""
        print("\n🚀 STARTING MPI SCREENSHOT SEQUENCE 🚀\n")
        
        os.chdir('MPI')
        
        process_counts = [1, 2, 4, 8, 16]
        array_size = 4096
        
        for processes in process_counts:
            print(f"\n📡 Running MPI test with {processes} process(es)")
            print(f"Command: mpirun -np {processes} ./mpi_bitonic {array_size}")
            print("Ready to execute. Take screenshot after running this command:")
            print(f"mpirun -np {processes} ./mpi_bitonic {array_size}")
            
            self.wait_for_screenshot(
                f"MPI execution with {processes} process(es)",
                f"mpi_{processes}_process{'es' if processes > 1 else ''}.png"
            )
        
        # Process scaling test
        print(f"\n📡 Running MPI process scaling test")
        print("Command: make test-procs")
        print("Ready to execute. Take screenshot after running this command:")
        print("make test-procs")
        
        self.wait_for_screenshot(
            "MPI process scaling test results",
            "mpi_scaling_test.png"
        )
        
        os.chdir('..')
    
    def run_performance_graphs(self):
        """Generate and capture performance graphs"""
        print("\n📈 GENERATING PERFORMANCE GRAPHS 📈\n")
        
        print("Running automated performance evaluation...")
        print("This will take several minutes to complete.")
        print("Command: python3 performance_evaluation.py --all")
        print("Ready to execute. Take screenshot of the generated graphs:")
        
        self.wait_for_screenshot(
            "Performance evaluation graphs (both OpenMP and MPI)",
            "performance_graphs_combined.png"
        )
    
    def run_system_info(self):
        """Display system information for screenshot"""
        print("\n💻 SYSTEM INFORMATION SCREENSHOT 💻\n")
        
        print("Commands to run for system info:")
        print("echo 'CPU Information:'")
        print("sysctl -n machdep.cpu.brand_string")
        print("sysctl -n hw.ncpu")
        print("sysctl -n hw.logicalcpu")
        print("echo 'Memory Information:'")
        print("sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 \" GB\"}'")
        print("mpirun --version")
        
        self.wait_for_screenshot(
            "System specifications and MPI configuration",
            "system_info.png"
        )
    
    def provide_final_instructions(self):
        """Provide final instructions"""
        print(f"\n🎉 SCREENSHOT SEQUENCE COMPLETE! 🎉\n")
        print("Screenshot Organization Tips:")
        print(f"1. All screenshots should be saved in the '{self.screenshot_dir}' directory")
        print("2. Use the suggested filenames for consistency")
        print("3. Ensure screenshots are high resolution (PNG format recommended)")
        print("4. Include terminal window with complete command and output")
        print("\nNext Steps:")
        print("1. Run the performance evaluation script: python3 performance_evaluation.py --all")
        print("2. Check generated CSV files and graphs")
        print("3. Review screenshot_guide.md for additional guidance")
        print("4. Organize screenshots for your report")
        
        print(f"\nSuggested Screenshot Organization:")
        print(f"{self.screenshot_dir}/")
        print("├── openmp/")
        print("│   ├── openmp_1_thread.png")
        print("│   ├── openmp_2_threads.png") 
        print("│   ├── openmp_4_threads.png")
        print("│   ├── openmp_8_threads.png")
        print("│   ├── openmp_16_threads.png")
        print("│   └── openmp_scaling_test.png")
        print("├── mpi/")
        print("│   ├── mpi_1_process.png")
        print("│   ├── mpi_2_processes.png")
        print("│   ├── mpi_4_processes.png") 
        print("│   ├── mpi_8_processes.png")
        print("│   ├── mpi_16_processes.png")
        print("│   └── mpi_scaling_test.png")
        print("└── analysis/")
        print("    ├── performance_graphs_combined.png")
        print("    └── system_info.png")

def main():
    helper = ScreenshotHelper()
    
    print("🎬 Automated Screenshot Helper for Performance Evaluation 🎬")
    print("=" * 60)
    
    if not helper.setup():
        return
    
    print("\nThis script will guide you through taking screenshots for:")
    print("✓ OpenMP performance tests (1, 2, 4, 8, 16 threads)")
    print("✓ MPI performance tests (1, 2, 4, 8, 16 processes)")
    print("✓ Automated scaling tests")
    print("✓ Performance graphs")
    print("✓ System information")
    
    print("\nIMPORTANT:")
    print("- Have your screenshot tool ready (Cmd+Shift+4 on macOS)")
    print("- Make terminal window large enough to show complete output")
    print("- Use high contrast terminal theme")
    print("- Run commands in a separate terminal window")
    
    choice = input("\nStart screenshot sequence? (y/n): ").lower()
    
    if choice != 'y':
        print("Screenshot sequence cancelled.")
        return
    
    try:
        # Run test sequences
        helper.run_openmp_tests()
        helper.run_mpi_tests()
        helper.run_performance_graphs()
        helper.run_system_info()
        
        # Final instructions
        helper.provide_final_instructions()
        
    except KeyboardInterrupt:
        print("\n\nScreenshot sequence interrupted by user.")
    except Exception as e:
        print(f"\nError during screenshot sequence: {e}")

if __name__ == "__main__":
    main()