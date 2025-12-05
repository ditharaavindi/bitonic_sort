# Master Makefile for All Bitonic Sort Implementations
# Author: Parallel Computing Assignment 3
# Date: December 2025

# Default target
all:
	@echo "Building all bitonic sort implementations..."
	$(MAKE) -C Serial all
	$(MAKE) -C OpenMP all
	$(MAKE) -C MPI all
	$(MAKE) -C CUDA all
	@echo "All implementations built successfully!"

# Clean all implementations
clean:
	@echo "Cleaning all implementations..."
	$(MAKE) -C Serial clean
	$(MAKE) -C OpenMP clean
	$(MAKE) -C MPI clean
	$(MAKE) -C CUDA clean
	@echo "All implementations cleaned!"

# Test all implementations
test:
	@echo "=== Testing All Implementations ==="
	@echo "\n1. Testing Serial Implementation:"
	$(MAKE) -C Serial test
	@echo "\n2. Testing OpenMP Implementation:"
	$(MAKE) -C OpenMP test
	@echo "\n3. Testing MPI Implementation:"
	$(MAKE) -C MPI test
	@echo "\n4. Testing CUDA Implementation:"
	$(MAKE) -C CUDA test

# Run basic tests for all implementations
run-all:
	@echo "=== Running All Implementations (Size 1024) ==="
	@echo "\n1. Serial:"
	$(MAKE) -C Serial run
	@echo "\n2. OpenMP:"
	$(MAKE) -C OpenMP run
	@echo "\n3. MPI:"
	$(MAKE) -C MPI run
	@echo "\n4. CUDA:"
	$(MAKE) -C CUDA run

# Performance comparison
benchmark:
	@echo "=== Performance Benchmark (Size 4096) ==="
	@echo "\n1. Serial:"
	$(MAKE) -C Serial run TARGET_SIZE=4096 || Serial/serial_bitonic 4096
	@echo "\n2. OpenMP:"
	$(MAKE) -C OpenMP benchmark
	@echo "\n3. MPI:"
	$(MAKE) -C MPI benchmark
	@echo "\n4. CUDA:"
	$(MAKE) -C CUDA benchmark

# Install all implementations
install:
	@echo "Installing all implementations..."
	$(MAKE) -C Serial install
	$(MAKE) -C OpenMP install
	$(MAKE) -C MPI install
	$(MAKE) -C CUDA install
	@echo "All implementations installed!"

# Uninstall all implementations
uninstall:
	@echo "Uninstalling all implementations..."
	$(MAKE) -C Serial uninstall
	$(MAKE) -C OpenMP uninstall
	$(MAKE) -C MPI uninstall
	$(MAKE) -C CUDA uninstall
	@echo "All implementations uninstalled!"

# Show help
help:
	@echo "=== Bitonic Sort Implementation Master Makefile ==="
	@echo "Available targets:"
	@echo "  all       - Build all implementations"
	@echo "  clean     - Clean all implementations"
	@echo "  test      - Test all implementations comprehensively"
	@echo "  run-all   - Run basic test for all implementations"
	@echo "  benchmark - Performance comparison of all implementations"
	@echo "  install   - Install all implementations to system"
	@echo "  uninstall - Remove all implementations from system"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Individual targets (use 'make -C <dir> <target>'):"
	@echo "  Serial/   - Serial implementation"
	@echo "  OpenMP/   - OpenMP parallel implementation"
	@echo "  MPI/      - MPI distributed implementation"
	@echo "  CUDA/     - CUDA GPU implementation"

.PHONY: all clean test run-all benchmark install uninstall help