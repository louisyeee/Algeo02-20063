import numpy as np


# Mendekomposisi matriks A menjadi tuple of (U,S,V^t)
# dengan A = U . S . V^t
def svd(A: np.matrix) -> (np.matrix, np.matrix, np.matrix):
    A = np.matrix(A,dtype='float')
    AT = np.transpose(A)
    AAT = np.matrix(np.matmul(A, AT))
    ATA = np.matrix(np.matmul(AT, A))

    egv_list_ATA, V = eigen(ATA)
    egv_list_AAT, U = eigen(AAT)

    if len(egv_list_ATA) < len(egv_list_AAT):
        egv_list = egv_list_ATA
    else:
        egv_list = egv_list_AAT

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
    accuracy_level = 5
    K = np.identity(A.shape[0])

    for i in range(accuracy_level):
        Q, R = np.linalg.qr(A)
        K = np.matmul(K, Q)
        A = np.matmul(R, Q)

    soln = np.array([abs(A[i, i]) for i in range(len(A))])

    return soln, np.matrix(K)
