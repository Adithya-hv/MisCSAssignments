#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MIN_SIZE 512
#define MAX_SIZE 8192
#define STEP_SIZE 512
#define NUM_TESTS 10
#define NUM_TRIALS 5

void naive_transpose(int n, double *A, double *B) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            B[j*n + i] = A[i*n + j];
        }
    }
}

void blocked_transpose(int n, double *A, double *B, int block_size) {
    for (int i = 0; i < n; i += block_size) {
        for (int j = 0; j < n; j += block_size) {
            for (int ii = i; ii < i + block_size && ii < n; ii++) {
                for (int jj = j; jj < j + block_size && jj < n; jj++) {
                    B[jj*n + ii] = A[ii*n + jj];
                }
            }
        }
    }
}

int main() {
    srand(time(NULL));

    FILE *file = fopen("results.csv", "w");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    fprintf(file, "Matrix Size,Block Size,Blocked Time (ms)\n");

    for (int size = MIN_SIZE; size <= MAX_SIZE; size += STEP_SIZE) {
        double *A = (double *)malloc(size * size * sizeof(double));
        double *B = (double *)malloc(size * size * sizeof(double));

        for (int i = 0; i < size * size; i++) {
            A[i] = (double)rand() / RAND_MAX;
        }

        for (int block_size = 8; block_size <= 128; block_size *= 2) {
            double total_blocked_time = 0.0;

            for (int t = 0; t < NUM_TRIALS; t++) {
                clock_t start = clock();
                blocked_transpose(size, A, B, block_size);
                total_blocked_time += ((double)(clock() - start)) / CLOCKS_PER_SEC * 1000;
            }

            double avg_blocked_time = total_blocked_time / NUM_TRIALS;
            fprintf(file, "%d,%d,%.3f\n", size, block_size, avg_blocked_time);
        }

        free(A);
        free(B);
    }

    fclose(file);
    printf("Results written to results.csv\n");

    return 0;
}
