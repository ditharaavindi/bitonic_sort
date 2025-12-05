# Makefile for Serial Bitonic Sort
# Author: Parallel Computing Assignment 3
# Date: December 2025

CC = gcc
CFLAGS = -Wall -Wextra -O3 -std=c99
TARGET = serial_bitonic
SOURCE = serial_bitonic.c

# Default target
all: $(TARGET)

# Build the serial version
$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(SOURCE) -o $(TARGET)

# Clean build artifacts
clean:
	rm -f $(TARGET)

# Run with default size
run: $(TARGET)
	./$(TARGET) 1024

# Run with different sizes for testing
test: $(TARGET)
	@echo "Testing with different array sizes:"
	@echo "Size 256:"
	./$(TARGET) 256
	@echo "\nSize 512:"
	./$(TARGET) 512
	@echo "\nSize 1024:"
	./$(TARGET) 1024
	@echo "\nSize 2048:"
	./$(TARGET) 2048

# Install (copy to system directory - requires sudo)
install: $(TARGET)
	sudo cp $(TARGET) /usr/local/bin/

# Uninstall
uninstall:
	sudo rm -f /usr/local/bin/$(TARGET)

# Show help
help:
	@echo "Available targets:"
	@echo "  all      - Build the serial bitonic sort program"
	@echo "  clean    - Remove build artifacts"
	@echo "  run      - Run with default array size (1024)"
	@echo "  test     - Run with multiple array sizes"
	@echo "  install  - Install to system directory"
	@echo "  uninstall- Remove from system directory"
	@echo "  help     - Show this help message"

.PHONY: all clean run test install uninstall help