#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

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
        for (int idx = 0; idx < local_n; ++idx)
        {
            local[idx] = merged[idx];
        }
    }
    else
    {
        for (int idx = 0; idx < local_n; ++idx)
        {
            local[idx] = merged[local_n + idx];
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

    qsort(local_data, local_n, sizeof(int), int_compare);
    distributed_bitonic(local_data, local_n, rank, world_size);

    MPI_Barrier(MPI_COMM_WORLD);
    double end = MPI_Wtime();

    int *gathered = NULL;
    if (rank == 0)
    {
        gathered = malloc(padded_count * sizeof(int));
        if (!gathered)
        {
            fprintf(stderr, "Memory allocation failed on gather\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
    }

    MPI_Gather(local_data, local_n, MPI_INT, gathered, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        write_output_rank0("OutputFiles/mpi_output.txt", gathered, original_count);
        printf("Processes: %d\n", world_size);
        printf("Execution time (s): %.6f\n", end - start);
    }

    free(local_data);
    free(gathered);
    free(global_data);

    MPI_Finalize();
    return 0;
}
