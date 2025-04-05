import numpy as np
from concurrent.futures import ThreadPoolExecutor


def strassen_iterative(A, B):
    def naive_multiply(A, B):
        return A @ B

    def add(A, B):
        return A + B

    def sub(A, B):
        return A - B

    n = A.shape[0]
    if n <= THRESHOLD:
        return naive_multiply(A, B)

    mid = n // 2

    A11, A12 = A[:mid, :mid], A[:mid, mid:]
    A21, A22 = A[mid:, :mid], A[mid:, mid:]
    B11, B12 = B[:mid, :mid], B[:mid, mid:]
    B21, B22 = B[mid:, :mid], B[mid:, mid:]

    with ThreadPoolExecutor(max_workers=7) as executor:
        futures = [
            executor.submit(strassen_iterative, add(
                A11, A22), add(B11, B22)),  # M1
            executor.submit(strassen_iterative, add(
                A21, A22), B11),            # M2
            executor.submit(strassen_iterative, A11,
                            sub(B12, B22)),            # M3
            executor.submit(strassen_iterative, A22,
                            sub(B21, B11)),            # M4
            executor.submit(strassen_iterative, add(
                A11, A12), B22),            # M5
            executor.submit(strassen_iterative, sub(
                A21, A11), add(B11, B12)),  # M6
            executor.submit(strassen_iterative, sub(
                A12, A22), add(B21, B22)),  # M7
        ]
        M1, M2, M3, M4, M5, M6, M7 = [f.result() for f in futures]

    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(sub(add(M1, M3), M2), M6)

    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    C = np.vstack((top, bottom))
    return C


N = 512
A = np.random.rand(N, N)
B = np.random.rand(N, N)

C = strassen_iterative(A, B)

if np.allclose(C, A @ B):
    print("The Algorithm is correct")
else:
    print("The Algorithm is incorrect")
