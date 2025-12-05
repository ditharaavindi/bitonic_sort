/**
 * MPI Parallel Bitonic Sort Implementation
 *
 * This program implements the bitonic sort algorithm using MPI for distributed parallelization.
 * The array is distributed across processes, local bitonic sort is performed, and then
 * segments are merged using MPI communication patterns.
 *
 * Time Complexity: O(n log²n)
 * Space Complexity: O(n/p) per process, where p is the number of processes
 *
 * Compilation: mpicc mpi_bitonic.c -o mpi_bitonic
 * Usage: mpirun -np 4 ./mpi_bitonic 1024
 *
 * Author: Parallel Computing Assignment 3
 * Date: December 2025
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include <mpi.h>

// Function prototypes
void generate_random_array(int *arr, int size);
void print_array_sample(int *arr, int size, const char *label);
int is_sorted(int *arr, int size);
void compare_and_swap(int *arr, int i, int j, int ascending);
void bitonic_merge(int *arr, int low, int count, int ascending);
void bitonic_sort_recursive(int *arr, int low, int count, int ascending);
void bitonic_sort_local(int *arr, int size);
void merge_split(int *arr, int size, int partner_rank, int ascending, MPI_Comm comm);
void bitonic_sort_mpi(int *local_arr, int local_size, int rank, int num_procs, MPI_Comm comm);

/**
 * Generates random array values
 * @param arr: Array to fill with random values
 * @param size: Size of the array
 */
void generate_random_array(int *arr, int size)
{
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
 * Merges a bitonic sequence into a monotonic sequence (local version)
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

        // Compare and swap elements
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
 * Recursively builds bitonic sequences and sorts them (local version)
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
 * Local bitonic sort function
 * @param arr: Array to sort
 * @param size: Size of the array (must be a power of 2)
 */
void bitonic_sort_local(int *arr, int size)
{
    bitonic_sort_recursive(arr, 0, size, 1); // Sort in ascending order
}

/**
 * Comparison function for qsort
 */
int compare_ints(const void *a, const void *b)
{
    return (*(int *)a - *(int *)b);
}

/**
 * Merge and split operation for MPI bitonic sort
 * @param arr: Local array
 * @param size: Size of local array
 * @param partner_rank: Rank of partner process
 * @param ascending: Direction of sorting
 * @param comm: MPI communicator
 */
void merge_split(int *arr, int size, int partner_rank, int ascending, MPI_Comm comm)
{
    int *temp_arr = (int *)malloc(size * sizeof(int));
    int *merged_arr = (int *)malloc(2 * size * sizeof(int));

    // Exchange data with partner
    MPI_Sendrecv(arr, size, MPI_INT, partner_rank, 0,
                 temp_arr, size, MPI_INT, partner_rank, 0,
                 comm, MPI_STATUS_IGNORE);

    // Merge the two arrays
    int i = 0, j = 0, k = 0;
    while (i < size && j < size)
    {
        if (arr[i] <= temp_arr[j])
        {
            merged_arr[k++] = arr[i++];
        }
        else
        {
            merged_arr[k++] = temp_arr[j++];
        }
    }

    // Copy remaining elements
    while (i < size)
        merged_arr[k++] = arr[i++];
    while (j < size)
        merged_arr[k++] = temp_arr[j++];

    // Split the merged array
    int my_rank;
    MPI_Comm_rank(comm, &my_rank);

    if ((my_rank < partner_rank && ascending) || (my_rank > partner_rank && !ascending))
    {
        // Take the smaller half
        for (int i = 0; i < size; i++)
        {
            arr[i] = merged_arr[i];
        }
    }
    else
    {
        // Take the larger half
        for (int i = 0; i < size; i++)
        {
            arr[i] = merged_arr[size + i];
        }
    }

    free(temp_arr);
    free(merged_arr);
}

/**
 * MPI Bitonic sort main function
 * @param local_arr: Local array for this process
 * @param local_size: Size of local array
 * @param rank: Process rank
 * @param num_procs: Number of processes
 * @param comm: MPI communicator
 */
void bitonic_sort_mpi(int *local_arr, int local_size, int rank, int num_procs, MPI_Comm comm)
{
    // First, sort local array
    bitonic_sort_local(local_arr, local_size);

    // Perform bitonic merge across processes
    for (int stage = 1; stage < num_procs; stage *= 2)
    {
        for (int step = stage; step > 0; step /= 2)
        {
            // Find partner process
            int partner = rank ^ step;

            if (partner < num_procs)
            {
                // Determine sorting direction
                int ascending = ((rank & stage) == 0);

                // Perform merge-split with partner
                merge_split(local_arr, local_size, partner, ascending, comm);
            }
        }
    }
}

/**
 * Main function
 */
int main(int argc, char *argv[])
{
    int rank, num_procs;
    int total_size, local_size;
    int *global_arr = NULL;
    int *local_arr = NULL;
    double start_time, end_time;

    // Initialize MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    // Parse command line arguments
    if (argc != 2)
    {
        if (rank == 0)
        {
            printf("Usage: mpirun -np <num_procs> %s <array_size>\n", argv[0]);
            printf("Note: Array size must be a power of 2 and divisible by number of processes\n");
        }
        MPI_Finalize();
        return 1;
    }

    total_size = atoi(argv[1]);
    local_size = total_size / num_procs;

    // Validate input
    if (total_size <= 0 || (total_size & (total_size - 1)) != 0 ||
        (num_procs & (num_procs - 1)) != 0 || total_size % num_procs != 0)
    {
        if (rank == 0)
        {
            printf("Error: Array size must be a power of 2, number of processes must be a power of 2,\n");
            printf("       and array size must be divisible by number of processes\n");
        }
        MPI_Finalize();
        return 1;
    }

    if (rank == 0)
    {
        printf("=== MPI Parallel Bitonic Sort ===\n");
        printf("Array Size: %d\n", total_size);
        printf("Number of Processes: %d\n", num_procs);
        printf("Local Array Size: %d\n", local_size);
    }

    // Allocate memory for local array
    local_arr = (int *)malloc(local_size * sizeof(int));
    if (local_arr == NULL)
    {
        printf("Process %d: Memory allocation failed\n", rank);
        MPI_Finalize();
        return 1;
    }

    // Process 0 generates and distributes data
    if (rank == 0)
    {
        global_arr = (int *)malloc(total_size * sizeof(int));
        if (global_arr == NULL)
        {
            printf("Process 0: Global array allocation failed\n");
            MPI_Finalize();
            return 1;
        }

        // Initialize random seed
        srand(time(NULL));
        generate_random_array(global_arr, total_size);

        // Print array sample before sorting
        print_array_sample(global_arr, total_size, "Before sorting");
    }

    // Distribute data to all processes
    MPI_Scatter(global_arr, local_size, MPI_INT,
                local_arr, local_size, MPI_INT,
                0, MPI_COMM_WORLD);

    // Synchronize and start timing
    MPI_Barrier(MPI_COMM_WORLD);
    start_time = MPI_Wtime();

    // Perform MPI bitonic sort
    bitonic_sort_mpi(local_arr, local_size, rank, num_procs, MPI_COMM_WORLD);

    // Synchronize and end timing
    MPI_Barrier(MPI_COMM_WORLD);
    end_time = MPI_Wtime();

    // Gather sorted data
    MPI_Gather(local_arr, local_size, MPI_INT,
               global_arr, local_size, MPI_INT,
               0, MPI_COMM_WORLD);

    // Process 0 prints results
    if (rank == 0)
    {
        double execution_time = (end_time - start_time) * 1000.0; // Convert to milliseconds

        // Print array sample after sorting
        print_array_sample(global_arr, total_size, "After sorting");

        // Verify sorting
        int sorted = is_sorted(global_arr, total_size);

        // Print results
        printf("\n=== Results ===\n");
        printf("Array Size: %d\n", total_size);
        printf("Number of Processes: %d\n", num_procs);
        printf("Execution Time: %.2f ms\n", execution_time);
        printf("Sorted correctly: %s\n", sorted ? "YES" : "NO");

        free(global_arr);
    }

    // Clean up
    free(local_arr);
    MPI_Finalize();

    return 0;
}