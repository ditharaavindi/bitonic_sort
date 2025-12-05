# Makefile for OpenMP Parallel Bitonic Sort
# Author: Parallel Computing Assignment 3
# Date: December 2025

CC = gcc-15
CFLAGS = -Wall -Wextra -O3 -std=c99 -fopenmp
TARGET = openmp_bitonic
SOURCE = openmp_bitonic.c

# Default target
all: $(TARGET)

# Build the OpenMP version
$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(SOURCE) -o $(TARGET)

# Clean build artifacts
clean:
	rm -f $(TARGET)

# Run with default size and 4 threads
run: $(TARGET)
	OMP_NUM_THREADS=4 ./$(TARGET) 1024

# Run with different thread counts
test-threads: $(TARGET)
	@echo "Testing with different thread counts (array size 2048):"
	@echo "1 thread:"
	OMP_NUM_THREADS=1 ./$(TARGET) 2048
	@echo "\n2 threads:"
	OMP_NUM_THREADS=2 ./$(TARGET) 2048
	@echo "\n4 threads:"
	OMP_NUM_THREADS=4 ./$(TARGET) 2048
	@echo "\n8 threads:"
	OMP_NUM_THREADS=8 ./$(TARGET) 2048

# Run with different array sizes
test-sizes: $(TARGET)
	@echo "Testing with different array sizes (4 threads):"
	@echo "Size 256:"
	OMP_NUM_THREADS=4 ./$(TARGET) 256
	@echo "\nSize 512:"
	OMP_NUM_THREADS=4 ./$(TARGET) 512
	@echo "\nSize 1024:"
	OMP_NUM_THREADS=4 ./$(TARGET) 1024
	@echo "\nSize 2048:"
	OMP_NUM_THREADS=4 ./$(TARGET) 2048
	@echo "\nSize 4096:"
	OMP_NUM_THREADS=4 ./$(TARGET) 4096

# Comprehensive test
test: $(TARGET)
	@echo "=== OpenMP Bitonic Sort Testing ==="
	@$(MAKE) test-threads
	@echo "\n"
	@$(MAKE) test-sizes

# Performance benchmark
benchmark: $(TARGET)
	@echo "=== Performance Benchmark ==="
	@echo "Serial (1 thread):"
	OMP_NUM_THREADS=1 ./$(TARGET) 4096
	@echo "\nParallel (max threads):"
	./$(TARGET) 4096

# Install (copy to system directory - requires sudo)
install: $(TARGET)
	sudo cp $(TARGET) /usr/local/bin/

# Uninstall
uninstall:
	sudo rm -f /usr/local/bin/$(TARGET)

# Show help
help:
	@echo "Available targets:"
	@echo "  all         - Build the OpenMP bitonic sort program"
	@echo "  clean       - Remove build artifacts"
	@echo "  run         - Run with default settings (4 threads, size 1024)"
	@echo "  test-threads- Test with different thread counts"
	@echo "  test-sizes  - Test with different array sizes"
	@echo "  test        - Run comprehensive tests"
	@echo "  benchmark   - Run performance comparison"
	@echo "  install     - Install to system directory"
	@echo "  uninstall   - Remove from system directory"
	@echo "  help        - Show this help message"

.PHONY: all clean run test-threads test-sizes test benchmark install uninstall help