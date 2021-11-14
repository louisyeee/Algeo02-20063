import numpy
from PIL import Image
from matrix import *
import time


def openImage(originalImage):  # Fungsi untuk membuka file image dan menghasilkan matriks RGB
    # originalImage = Image.open(imagePath)  # membuka image
    image = numpy.array(originalImage)  # menghasilkan matriks image
    matrixRed = image[:, :, 0]
    matrixGreen = image[:, :, 1]
    matrixBlue = image[:, :, 2]

    return [matrixRed, matrixGreen, matrixBlue, originalImage]


def createColorMatrix(m1, m2, m3, limitSVD):
    m1 = m1[:, :limitSVD]
    m2 = m2[:limitSVD, :limitSVD]
    m3 = m3[:limitSVD, :]
    m2 = np.matmul(m1, m2)
    m3 = np.matmul(m2, m3)
    m3 = m3.astype('uint8')
    return m3


def compress(imagePath,ratio):

    matrixRed, matrixGreen, matrixBlue, originalImage = openImage(imagePath)

    # originalImage.show()
    # Menghasilkan nilai lebar dan tinggi dari Image
    oriWidth, oriHeight = originalImage.size

    # Menghasilkan ukuran asli dari Image
    oriImageSize = oriWidth * oriHeight * 3

    # Menerima rasio pengurangan ukuran yang diinginkan user
    # ratio = int(input("Masukkan ratio pengurangan: "))
    start = time.time()
    ratio = 100-ratio

    # Menentukan limit SVD
    limitSVD = round(oriImageSize * ratio / 100 / (1+oriWidth+oriHeight) / 3)*2

    # Menghasilkan matriks U, S, V hasil SVD
    URed, SRed, VRed = svd(matrixRed)
    UGreen, SGreen, VGreen = svd(matrixGreen)
    UBlue, SBlue, VBlue = svd(matrixBlue)

    # Menghasilkan matriks warna setelah SVD sesuai rasio
    finalRed = createColorMatrix(URed, SRed, VRed, limitSVD)
    finalGreen = createColorMatrix(UGreen, SGreen, VGreen, limitSVD)
    finalBlue = createColorMatrix(UBlue, SBlue, VBlue, limitSVD)

    # Menghasilkan gambar sesuai RGB
    imageRed = Image.fromarray(finalRed, mode=None)
    imageGreen = Image.fromarray(finalGreen, mode=None)
    imageBlue = Image.fromarray(finalBlue, mode=None)

    # Menghasilkan image setelah kompres
    finalImage = Image.merge("RGB", (imageRed, imageGreen, imageBlue))

    # Menghitung pixel difference ratio
    diffRatio = 100 - (oriWidth*limitSVD/2 + limitSVD/2 + limitSVD/2 *
                oriHeight)/(oriHeight*oriWidth) * 100

    end = time.time()
    runtime = end - start

    return finalImage, round(diffRatio,2), round(runtime,2)
