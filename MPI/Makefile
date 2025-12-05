# Makefile for MPI Parallel Bitonic Sort
# Author: Parallel Computing Assignment 3
# Date: December 2025

CC = mpicc
CFLAGS = -Wall -Wextra -O3 -std=c99
TARGET = mpi_bitonic
SOURCE = mpi_bitonic.c

# Default target
all: $(TARGET)

# Build the MPI version
$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(SOURCE) -o $(TARGET)

# Clean build artifacts
clean:
	rm -f $(TARGET)

# Run with default settings (4 processes, size 1024)
run: $(TARGET)
	mpirun -np 4 ./$(TARGET) 1024

# Run with different process counts
test-procs: $(TARGET)
	@echo "Testing with different process counts (array size 2048):"
	@echo "1 process:"
	mpirun -np 1 ./$(TARGET) 2048
	@echo "\n2 processes:"
	mpirun -np 2 ./$(TARGET) 2048
	@echo "\n4 processes:"
	mpirun -np 4 ./$(TARGET) 2048
	@echo "\n8 processes:"
	mpirun -np 8 ./$(TARGET) 2048

# Run with different array sizes
test-sizes: $(TARGET)
	@echo "Testing with different array sizes (4 processes):"
	@echo "Size 256:"
	mpirun -np 4 ./$(TARGET) 256
	@echo "\nSize 512:"
	mpirun -np 4 ./$(TARGET) 512
	@echo "\nSize 1024:"
	mpirun -np 4 ./$(TARGET) 1024
	@echo "\nSize 2048:"
	mpirun -np 4 ./$(TARGET) 2048
	@echo "\nSize 4096:"
	mpirun -np 4 ./$(TARGET) 4096

# Comprehensive test
test: $(TARGET)
	@echo "=== MPI Bitonic Sort Testing ==="
	@$(MAKE) test-procs
	@echo "\n"
	@$(MAKE) test-sizes

# Performance benchmark
benchmark: $(TARGET)
	@echo "=== Performance Benchmark ==="
	@echo "Serial (1 process):"
	mpirun -np 1 ./$(TARGET) 4096
	@echo "\nParallel (4 processes):"
	mpirun -np 4 ./$(TARGET) 4096
	@echo "\nParallel (8 processes):"
	mpirun -np 8 ./$(TARGET) 4096

# Install (copy to system directory - requires sudo)
install: $(TARGET)
	sudo cp $(TARGET) /usr/local/bin/

# Uninstall
uninstall:
	sudo rm -f /usr/local/bin/$(TARGET)

# Show help
help:
	@echo "Available targets:"
	@echo "  all        - Build the MPI bitonic sort program"
	@echo "  clean      - Remove build artifacts"
	@echo "  run        - Run with default settings (4 processes, size 1024)"
	@echo "  test-procs - Test with different process counts"
	@echo "  test-sizes - Test with different array sizes"
	@echo "  test       - Run comprehensive tests"
	@echo "  benchmark  - Run performance comparison"
	@echo "  install    - Install to system directory"
	@echo "  uninstall  - Remove from system directory"
	@echo "  help       - Show this help message"

.PHONY: all clean run test-procs test-sizes test benchmark install uninstall help