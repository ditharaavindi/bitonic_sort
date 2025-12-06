#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <omp.h>

static int next_power_of_two(int n)
{
    int p = 1;
    while (p < n)
    {
        p <<= 1;
    }
    return p;
}

static int read_input(const char *path, int **out_data)
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
    *out_data = buffer;
    return size;
}

static void write_output(const char *path, const int *data, int count)
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

static void bitonic_sort(int *data, int n)
{
    for (int k = 2; k <= n; k <<= 1)
    {
        for (int j = k >> 1; j > 0; j >>= 1)
        {
#pragma omp parallel for schedule(static)
            for (int i = 0; i < n; ++i)
            {
                int ixj = i ^ j;
                if (ixj > i)
                {
                    int ascending = ((i & k) == 0);
                    if ((data[i] > data[ixj]) == ascending)
                    {
                        int tmp = data[i];
                        data[i] = data[ixj];
                        data[ixj] = tmp;
                    }
                }
            }
        }
    }
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    int *values = NULL;
    int count = read_input(argv[1], &values);
    if (count <= 0)
    {
        return 1;
    }

    int padded = next_power_of_two(count);
    if (padded != count)
    {
        int *tmp = realloc(values, padded * sizeof(int));
        if (!tmp)
        {
            free(values);
            fprintf(stderr, "Memory allocation failed\n");
            return 1;
        }
        values = tmp;
        for (int i = count; i < padded; ++i)
        {
            values[i] = INT_MAX; // sentinel to keep padding at the end
        }
    }

    double start = omp_get_wtime();
    bitonic_sort(values, padded);
    double end = omp_get_wtime();

    int threads_used = omp_get_max_threads();
    printf("Dataset size: %d\n", count);
    printf("Threads: %d\n", threads_used);
    printf("Execution time (s): %.6f\n", end - start);

    write_output("OutputFiles/openmp_output.txt", values, count);

    free(values);
    return 0;
}
