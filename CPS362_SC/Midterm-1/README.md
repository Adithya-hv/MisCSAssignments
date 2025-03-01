# LU Decomposition

The program just converts a given 3x3 matrix into 3 components:

- L a lower triangular matrix
- D a Diagonal matrix
- U a Upper triangular matrix (temp)
- U_final normalized and has diagonals as 1

It uses Gaussian elimination and finds the multiples to convert A into U and stores that in U, and finally it stores U's diagonal andnormalizes U into U_final

### Sample Output:

Matrix A:
2.000000 3.000000 1.000000
4.000000 7.000000 2.000000
6.000000 18.000000 -1.000000

L matrix :
1.000000 0.000000 0.000000
2.000000 1.000000 0.000000
3.000000 9.000000 1.000000

U matrix:
2.000000 3.000000 1.000000
0.000000 1.000000 0.000000
0.000000 0.000000 -4.000000

D matrix:
2.000000 0.000000 0.000000
0.000000 1.000000 0.000000
0.000000 0.000000 -4.000000

U_final matrix :
1.000000 1.500000 0.500000
0.000000 1.000000 0.000000
0.000000 0.000000 1.000000
