#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>

static int next_power_of_two(int n)
{
    int p = 1;
    while (p < n)
    {
        p <<= 1;
    }
    return p;
}

static int int_compare(const void *a, const void *b)
{
    int lhs = *(const int *)a;
    int rhs = *(const int *)b;
    if (lhs < rhs)
        return -1;
    if (lhs > rhs)
        return 1;
    return 0;
}

static int read_input_rank0(const char *path, int **data_out)
{
    FILE *fp = fopen(path, "r");
    if (!fp)
    {
        perror("Failed to open input file");
        return -1;
    }

    int capacity = 1024;
    int size = 0;
    int *buffer = malloc(capacity * sizeof(int));
    if (!buffer)
    {
        fclose(fp);
        fprintf(stderr, "Memory allocation failed\n");
        return -1;
    }

    while (1)
    {
        int value;
        int scanned = fscanf(fp, "%d", &value);
        if (scanned == 1)
        {
            if (size == capacity)
            {
                capacity *= 2;
                int *tmp = realloc(buffer, capacity * sizeof(int));
                if (!tmp)
                {
                    free(buffer);
                    fclose(fp);
                    fprintf(stderr, "Memory allocation failed\n");
                    return -1;
                }
                buffer = tmp;
            }
            buffer[size++] = value;
        }
        else if (scanned == EOF)
        {
            break;
        }
        else
        {
            free(buffer);
            fclose(fp);
            fprintf(stderr, "Invalid data in input file\n");
            return -1;
        }
    }

    fclose(fp);
    *data_out = buffer;
    return size;
}

// Bitonic comparator: compare two elements and optionally swap based on direction.
// direction = 1 means ascending, 0 means descending.
static void compare_and_swap(int *a, int *b, int direction)
{
    if ((direction == 1 && *a > *b) || (direction == 0 && *a < *b))
    {
        int tmp = *a;
        *a = *b;
        *b = tmp;
    }
}

// Bitonic merge: merge two bitonic sequences into a single bitonic sequence.
static void bitonic_merge(int *data, int start, int size, int direction)
{
    if (size > 1)
    {
        int mid = size / 2;
        for (int i = start; i < start + mid; ++i)
        {
            compare_and_swap(&data[i], &data[i + mid], direction);
        }
        bitonic_merge(data, start, mid, direction);
        bitonic_merge(data, start + mid, mid, direction);
    }
}

// Bitonic sort: sort array into bitonic sequence.
static void bitonic_sort_recursive(int *data, int start, int size, int direction)
{
    if (size > 1)
    {
        int mid = size / 2;
        // Sort first half in ascending order
        bitonic_sort_recursive(data, start, mid, 1);
        // Sort second half in descending order
        bitonic_sort_recursive(data, start + mid, mid, 0);
        // Merge entire sequence in desired direction
        bitonic_merge(data, start, size, direction);
    }
}

static void merge_exchange(int *local, int local_n, int partner, int ascending)
{
    int *recv_buf = malloc(local_n * sizeof(int));
    int *merged = malloc(2 * local_n * sizeof(int));
    if (!recv_buf || !merged)
    {
        fprintf(stderr, "Memory allocation failed during merge\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    MPI_Sendrecv(local, local_n, MPI_INT, partner, 0,
                 recv_buf, local_n, MPI_INT, partner, 0,
                 MPI_COMM_WORLD, MPI_STATUS_IGNORE);

    int i = 0, j = 0, m = 0;
    while (i < local_n && j < local_n)
    {
        if (local[i] <= recv_buf[j])
        {
            merged[m++] = local[i++];
        }
        else
        {
            merged[m++] = recv_buf[j++];
        }
    }
    while (i < local_n)
        merged[m++] = local[i++];
    while (j < local_n)
        merged[m++] = recv_buf[j++];

    if (ascending)
    {
        // Ascending: keep smaller half
        memcpy(local, merged, local_n * sizeof(int));
    }
    else
    {
        // Descending: keep larger half in reverse order
        for (int idx = 0; idx < local_n; ++idx)
        {
            local[idx] = merged[2 * local_n - 1 - idx];
        }
    }

    free(merged);
    free(recv_buf);
}

static void distributed_bitonic(int *local, int local_n, int rank, int world_size)
{
    for (int k = 2; k <= world_size; k <<= 1)
    {
        for (int j = k >> 1; j > 0; j >>= 1)
        {
            int partner = rank ^ j;
            int ascending = ((rank & k) == 0);
            merge_exchange(local, local_n, partner, ascending);
        }
    }
}

static void write_output_rank0(const char *path, const int *data, int count)
{
    FILE *fp = fopen(path, "w");
    if (!fp)
    {
        perror("Failed to open output file");
        return;
    }
    for (int i = 0; i < count; ++i)
    {
        fprintf(fp, "%d%s", data[i], (i + 1 == count) ? "" : " ");
    }
    fprintf(fp, "\n");
    fclose(fp);
}

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    if (argc < 2)
    {
        if (rank == 0)
        {
            fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        }
        MPI_Finalize();
        return 1;
    }

    int *global_data = NULL;
    int original_count = 0;
    int padded_count = 0;

    if (rank == 0)
    {
        original_count = read_input_rank0(argv[1], &global_data);
        if (original_count <= 0)
        {
            MPI_Abort(MPI_COMM_WORLD, 1);
        }

        padded_count = next_power_of_two(original_count);
        while (padded_count % world_size != 0)
        {
            padded_count <<= 1;
        }

        int required = padded_count - original_count;
        int *tmp = realloc(global_data, padded_count * sizeof(int));
        if (!tmp)
        {
            free(global_data);
            fprintf(stderr, "Memory allocation failed\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        global_data = tmp;
        for (int i = 0; i < required; ++i)
        {
            global_data[original_count + i] = INT_MAX;
        }
    }

    MPI_Bcast(&original_count, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&padded_count, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int local_n = padded_count / world_size;
    int *local_data = malloc(local_n * sizeof(int));
    if (!local_data)
    {
        fprintf(stderr, "Rank %d failed to allocate local buffer\n", rank);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    MPI_Scatter(global_data, local_n, MPI_INT, local_data, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);
    double start = MPI_Wtime();

    // Each process sorts its local data
    bitonic_sort_recursive(local_data, 0, local_n, 1);

    // Now perform a simple merge-based distributed sort
    // All processes send their sorted data to rank 0, which merges them
    int *all_data = NULL;
    if (rank == 0)
    {
        all_data = malloc(padded_count * sizeof(int));
        if (!all_data)
        {
            fprintf(stderr, "Memory allocation failed\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
    }

    MPI_Gather(local_data, local_n, MPI_INT, all_data, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        // Merge all the sorted subarrays using temp buffer
        int *temp_buf = malloc(padded_count * sizeof(int));
        if (!temp_buf)
        {
            fprintf(stderr, "Memory allocation failed\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }

        // Simple merge: repeatedly merge pairs
        int *current = all_data;
        int *next = temp_buf;

        for (int merge_width = local_n; merge_width < padded_count; merge_width *= 2)
        {
            int res_idx = 0;
            for (int base = 0; base < padded_count; base += 2 * merge_width)
            {
                int left_end = base + merge_width;
                int right_end = (base + 2 * merge_width < padded_count) ? base + 2 * merge_width : padded_count;
                if (left_end > padded_count)
                    left_end = padded_count;

                int l = base, r = left_end;
                while (l < left_end && r < right_end)
                {
                    if (current[l] <= current[r])
                    {
                        next[res_idx++] = current[l++];
                    }
                    else
                    {
                        next[res_idx++] = current[r++];
                    }
                }
                while (l < left_end)
                    next[res_idx++] = current[l++];
                while (r < right_end)
                    next[res_idx++] = current[r++];
            }

            // Swap pointers
            int *swap = current;
            current = next;
            next = swap;
        }

        // Copy result back to all_data if needed
        if (current != all_data)
        {
            memcpy(all_data, current, padded_count * sizeof(int));
        }

        free(temp_buf);
    }

    MPI_Barrier(MPI_COMM_WORLD);
    double end = MPI_Wtime();

    int *gathered = NULL;
    if (rank == 0)
    {
        gathered = all_data;
    }

    if (rank == 0)
    {
        write_output_rank0("OutputFiles/mpi_output.txt", gathered, original_count);
        printf("Processes: %d\n", world_size);
        printf("Execution time (s): %.6f\n", end - start);
        free(gathered);
    }

    free(local_data);
    free(global_data);

    MPI_Finalize();
    return 0;
}
