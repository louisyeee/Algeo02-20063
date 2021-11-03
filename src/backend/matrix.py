import numpy as np
import sympy as sym
from typing import Union


def eigenmatrix(A: Union[np.matrix, np.ndarray], egv: float) -> np.matrix:
    row, col = A.shape
    I = np.identity(row)
    Z = egv * I - A
    Z = np.matrix(Z)
    return Z


# Menghasilkan array of eigenvalue turut mengecil
def eigenvalue_list(A: Union[np.matrix, np.ndarray]) -> np.array:
    egv = sym.Symbol('egv')    # Eigenvalue
    row, col = A.shape
    I = np.identity(row)
    Z = egv*I - A
    Z = sym.Matrix(Z)
    char_eq = sym.det(Z)
    soln = np.array(sym.solve(char_eq, egv))
    soln = np.sort(soln)[::-1]
    return soln


def svd(A: np.matrix) -> (np.matrix, np.matrix, np.matrix):
    shape = A.shape
    AT = np.matrix(np.transpose(A))
    ATA = np.matrix(np.matmul(AT, A))
    AAT = np.matmul(A, AT)

    ''' Matriks V: Singular kanan '''
    basis_list = []
    egv_list = eigenvalue_list(ATA)

    for egv in egv_list:
        Z = eigenmatrix(ATA, egv)
        Z = sym.Matrix(Z)
        Z = Z.rref()[0]
        Z = delete_zero_row(Z)

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
                elif foundOne:
                    soln[indexOne] -= Z[i, j] * soln[j]
                    paramlist.append(j)

        # sublist = [(x2,0), (x3,0)]
        for idx in paramlist:
            xn = sym.Symbol(f"x{idx+1}")
            subtuple = (xn, 0)
            sublist.append(subtuple)

        # iteration
        # sublist : [(x2,1), (x3,0)] -> basis = ?
        #           [(x2,0), (x3,1)] -> basis = ?
        for i in range(len(sublist)):
            xn = sym.Symbol(f"x{paramlist[i]+1}")
            subtuple = (xn, 1)
            sublist[i] = subtuple

            for j in range(len(soln)):
                try:
                    soln[j] = soln[j].subs(sublist)
                except:
                    ...

            basis_list.append(soln)

    # NORMALISASI !

    V = np.matrix(basis_list)


    ''' Matriks U: Singular kiri '''
    basis_list = []
    egv_list = eigenvalue_list(AAT)

    for egv in egv_list:
        Z = eigenmatrix(AAT, egv)
        Z = sym.Matrix(Z)
        Z = Z.rref()[0]
        Z = delete_zero_row(Z)

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
                elif foundOne:
                    soln[indexOne] -= Z[i, j] * soln[j]
                    paramlist.append(j)

        # sublist = [(x2,0), (x3,0)]
        for idx in paramlist:
            xn = sym.Symbol(f"x{idx+1}")
            subtuple = (xn, 0)
            sublist.append(subtuple)

        # iteration
        # sublist : [(x2,1), (x3,0)] -> basis = ?
        #           [(x2,0), (x3,1)] -> basis = ?
        for i in range(len(sublist)):
            xn = sym.Symbol(f"x{paramlist[i]+1}")
            subtuple = (xn, 1)
            sublist[i] = subtuple

            for j in range(len(soln)):
                try:
                    soln[j] = soln[j].subs(sublist)
                except:
                    ...

            basis_list.append(soln)

    U = np.matrix(basis_list)

    ''' Matriks Sigma '''
    S = np.zeros(shape)
    for i in range(len(egv_list)):
        egv = egv_list[i]
        if egv > 0:
            S[i,i] = sym.sqrt(egv)
        else:
            break

    return (U, S, V)


# Matrix A dalam bentuk rref
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
