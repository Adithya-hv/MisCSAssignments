# Question-2

(50 pts) Design an iteration based parallel Strassen's algorithm. No recursion. Matrices involved into standard multiplications in the algorithm should be small enough. Pseudo code is required. In addition, please argue the time and the space complexity of your algorithm. (Introduce hyperparameters into your complexity analysis as needed.)

# Answer

This quesiton needs an iteration based, non recursive, and parallelized version of Strassen's matrix multiplication algorithm. The goal is to replace traditional recursion with loops and simulate parallel computation for performance gains.

## Strassen’s Algorithm

The Algorithm basically improves on the standard matrix multiplication time complexity. Instead of performing 8 multiplications on submatrices, it reduces this to 7.

Given two N x N matrices A and B, they are divided into N/2 x N/2 submatrices and used to compute 7 intermediary products (M1 through M7). These products are then combined to compute the final result C.

This reduces the time complexity from O(n^3) to approximately O(n^2.81).

## Parallelization Strategy

M1 to M7 are all independent calculations and can be executed in parallel using threads. Once those values are computed, we use them to form the final output submatrices (C11 to C22). We used python to make the code more managable.

Parallelism can also be introduced in the matrix addition and subtraction steps, although the gains there are smaller compared to the multiplication steps.

## Space Complexity

The space complexity is determined by the storage requirements for the input matrices, the output matrix, and the temporary matrices used during computation. At each recursive level, additional matrices are allocated to hold intermediate results, leading to an overall space complexity of O(n²).
