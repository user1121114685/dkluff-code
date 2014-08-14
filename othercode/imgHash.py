"""
Copyright 2011 Statsbiblioteket

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
hg clone https://bitbucket.org/esbenab/image-hash
"""

import sys
import numpy
import pywt

from numpy import mgrid, zeros, sum
from scipy.fftpack import dct
from scipy.misc.pilutil import imrotate  # radon
import Image

# lagacy code EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'
AVG_HASH_SIZE = 8
P_HASH_SIZE = AVG_HASH_SIZE * 4
RAD_VAR_HASH_SIZE = AVG_HASH_SIZE * 4
DWT_HASH_SIZE = AVG_HASH_SIZE * 2


def makeBitList(avg, values):
    """takes an average value and a list of values and returns a "greater than
    ?" bit list.

    Examples:
            makeBitList(125, [255, 255, 10, 10, 125]
            # => [1, 1, 0, 0, 1]
    """
    returnValue = []
    for i, pixValue in enumerate(values):
        if pixValue >= avg:
            returnValue.insert(i, 1)
        else:
            returnValue.insert(i, 0)
    return returnValue


def dwtHash(image, dCoef='cA'):
    """Using Discrete Wavelet Transform (dwt) create a hash of the image
    image - the image for which to compute the dwt hash.

    This method defaults to the approximation wavelet. Options are:
    'cA': Approximation
    'cH': Horizontal detail
    'cV': Vertical detail
    'cD': Diagonal detail

    Examples:

        dwtHash(myImg)
        # => [1, 0, 1, 0, .., 1]

        dwtHash(myImg, dCoef='cH')
        # => [1, 0, 1, 0, .., 0]
    """
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    image = image.resize((DWT_HASH_SIZE, DWT_HASH_SIZE),
            Image.ANTIALIAS).convert('L')
    image_array = numpy.array(image).astype(float)
    dwt_tuple = pywt.dwt2(image_array, 'haar')
    cA, (cH, cV, cD) = dwt_tuple
    if dCoef is 'cH':
        coef = cH
    elif dCoef is 'cV':
        coef = cV
    elif dCoef is 'cD':
        coef = cD
    else:
        coef = cA
    coef = coef.ravel()
    avg = reduce(lambda x, y: x + y, coef) / len(coef)
    return makeBitList(avg, coef)

def avgHash(image):
    """Given an image conpute the avarage hash
    image - the image for which to compute the avarage hash

    Examples:

        avgHash(myImg)
        # => [1, 0, 0, 1, 1, .., 0]
    """
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    image = image.resize((AVG_HASH_SIZE, AVG_HASH_SIZE),
            Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, image.getdata()) / (AVG_HASH_SIZE ** 2)
    return makeBitList(avg, image.getdata())


def dctHash(image):
    """Given an image compute the dctHash
    image - the image for which to compute the phash

    Examples:

        dctHash(myImage)
        # => [1, 0, 0, 1, 1, .., 0]
    """
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    image = image.resize((P_HASH_SIZE, P_HASH_SIZE),
            Image.ANTIALIAS).convert('L')
    array = numpy.array(image).astype(float)
    dct_value = dct(array)
    dct_avg = 0
    dct_values = []
    for matrixes in dct_value[:AVG_HASH_SIZE]:
        for value in matrixes[1:AVG_HASH_SIZE + 1]:
            dct_avg += value
            dct_values.append(value)
    dct_avg /= (AVG_HASH_SIZE ** 2)
    return makeBitList(dct_avg, dct_values)


def radVarHash(image):
    """Given an image compute the Radial Variance Hash
    image - the image for which to compute the radial variance hash

    Examples:

        radVarHash(image)
        # => [1, 0, 0, 1, 1, .., 0]
    """
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    image = image.resize((RAD_VAR_HASH_SIZE, RAD_VAR_HASH_SIZE),
            Image.ANTIALIAS).convert('L')
    image_array = numpy.array(image)
    radon_array = radon(image_array, range(RAD_VAR_HASH_SIZE+1))[0][1:]
    radon_avg = 0
    radon_avg = reduce(lambda x,y: x+y, radon_array) / len(radon_array)
    return makeBitList(radon_avg, radon_array)


def radon(arr, theta=None):
    """ "Borrowed" from scipy.misc.pilutils.py"""
    if theta is None:
        theta = mgrid[0:180]
    s = zeros((arr.shape[1], len(theta)), float)
    k = 0
    for th in theta:
        im = imrotate(arr, -th)
        s[:, k] = sum(im, axis=0)
        k += 1
    return s


def hamming_distance(b1, b2):
    """Takes two bit strings of equal length and returns the distance between
    them

    Examples:

        hamming_distance(10011, 00011)
        # => 1
    """
    assert len(b1) == len(b2)
    return sum(bit1 != bit2 for bit1, bit2 in zip(b1, b2))

hashFunctions = [avgHash, dwtHash, dctHash, radVarHash]
distanceFunctions = [hamming_distance]

if __name__ == '__main__':
    images = sys.argv[1:]
    avgValues = []
    pHashValues = []
    radVarValues = []
    dwtValues = []
    for im in images:
        avgValues.append(avgHash(im))
        pHashValues.append(dctHash(im))
        radVarValues.append(radVarHash(im))
        dwtValues.append(dwtHash(im))
        # print(radVarHash(im))
    print("avg\tpHash\trad\tdwt")
    for i in range(len(avgValues)):
        # print(avgValues[i])
        # print(avgValues[i + 1])
        print(str(hamming_distance(avgValues[0], avgValues[i])) + '\t' +\
                str(hamming_distance(pHashValues[0], pHashValues[i])) + '\t' +\
                str(hamming_distance(radVarValues[0], radVarValues[i])) +
                '\t' + str(hamming_distance(dwtValues[0], dwtValues[i])))
