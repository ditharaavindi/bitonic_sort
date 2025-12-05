/**
 * Serial Bitonic Sort Implementation
 *
 * This program implements the bitonic sort algorithm in a sequential manner.
 * Bitonic sort is a comparison-based sorting algorithm that works by
 * recursively building bitonic sequences and then sorting them.
 *
 * Time Complexity: O(n log²n)
 * Space Complexity: O(n)
 *
 * Author: Parallel Computing Assignment 3
 * Date: December 2025
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>

// Function prototypes
void generate_random_array(int *arr, int size);
void print_array_sample(int *arr, int size, const char *label);
int is_sorted(int *arr, int size);
void compare_and_swap(int *arr, int i, int j, int ascending);
void bitonic_merge(int *arr, int low, int count, int ascending);
void bitonic_sort_recursive(int *arr, int low, int count, int ascending);
void bitonic_sort(int *arr, int size);
double get_time_diff(clock_t start, clock_t end);

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
 * Merges a bitonic sequence into a monotonic sequence
 * @param arr: Array containing the bitonic sequence
 * @param low: Starting index of the sequence
 * @param count: Number of elements in the sequence
 * @param ascending: 1 for ascending order, 0 for descending
 */
void bitonic_merge(int *arr, int low, int count, int ascending)
{
    if (count > 1)
    {
        int k = count / 2;

        // Compare and swap elements in the first half with corresponding elements in the second half
        for (int i = low; i < low + k; i++)
        {
            compare_and_swap(arr, i, i + k, ascending);
        }

        // Recursively merge the two halves
        bitonic_merge(arr, low, k, ascending);
        bitonic_merge(arr, low + k, k, ascending);
    }
}

/**
 * Recursively builds bitonic sequences and sorts them
 * @param arr: Array to sort
 * @param low: Starting index
 * @param count: Number of elements to sort
 * @param ascending: 1 for ascending order, 0 for descending
 */
void bitonic_sort_recursive(int *arr, int low, int count, int ascending)
{
    if (count > 1)
    {
        int k = count / 2;

        // Sort first half in ascending order
        bitonic_sort_recursive(arr, low, k, 1);

        // Sort second half in descending order
        bitonic_sort_recursive(arr, low + k, k, 0);

        // Merge the entire sequence in the specified order
        bitonic_merge(arr, low, count, ascending);
    }
}

/**
 * Main bitonic sort function
 * @param arr: Array to sort
 * @param size: Size of the array (must be a power of 2)
 */
void bitonic_sort(int *arr, int size)
{
    bitonic_sort_recursive(arr, 0, size, 1); // Sort in ascending order
}

/**
 * Calculates time difference in milliseconds
 * @param start: Start time
 * @param end: End time
 * @return: Time difference in milliseconds
 */
double get_time_diff(clock_t start, clock_t end)
{
    return ((double)(end - start) / CLOCKS_PER_SEC) * 1000.0;
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
        return 1;
    }

    size = atoi(argv[1]);

    // Validate that size is a power of 2
    if (size <= 0 || (size & (size - 1)) != 0)
    {
        printf("Error: Array size must be a positive power of 2\n");
        return 1;
    }

    printf("=== Serial Bitonic Sort ===\n");
    printf("Array Size: %d\n", size);

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

    // Measure execution time
    clock_t start_time = clock();

    // Perform bitonic sort
    bitonic_sort(arr, size);

    clock_t end_time = clock();
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