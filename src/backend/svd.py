import numpy
from PIL import Image


def openImage(imagePath):  # Fungsi untuk membuka file image dan menghasilkan matriks RGB
    originalImage = Image.open(imagePath)  # membuka image
    image = numpy.array(originalImage)  # menghasilkan matriks image
    matrixRed = image[:, :, 0]
    matrixGreen = image[:, :, 1]
    matrixBlue = image[:, :, 2]

    return [matrixRed, matrixGreen, matrixBlue, originalImage]


imagePath = input("Masukkan nama file: ")
matrixRed, matrixGreen, matrixBlue, originalImage = openImage()

# Menghasilkan nilai lebar dan tinggi dari Image
oriWidth, oriHeight = originalImage.size

# Menghasilkan ukuran asli dari Image
oriImageSize = oriWidth * oriHeight * 3
