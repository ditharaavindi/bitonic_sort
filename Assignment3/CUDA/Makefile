# Makefile for CUDA GPU Bitonic Sort
# Author: Parallel Computing Assignment 3
# Date: December 2025

NVCC = nvcc
NVCCFLAGS = -O3 -arch=sm_35 -Xcompiler -Wall
TARGET = cuda_bitonic
SOURCE = cuda_bitonic.cu

# Default target
all: $(TARGET)

# Build the CUDA version
$(TARGET): $(SOURCE)
	$(NVCC) $(NVCCFLAGS) $(SOURCE) -o $(TARGET)

# Clean build artifacts
clean:
	rm -f $(TARGET)

# Run with default size
run: $(TARGET)
	./$(TARGET) 1024

# Run with different array sizes
test: $(TARGET)
	@echo "Testing CUDA implementation with different array sizes:"
	@echo "Size 256:"
	./$(TARGET) 256
	@echo "\nSize 512:"
	./$(TARGET) 512
	@echo "\nSize 1024:"
	./$(TARGET) 1024
	@echo "\nSize 2048:"
	./$(TARGET) 2048
	@echo "\nSize 4096:"
	./$(TARGET) 4096

# Performance benchmark
benchmark: $(TARGET)
	@echo "=== CUDA Performance Benchmark ==="
	@echo "Running large array sizes for performance comparison:"
	@echo "Size 8192:"
	./$(TARGET) 8192
	@echo "\nSize 16384:"
	./$(TARGET) 16384

# GPU information
gpu-info:
	@echo "=== GPU Information ==="
	nvidia-smi
	@echo "\nCUDA Compiler Information:"
	nvcc --version

# Install (copy to system directory - requires sudo)
install: $(TARGET)
	sudo cp $(TARGET) /usr/local/bin/

# Uninstall
uninstall:
	sudo rm -f /usr/local/bin/$(TARGET)

# Show help
help:
	@echo "Available targets:"
	@echo "  all       - Build the CUDA bitonic sort program"
	@echo "  clean     - Remove build artifacts"
	@echo "  run       - Run with default array size (1024)"
	@echo "  test      - Test with different array sizes"
	@echo "  benchmark - Run performance benchmark with large arrays"
	@echo "  gpu-info  - Display GPU and CUDA information"
	@echo "  install   - Install to system directory"
	@echo "  uninstall - Remove from system directory"
	@echo "  help      - Show this help message"

.PHONY: all clean run test benchmark gpu-info install uninstall help