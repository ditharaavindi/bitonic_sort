/**
 * CUDA GPU Bitonic Sort Implementation
 *
 * This program implements the bitonic sort algorithm using CUDA for GPU parallelization.
 * The compare-and-swap operations are performed in parallel using CUDA threads and blocks.
 * Kernel execution time is measured using CUDA events.
 *
 * Time Complexity: O(n log²n)
 * Space Complexity: O(n)
 *
 * Compilation: nvcc cuda_bitonic.cu -o cuda_bitonic
 * Usage: ./cuda_bitonic 1024
 *
 * Author: Parallel Computing Assignment 3
 * Date: December 2025
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include <cuda_runtime.h>

// CUDA error checking macro
#define CUDA_CHECK(call)                                                                         \
    do                                                                                           \
    {                                                                                            \
        cudaError_t error = call;                                                                \
        if (error != cudaSuccess)                                                                \
        {                                                                                        \
            printf("CUDA error at %s:%d - %s\n", __FILE__, __LINE__, cudaGetErrorString(error)); \
            exit(1);                                                                             \
        }                                                                                        \
    } while (0)

// Constants
#define THREADS_PER_BLOCK 256
#define MAX_THREADS_PER_BLOCK 1024

// Function prototypes
void generate_random_array(int *arr, int size);
void print_array_sample(int *arr, int size, const char *label);
int is_sorted(int *arr, int size);
void bitonic_sort_cpu(int *arr, int size);

// CUDA kernels
__global__ void bitonic_sort_kernel(int *arr, int stage, int step, int size);
__device__ void compare_and_swap(int *arr, int i, int j, int ascending);

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
 * CUDA device function: Compare and swap two elements
 * @param arr: Array containing the elements
 * @param i: Index of first element
 * @param j: Index of second element
 * @param ascending: 1 for ascending order, 0 for descending
 */
__device__ void compare_and_swap(int *arr, int i, int j, int ascending)
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
 * CUDA kernel for bitonic sort
 * @param arr: Device array to sort
 * @param stage: Current stage of bitonic sort
 * @param step: Current step within the stage
 * @param size: Size of the array
 */
__global__ void bitonic_sort_kernel(int *arr, int stage, int step, int size)
{
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int pair_distance = step;

    if (tid < size / 2)
    {
        int i = tid % pair_distance + (tid / pair_distance) * pair_distance * 2;
        int j = i + pair_distance;

        if (j < size)
        {
            // Determine sorting direction based on stage
            int ascending = ((tid / stage) % 2) == 0;
            compare_and_swap(arr, i, j, ascending);
        }
    }
}

/**
 * Optimized CUDA kernel using shared memory
 * @param arr: Device array to sort
 * @param stage: Current stage of bitonic sort
 * @param step: Current step within the stage
 * @param size: Size of the array
 */
__global__ void bitonic_sort_shared_kernel(int *arr, int stage, int step, int size)
{
    extern __shared__ int shared_arr[];

    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int local_tid = threadIdx.x;
    int block_size = blockDim.x;

    // Load data into shared memory
    if (tid < size)
    {
        shared_arr[local_tid] = arr[tid];
        if (tid + block_size < size)
        {
            shared_arr[local_tid + block_size] = arr[tid + block_size];
        }
    }

    __syncthreads();

    // Perform bitonic sort steps that fit within shared memory
    for (int current_step = step; current_step > 0 && current_step >= block_size; current_step /= 2)
    {
        int pair_distance = current_step;

        if (local_tid < block_size / 2)
        {
            int i = local_tid % pair_distance + (local_tid / pair_distance) * pair_distance * 2;
            int j = i + pair_distance;

            if (j < block_size * 2 && tid < size)
            {
                int ascending = ((tid / stage) % 2) == 0;
                if ((shared_arr[i] > shared_arr[j]) == ascending)
                {
                    int temp = shared_arr[i];
                    shared_arr[i] = shared_arr[j];
                    shared_arr[j] = temp;
                }
            }
        }

        __syncthreads();
    }

    // Write back to global memory
    if (tid < size)
    {
        arr[tid] = shared_arr[local_tid];
        if (tid + block_size < size)
        {
            arr[tid + block_size] = shared_arr[local_tid + block_size];
        }
    }
}

/**
 * CUDA bitonic sort implementation
 * @param h_arr: Host array to sort
 * @param size: Size of the array
 * @param kernel_time_ms: Pointer to store kernel execution time
 */
void bitonic_sort_cuda(int *h_arr, int size, float *kernel_time_ms)
{
    int *d_arr;
    cudaEvent_t start, stop;

    // Create CUDA events for timing
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    // Allocate device memory
    CUDA_CHECK(cudaMalloc(&d_arr, size * sizeof(int)));

    // Copy data from host to device
    CUDA_CHECK(cudaMemcpy(d_arr, h_arr, size * sizeof(int), cudaMemcpyHostToDevice));

    // Configure kernel launch parameters
    int num_blocks = (size / 2 + THREADS_PER_BLOCK - 1) / THREADS_PER_BLOCK;

    printf("CUDA Configuration:\n");
    printf("Threads per block: %d\n", THREADS_PER_BLOCK);
    printf("Number of blocks: %d\n", num_blocks);
    printf("Total threads: %d\n", num_blocks * THREADS_PER_BLOCK);

    // Start timing
    CUDA_CHECK(cudaEventRecord(start));

    // Perform bitonic sort
    for (int stage = 2; stage <= size; stage *= 2)
    {
        for (int step = stage / 2; step > 0; step /= 2)
        {
            // Use shared memory kernel for smaller steps, global memory for larger
            if (step <= THREADS_PER_BLOCK && stage <= 2 * THREADS_PER_BLOCK)
            {
                int shared_mem_size = 2 * THREADS_PER_BLOCK * sizeof(int);
                bitonic_sort_shared_kernel<<<num_blocks, THREADS_PER_BLOCK, shared_mem_size>>>(
                    d_arr, stage, step, size);
            }
            else
            {
                bitonic_sort_kernel<<<num_blocks, THREADS_PER_BLOCK>>>(d_arr, stage, step, size);
            }

            // Check for kernel launch errors
            CUDA_CHECK(cudaGetLastError());
        }
    }

    // Synchronize and stop timing
    CUDA_CHECK(cudaDeviceSynchronize());
    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    // Calculate kernel execution time
    CUDA_CHECK(cudaEventElapsedTime(kernel_time_ms, start, stop));

    // Copy result back to host
    CUDA_CHECK(cudaMemcpy(h_arr, d_arr, size * sizeof(int), cudaMemcpyDeviceToHost));

    // Clean up
    CUDA_CHECK(cudaFree(d_arr));
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));
}

/**
 * CPU implementation for comparison
 */
void compare_and_swap_cpu(int *arr, int i, int j, int ascending)
{
    if ((arr[i] > arr[j]) == ascending)
    {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

void bitonic_merge_cpu(int *arr, int low, int count, int ascending)
{
    if (count > 1)
    {
        int k = count / 2;
        for (int i = low; i < low + k; i++)
        {
            compare_and_swap_cpu(arr, i, i + k, ascending);
        }
        bitonic_merge_cpu(arr, low, k, ascending);
        bitonic_merge_cpu(arr, low + k, k, ascending);
    }
}

void bitonic_sort_recursive_cpu(int *arr, int low, int count, int ascending)
{
    if (count > 1)
    {
        int k = count / 2;
        bitonic_sort_recursive_cpu(arr, low, k, 1);
        bitonic_sort_recursive_cpu(arr, low + k, k, 0);
        bitonic_merge_cpu(arr, low, count, ascending);
    }
}

void bitonic_sort_cpu(int *arr, int size)
{
    bitonic_sort_recursive_cpu(arr, 0, size, 1);
}

/**
 * Main function
 */
int main(int argc, char *argv[])
{
    int size;
    int *h_arr, *h_arr_cpu;
    float kernel_time;
    clock_t cpu_start, cpu_end;

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

    printf("=== CUDA GPU Bitonic Sort ===\n");
    printf("Array Size: %d\n", size);

    // Query and display GPU information
    int device_count;
    CUDA_CHECK(cudaGetDeviceCount(&device_count));
    if (device_count == 0)
    {
        printf("No CUDA-capable devices found!\n");
        return 1;
    }

    cudaDeviceProp device_prop;
    CUDA_CHECK(cudaGetDeviceProperties(&device_prop, 0));
    printf("GPU: %s\n", device_prop.name);
    printf("Compute Capability: %d.%d\n", device_prop.major, device_prop.minor);
    printf("Global Memory: %.2f GB\n", device_prop.totalGlobalMem / (1024.0 * 1024.0 * 1024.0));

    // Allocate host memory
    h_arr = (int *)malloc(size * sizeof(int));
    h_arr_cpu = (int *)malloc(size * sizeof(int));
    if (h_arr == NULL || h_arr_cpu == NULL)
    {
        printf("Error: Host memory allocation failed\n");
        return 1;
    }

    // Generate random array
    generate_random_array(h_arr, size);

    // Create copy for CPU comparison
    memcpy(h_arr_cpu, h_arr, size * sizeof(int));

    // Print array sample before sorting
    print_array_sample(h_arr, size, "Before sorting (GPU)");

    // Perform CUDA bitonic sort
    bitonic_sort_cuda(h_arr, size, &kernel_time);

    // Print array sample after GPU sorting
    print_array_sample(h_arr, size, "After sorting (GPU)");

    // Verify GPU sorting
    int gpu_sorted = is_sorted(h_arr, size);

    // Perform CPU bitonic sort for comparison
    printf("\nPerforming CPU comparison...\n");
    cpu_start = clock();
    bitonic_sort_cpu(h_arr_cpu, size);
    cpu_end = clock();
    double cpu_time = ((double)(cpu_end - cpu_start) / CLOCKS_PER_SEC) * 1000.0;

    // Verify CPU sorting
    int cpu_sorted = is_sorted(h_arr_cpu, size);

    // Print results
    printf("\n=== Results ===\n");
    printf("Array Size: %d\n", size);
    printf("GPU Kernel Time: %.2f ms\n", kernel_time);
    printf("CPU Time: %.2f ms\n", cpu_time);
    printf("Speedup: %.2fx\n", cpu_time / kernel_time);
    printf("GPU Sorted correctly: %s\n", gpu_sorted ? "YES" : "NO");
    printf("CPU Sorted correctly: %s\n", cpu_sorted ? "YES" : "NO");

    // Clean up memory
    free(h_arr);
    free(h_arr_cpu);

    return 0;
}