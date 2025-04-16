import numpy as np


def hh_qr(input_matrix):
    num_rows = input_matrix.shape[0]
    Q_matrix = np.eye(num_rows)
    R_matrix = input_matrix.copy()

    for col_index in range(num_rows - 1):  # Step-4 from image
        # Step-1 from image
        v_column = R_matrix[col_index:, col_index]

        # Step-2 from image
        v_reflection_target = np.zeros_like(v_column)
        v_reflection_target[0] = np.linalg.norm(
            v_column) * (1 if v_column[0] >= 0 else -1)
        v_inter_u = v_column + v_reflection_target
        v_hh = v_inter_u / np.linalg.norm(v_inter_u)

        # Step-3 from image
        hh_matrix_H = np.eye(num_rows)
        hh_matrix_H[col_index:, col_index:] -= 2.0 * np.outer(v_hh, v_hh)

        R_matrix = hh_matrix_H @ R_matrix
        Q_matrix = Q_matrix @ hh_matrix_H.T

    return Q_matrix, R_matrix


def qr_algorithm(matrix_A, num_iterations=10000):  # Step-5 from image
    current_matrix = matrix_A.copy()
    for _ in range(num_iterations):
        Q_matrix, R_matrix = hh_qr(current_matrix)
        current_matrix = R_matrix @ Q_matrix
    return np.diag(current_matrix)  # Step-6 from image (after loops done)


matrix_A = np.array([
    [1.0, 3.0, 0.0],
    [3.0, 1.0, 3.0],
    [0.0, 3.0, 1.0]
])

eigenvalue_estimates = qr_algorithm(matrix_A)  # Step-6 result
print("Eigenvalues:", eigenvalue_estimates)
