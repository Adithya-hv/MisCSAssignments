# LU Decomposition

The program just converts a given 3x3 matrix into 3 components:

- L a lower triangular matrix
- D a Diagonal matrix
- U a Upper triangular matrix (temp)
- U_final is normalized and has diagonals as 1

It uses Gaussian elimination and finds the multiples to convert A into U and stores that in U, and finally, it stores U's diagonal and normalizes U into U_final

### Sample Output:

Matrix A:<br>
2.000000 3.000000 1.000000 <br>
4.000000 7.000000 2.000000<br>
6.000000 18.000000 -1.000000<br>

L matrix :<br>
1.000000 0.000000 0.000000<br>
2.000000 1.000000 0.000000<br>
3.000000 9.000000 1.000000<br>

U matrix:<br>
2.000000 3.000000 1.000000<br>
0.000000 1.000000 0.000000<br>
0.000000 0.000000 -4.000000<br>

D matrix:<br>
2.000000 0.000000 0.000000<br>
0.000000 1.000000 0.000000<br>
0.000000 0.000000 -4.000000<br>

U_final matrix :<br>
1.000000 1.500000 0.500000<br>
0.000000 1.000000 0.000000<br>
0.000000 0.000000 1.000000<br>
