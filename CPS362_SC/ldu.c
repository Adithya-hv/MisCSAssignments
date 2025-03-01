#include <stdio.h>


int main() {

    double A[3][3] = {
        {2.0,  3.0,  1.0},
        {4.0,  7.0,  2.0},
        {6.0, 18.0, -1.0}
    };

    double L[3][3] = {0};  
    double U[3][3] = {0};

    // set diagonals to one
    for (int i = 0; i < 3; i++) {
        L[i][i] = 1.0;
    }

      // first row of Upper is always the same
      U[0][0] = A[0][0];
      U[0][1] = A[0][1];
      U[0][2] = A[0][2];
  
      // getting multipliers for :
      L[1][0] = A[1][0] / U[0][0];
      L[2][0] = A[2][0] / U[0][0];
  
      //  second row
      U[1][0] = 0.0;
      U[1][1] = A[1][1] - L[1][0] * U[0][1];
      U[1][2] = A[1][2] - L[1][0] * U[0][2];
  
      // compute multiplier for r 3 and c 2
      L[2][1] = (A[2][1] - L[2][0] * U[0][1]) / U[1][1];

      U[2][0] = 0.0; 
      U[2][1] = 0.0; 
      U[2][2] = A[2][2] - L[2][0] * U[0][2] - L[2][1] * U[1][2];

      // Soo now we have LU but we want D too, to get D
      // we make U normalized to have all its diag elements as 1
  
      double D[3][3] = {0};     
      double U_final[3][3] = {0}; 
  
    	for (int i = 0; i < 3; i++) {
        	for (int j = 0; j < 3; j++) {
            	if (i == j) {
                    D[i][j] = U[i][i];   // diagonal entry of U becomes D's entry
                	U_final[i][j] = 1.0;    
              } else if (i < j) {
                    U_final[i][j] = U[i][j] / U[i][i];
              } else {
                    U_final[i][j] = 0.0;
              }
          }
      }
  
      // Print out A, L, U, D, and U_final
      printf("Matrix A:\n");
      for (int i = 0; i < 3; i++){
          for (int j = 0; j < 3; j++){
              printf("%lf ", A[i][j]);
          }
          printf("\n");
      }
      printf("\n");
  
      printf("L matrix :\n");
      for (int i = 0; i < 3; i++){
          for (int j = 0; j < 3; j++){
              printf("%lf ", L[i][j]);
          }
          printf("\n");
      }
      printf("\n");
  
      printf("U matrix (from LU):\n");
      for (int i = 0; i < 3; i++){
          for (int j = 0; j < 3; j++){
              printf("%lf ", U[i][j]);
          }
          printf("\n");
      }
      printf("\n");
  
      printf("D matrix (from LDU):\n");
      for (int i = 0; i < 3; i++){
          for (int j = 0; j < 3; j++){
              printf("%lf ", D[i][j]);
          }
          printf("\n");
      }
      printf("\n");
  
      printf("U_unit matrix (from LDU):\n");
      for (int i = 0; i < 3; i++){
          for (int j = 0; j < 3; j++){
              printf("%lf ", U_final[i][j]);
          }
          printf("\n");
      }
      printf("\n");
  
      return 0;


}