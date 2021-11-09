import numpy as np
from scipy.linalg import hessenberg
# import sympy as sym


# Mendekomposisi matriks A menjadi tuple of (U,S,V^t)
# dengan A = U . S . V^t
def svd(A: np.matrix) -> (np.matrix, np.matrix, np.matrix):
    AT = np.transpose(A)
    AAT = np.matrix(np.matmul(A, AT))
    ATA = np.matrix(np.matmul(AT, A))

    egv_list, V = eigen(ATA)
    egv_list, U = eigen(AAT)

    S = np.matrix(np.zeros(A.shape))
    for i in range(len(egv_list)):
        egv = egv_list[i]
        S[i, i] = np.sqrt(egv)

    for i in range(len(egv_list)):
        U[:, i] = np.dot(A, V[:, i])/S[i, i]

    Vt = np.transpose(V)

    return U, S, Vt


# Menghasilkan (eigenvalues, eigenvectors)
# dengan QR algorithm
def eigen(A: np.matrix) -> (np.array, np.matrix):
    accuracy_level = 3
    K = np.identity(A.shape[0])

    for i in range(accuracy_level):
        Q, R = np.linalg.qr(A)
        K = np.matmul(K, Q)
        A = np.matmul(R, Q)

    soln = [abs(A[i, i]) for i in range(len(A))]

    for i in range(len(soln)):
        if soln[i] < 0.00001:
            soln = soln[:i]
            break

    return soln, np.matrix(K)


''' -- Algoritma memiliki kompleksitas tinggi -- '''

'''
def eigenvalue_list(A: sym.Matrix) -> np.array:
    # egv = sym.Symbol('egv')    # Eigenvalue
    # row = A.rows
    # I = sym.eye(row)
    # Z = egv * I - A

    # char_eq = sym.det(Z)
    # soln = np.array(sym.solve(char_eq, egv))

    # for i in range(len(soln)):
    #     soln[i] = sym.re(sym.N(soln[i]))
    # soln = np.sort(soln)[::-1]

    # return soln

# Matriks singular
def singular_matrix(A: np.matrix, egv_list: np.array) -> np.matrix:
    epsilon = 0.000001
    basis_list = []
    
    for egv in egv_list:
        Z = eigenmatrix(A, egv)
        Z = rref(Z)
        print('-----')
        print(Z)
        Z = delete_zero_row(Z)
        row, col = Z.shape

        soln = []
        paramlist = [i for i in range(col)]  # list of index of parameters
        sublist = []    # list of substitution tuples

        # Setup variable list [x1, x2, x3, ...]
        for j in range(col):
            xn = sym.Symbol(f"x{j+1}")
            soln.append(xn)

        # soln = [-x2+x3, x2, x3, ...]
        # paramlist = [1,2]
        for i in range(row):
            foundOne = False
            for j in range(col):
                if not foundOne and abs(Z[i, j] - 1) < epsilon:
                    foundOne = True
                    indexOne = j
                    soln[indexOne] = 0
                    paramlist.remove(indexOne)
                elif foundOne and abs(Z[i,j]) > epsilon:
                    soln[indexOne] -= Z[i, j] * soln[j]

        # sublist = [(x2,0), (x3,0), ...]
        for idx in paramlist:
            xn = sym.Symbol(f"x{idx+1}")
            subtuple = (xn, 0)
            sublist.append(subtuple)

        # iteration
        # sublist : [(x2,1), (x3,0), ...] -> basis = ?
        #           [(x2,0), (x3,1), ...] -> basis = ?
        for i in range(len(sublist)):
            soln_instance = soln.copy()
            sublist_instance = sublist.copy()

            xn = sym.Symbol(f"x{paramlist[i]+1}")
            subtuple = (xn, 1)
            sublist_instance[i] = subtuple

            sum_of_square = 0
            for j in range(len(soln)):
                try:
                    soln_instance[j] = soln[j].subs(sublist_instance)
                except:
                    ...
                sum_of_square += soln_instance[j]**2

            magnitude = sym.sqrt(sum_of_square)
            for j in range(len(soln)):
                soln_instance[j] = sym.N(soln_instance[j] / magnitude)

            basis_list.append(soln_instance)

    if len(basis_list) != A.shape[0]:
        number_of_pads = A.shape[0] - len(basis_list)
        for i in range(number_of_pads):
            basis_list = np.r_[basis_list, np.zeros((1, A.shape[0]))]

    return np.matrix(np.transpose(basis_list))


def eigenmatrix(A: np.matrix, egv: float) -> np.matrix:
    row, col = A.shape
    I = np.identity(row)
    Z = egv * I - A
    return Z


# Menghasilkan array of eigenvalue > 0 turut mengecil
def eigenvalue_list(A: np.matrix) -> np.array:
    # QR Algorithm
    accuracy_level = 50
    for i in range(accuracy_level):
        Q, R = np.linalg.qr(A)
        A = np.matmul(R, Q)

    soln = [A[i,i] for i in range(len(A))]

    for i in range(len(soln)):
        if soln[i] < 0.001:
            break

    return soln[:i]


# Tidak menggunakan sympy.rref() dengan tujuan
# modifikasi ketelitian saat melakukan OBE
def rref(A: np.matrix) -> np.matrix:
    return row_echelon_top(row_echelon_bottom(A))


# Membentuk matriks eselon baris
def row_echelon_bottom(A: np.matrix) -> np.matrix:
    epsilon = 0.001
    A = np.array(A, 'float')
    row, col = A.shape

    # Basis: matriks kosong adalah eselon
    if row == 0 or col == 0:
        return np.matrix(A)

    # Rekursi: matriks berisi memiliki "head" dan "tail",
    #          tail akan dimodifikasi sesuai head
    else:
        allZero, nonZeroIdx = True, 0      # Seluruh kolom pertama 0
        for i in range(row):
            if abs(A[i,0]) >= epsilon:
                allZero = False
                nonZeroIdx = i
                break

        if allZero:
            B = row_echelon_bottom(A[:, 1:])
            return np.matrix(np.hstack([A[:, :1], B]))

        else:
            # Menukar baris yang depannya bukan nol ke atas
            if nonZeroIdx != 0:
                temp = A[nonZeroIdx].copy()
                A[nonZeroIdx] = A[0]
                A[0] = temp

            A[0] = A[0] / A[0,0]
            for i in range(1, row):
                first_head = A[i,0]
                for j in range(col):
                    A[i,j] -= A[0,j] * first_head
                    if abs(A[i,j]) < epsilon:
                        A[i,j] = 0

            # Contoh:
            #      1   2 3  A[:1]
            #      _ . _ _
            #      0 | 3 8
            #      0 | 7 2
            # A[1:,:1]  B
            B = row_echelon_bottom(A[1:,1:])
            return np.matrix(np.vstack([A[:1], np.hstack([A[1:,:1], B])]))


# Menghasilkan matriks eselon baris tereduksi dari
# matriks eselon baris
def row_echelon_top(A: np.matrix) -> np.matrix:
    epsilon = 0.001
    A = np.array(A, 'float')
    row, col = A.shape

    # Basis: matriks kosong adalah eselon
    if row == 0 or col == 0:
        return np.matrix(A)

    # Rekursi: matriks berisi memiliki "head" dan "tail",
    #          tail akan dimodifikasi sesuai head
    else:
        allZero = True     # Seluruh baris terakhir 0
        for j in range(col-1, -1, -1):
            if abs(A[-1, j]) >= epsilon:
                allZero = False
                break

        if allZero:
            B = row_echelon_top(A[:-1, :])
            return np.matrix(np.vstack([B, A[-1:]]))

        else:
            oneColIdx = -1
            for j in range(col):
                if abs(A[-1,j] - 1) < epsilon:
                    oneColIdx = j
                    break

            for i in range(row-1):
                first_head = A[i,oneColIdx]
                for j in range(oneColIdx, col):
                    A[i,j] -= A[-1,j] * first_head
                    if abs(A[i,j]) < epsilon:
                        A[i,j] = 0

            # Contoh:
            #     B
            #    1 2 0 2
            #    0 1 0 1
            #    _ _ _ _
            #    0 0 1 3  A[-1:]
            B = np.array(row_echelon_top(A[:-1,:]))
            return np.matrix(np.vstack([B, A[-1:]]))


# Prekondisi: Matrix A dalam bentuk rref
def delete_zero_row(A: np.matrix) -> np.matrix:
    deleting = True
    row, col = A.shape
    while A.shape[0] > 0 and deleting:
        deleting = all(A[-1,j] == 0 for j in range(col))
        if deleting:
            A = A[:-1]
            col -= 1

    return A

# Menghasilkan array of eigenvalue > 0 turut mengecil
def eigenvalue_list(A: np.matrix) -> np.array:
    # QR Algorithm
    accuracy_level = 50
    for i in range(accuracy_level):
        Q, R = np.linalg.qr(A)
        A = np.matmul(R, Q)

    soln = [A[i,i] for i in range(len(A))]

    for i in range(len(soln)):
        if soln[i] < 0.001:
            break

    return soln[:i]

'''
