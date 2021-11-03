import numpy as np
import sympy as sym
from typing import Union


def eigenmatrix(A: sym.Matrix, egv: sym.Float) -> sym.Matrix:
    row = A.rows
    I = sym.eye(row)
    Z = egv * I - A
    return Z


# Menghasilkan array of eigenvalue turut mengecil
def eigenvalue_list(A: sym.Matrix) -> np.array:
    egv = sym.Symbol('egv')    # Eigenvalue
    row = A.rows
    I = sym.eye(row)
    Z = egv * I - A
    char_eq = sym.det(Z)
    soln = np.array(sym.solve(char_eq, egv))
    soln = np.sort(soln)[::-1]
    return soln


# Mendekomposisi matriks A menjadi tuple of (U,S,V)
def svd(A: np.matrix) -> (np.matrix, np.matrix, np.matrix):
    A = sym.Matrix(A)

    V = np.matrix(singular_matrix(A.T * A))
    U = np.matrix(singular_matrix(A * A.T))

    ''' Matriks Sigma '''
    S = np.matrix(np.zeros(A.shape))
    egv_list = eigenvalue_list(A.T * A)
    for i in range(len(egv_list)):
        egv = egv_list[i]
        if egv > 0:
            S[i,i] = sym.N(sym.sqrt(egv))
        else:
            break

    return U, S, V


# Matriks singular
def singular_matrix(A: sym.Matrix) -> sym.Matrix:
    basis_list = []
    egv_list = eigenvalue_list(A)

    for egv in egv_list:
        print()
        Z = eigenmatrix(A, egv)
        Z = Z.rref()[0]
        Z = delete_zero_row(Z)
        print(Z)

        soln = []
        paramlist = []  # list of index of parameters
        sublist = []    # list of substitution tuples

        # Setup variable list [x1, x2, x3, ...]
        for j in range(Z.cols):
            xn = sym.Symbol(f"x{j+1}")
            soln.append(xn)

        # soln = [-x2+x3, x2, x3, ...]
        # paramlist = [1,2]
        for i in range(Z.rows):
            foundOne = False
            for j in range(Z.cols):
                if not foundOne and Z[i, j] == 1:
                    foundOne = True
                    indexOne = j
                    soln[indexOne] = 0
                elif foundOne and Z[i,j] != 0:
                    soln[indexOne] -= Z[i, j] * soln[j]
                    if j not in paramlist:
                        paramlist.append(j)

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

    return sym.Matrix(basis_list).T


# Prekondisi: Matrix A dalam bentuk rref
def delete_zero_row(A: sym.Matrix) -> sym.Matrix:
    i = A.rows - 1
    deleting = True
    while i >= 0 and deleting:
        for x in A.row(i):
            if x != 0:
                deleting = False
        if deleting:
            A.row_del(i)
            i -= 1
    return A
