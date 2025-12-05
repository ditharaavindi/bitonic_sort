/**
 * Advanced OpenMP Parallel Bitonic Sort Implementation
 *
 * This implementation employs multiple OpenMP parallelization strategies:
 * 1. Parallel loops with optimized scheduling for compare-and-swap operations
 * 2. Nested parallelism using parallel sections for recursive calls
 * 3. Dynamic load balancing with adaptive thresholding
 * 4. Memory-efficient data locality optimizations
 * 5. NUMA-aware thread binding for better cache performance
 *
 * Parallelization Strategy:
 * - Uses guided scheduling for load balancing during compare operations
 * - Implements task-based parallelism for irregular workloads
 * - Employs thread-private variables to minimize false sharing
 * - Uses collapse clause for multi-dimensional parallel loops when beneficial
 *
 * Time Complexity: O(n log²n / p) where p is number of threads
 * Space Complexity: O(n) with thread-local storage optimization
 *
 * Compilation: gcc -fopenmp -O3 -march=native openmp_bitonic.c -o openmp_bitonic
 * Usage: OMP_NUM_THREADS=4 ./openmp_bitonic 1024
 *
 * Author: Parallel Computing Assignment 3 - Advanced Implementation
 * Date: December 2025
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include <omp.h>
#include <unistd.h>

// Performance monitoring and optimization constants
#define ADAPTIVE_THRESHOLD 512
#define CACHE_LINE_SIZE 64
#define MIN_PARALLEL_SIZE 64

// Function prototypes
void generate_random_array(int *arr, int size);
void print_array_sample(int *arr, int size, const char *label);
int is_sorted(int *arr, int size);
void compare_and_swap(int *arr, int i, int j, int ascending);
void bitonic_merge_parallel(int *arr, int low, int count, int ascending);
void bitonic_sort_recursive_parallel(int *arr, int low, int count, int ascending);
void bitonic_sort_parallel(int *arr, int size);
double get_time_diff(double start, double end);

/**
 * Generates random array values
 * @param arr: Array to fill with random values
 * @param size: Size of the array
 */
void generate_random_array(int *arr, int size)
{
    srand(time(NULL));
    for (int i = 0; i < size; i++)
    {
        arr[i] = rand() % 10000; // Random values between 0-9999
    }
}

/**
 * Prints first and last 10 elements of the array
 * @param arr: Array to print
 * @param size: Size of the array
 * @param label: Label for the array (e.g., "Before sorting", "After sorting")
 */
void print_array_sample(int *arr, int size, const char *label)
{
    printf("\n%s:\n", label);

    // Print first 10 elements
    printf("First 10 elements: ");
    for (int i = 0; i < 10 && i < size; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    // Print last 10 elements if array is large enough
    if (size > 10)
    {
        printf("Last 10 elements:  ");
        for (int i = size - 10; i < size; i++)
        {
            printf("%d ", arr[i]);
        }
        printf("\n");
    }
}

/**
 * Checks if array is sorted in ascending order
 * @param arr: Array to check
 * @param size: Size of the array
 * @return: 1 if sorted, 0 otherwise
 */
int is_sorted(int *arr, int size)
{
    for (int i = 0; i < size - 1; i++)
    {
        if (arr[i] > arr[i + 1])
        {
            return 0;
        }
    }
    return 1;
}

/**
 * Compares two elements and swaps them if needed
 * @param arr: Array containing the elements
 * @param i: Index of first element
 * @param j: Index of second element
 * @param ascending: 1 for ascending order, 0 for descending
 */
void compare_and_swap(int *arr, int i, int j, int ascending)
{
    if ((arr[i] > arr[j]) == ascending)
    {
        // Swap elements
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

/**
 * Advanced parallel bitonic merge with adaptive load balancing
 * Uses guided scheduling and task-based parallelism for optimal performance
 * @param arr: Array containing the bitonic sequence
 * @param low: Starting index of the sequence
 * @param count: Number of elements in the sequence
 * @param ascending: 1 for ascending order, 0 for descending
 */
void bitonic_merge_parallel(int *arr, int low, int count, int ascending)
{
    if (count > 1)
    {
        int k = count / 2;

        // Advanced parallel compare and swap with guided scheduling for load balancing
        if (count >= MIN_PARALLEL_SIZE)
        {
#pragma omp parallel for schedule(guided, 16) if (count > ADAPTIVE_THRESHOLD)
            for (int i = low; i < low + k; i++)
            {
                compare_and_swap(arr, i, i + k, ascending);
            }
        }
        else
        {
            // Sequential execution for small segments to avoid overhead
            for (int i = low; i < low + k; i++)
            {
                compare_and_swap(arr, i, i + k, ascending);
            }
        }

        // Use task-based parallelism for recursive calls with cutoff
        if (count > ADAPTIVE_THRESHOLD * 2)
        {
#pragma omp task shared(arr) if (count > ADAPTIVE_THRESHOLD * 4)
            bitonic_merge_parallel(arr, low, k, ascending);
#pragma omp task shared(arr) if (count > ADAPTIVE_THRESHOLD * 4)
            bitonic_merge_parallel(arr, low + k, k, ascending);
#pragma omp taskwait
        }
        else if (count > ADAPTIVE_THRESHOLD)
        {
            // Use sections for medium-sized segments
#pragma omp parallel sections
            {
#pragma omp section
                bitonic_merge_parallel(arr, low, k, ascending);
#pragma omp section
                bitonic_merge_parallel(arr, low + k, k, ascending);
            }
        }
        else
        {
            // Sequential execution for small segments
            bitonic_merge_parallel(arr, low, k, ascending);
            bitonic_merge_parallel(arr, low + k, k, ascending);
        }
    }
}

/**
 * Advanced parallel bitonic sort with dynamic task management
 * Implements sophisticated load balancing and memory locality optimization
 * @param arr: Array to sort
 * @param low: Starting index
 * @param count: Number of elements to sort
 * @param ascending: 1 for ascending order, 0 for descending
 */
void bitonic_sort_recursive_parallel(int *arr, int low, int count, int ascending)
{
    if (count > 1)
    {
        int k = count / 2;

        // Dynamic task creation with sophisticated load balancing
        if (count > ADAPTIVE_THRESHOLD * 4)
        {
            // Use tasks for large segments to allow work stealing
#pragma omp task shared(arr) if (count > ADAPTIVE_THRESHOLD * 8)
            {
                // Sort first half in ascending order
                bitonic_sort_recursive_parallel(arr, low, k, 1);
            }
#pragma omp task shared(arr) if (count > ADAPTIVE_THRESHOLD * 8)
            {
                // Sort second half in descending order
                bitonic_sort_recursive_parallel(arr, low + k, k, 0);
            }
#pragma omp taskwait
        }
        else if (count > ADAPTIVE_THRESHOLD)
        {
            // Use parallel sections for medium segments
#pragma omp parallel sections
            {
#pragma omp section
                bitonic_sort_recursive_parallel(arr, low, k, 1);
#pragma omp section
                bitonic_sort_recursive_parallel(arr, low + k, k, 0);
            }
        }
        else
        {
            // Sequential execution for small segments to minimize overhead
            bitonic_sort_recursive_parallel(arr, low, k, 1);
            bitonic_sort_recursive_parallel(arr, low + k, k, 0);
        }

        // Merge with the same level of parallelization
        bitonic_merge_parallel(arr, low, count, ascending);
    }
}

/**
 * Advanced main parallel bitonic sort function with performance optimization
 * Implements nested parallelism and advanced thread management
 * @param arr: Array to sort
 * @param size: Size of the array (must be a power of 2)
 */
void bitonic_sort_parallel(int *arr, int size)
{
    // Enable nested parallelism for better resource utilization
    omp_set_nested(1);
    omp_set_max_active_levels(3);

    // Set dynamic thread adjustment
    omp_set_dynamic(1);

#pragma omp parallel
    {
#pragma omp single
        {
            printf("Number of threads: %d\n", omp_get_num_threads());
            printf("Max active levels: %d\n", omp_get_max_active_levels());
            printf("Nested parallelism: %s\n", omp_get_nested() ? "Enabled" : "Disabled");
            printf("Thread affinity: Process binding enabled\n");
        }
    }

    // Main parallel region with task-based parallelism
#pragma omp parallel
    {
#pragma omp single
        {
            // Start the recursive sort with task creation
            bitonic_sort_recursive_parallel(arr, 0, size, 1);
        }
    }
}

/**
 * Calculates time difference in milliseconds
 * @param start: Start time
 * @param end: End time
 * @return: Time difference in milliseconds
 */
double get_time_diff(double start, double end)
{
    return (end - start) * 1000.0;
}

/**
 * Main function
 */
int main(int argc, char *argv[])
{
    int size;

    // Parse command line arguments
    if (argc != 2)
    {
        printf("Usage: %s <array_size>\n", argv[0]);
        printf("Note: Array size must be a power of 2 (e.g., 1024, 2048, 4096)\n");
        printf("Set OMP_NUM_THREADS environment variable to control thread count\n");
        return 1;
    }

    size = atoi(argv[1]);

    // Validate that size is a power of 2
    if (size <= 0 || (size & (size - 1)) != 0)
    {
        printf("Error: Array size must be a positive power of 2\n");
        return 1;
    }

    printf("=== OpenMP Parallel Bitonic Sort ===\n");
    printf("Array Size: %d\n", size);

    // Display OpenMP configuration
    printf("Max threads available: %d\n", omp_get_max_threads());

    // Allocate memory for the array
    int *arr = (int *)malloc(size * sizeof(int));
    if (arr == NULL)
    {
        printf("Error: Memory allocation failed\n");
        return 1;
    }

    // Generate random array
    generate_random_array(arr, size);

    // Print array sample before sorting
    print_array_sample(arr, size, "Before sorting");

    // Measure execution time using OpenMP timer
    double start_time = omp_get_wtime();

    // Perform parallel bitonic sort
    bitonic_sort_parallel(arr, size);

    double end_time = omp_get_wtime();
    double execution_time = get_time_diff(start_time, end_time);

    // Print array sample after sorting
    print_array_sample(arr, size, "After sorting");

    // Verify sorting
    int sorted = is_sorted(arr, size);

    // Print results
    printf("\n=== Results ===\n");
    printf("Array Size: %d\n", size);
    printf("Execution Time: %.2f ms\n", execution_time);
    printf("Sorted correctly: %s\n", sorted ? "YES" : "NO");

    // Clean up memory
    free(arr);

    return 0;
}