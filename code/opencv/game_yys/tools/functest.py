import sys
import os
import cv2 as cv
import numpy as np


from matplotlib import pyplot as plt
from pykeyboard import PyKeyboard
from pymouse import PyMouse
m = PyMouse()



#libdir=os.path.join("..")
sys.path.append("..")

from botv2 import *

def test(img,th):
    f,w,h,pts = findimg(img,th)
    if f:
        print pts
        paint(w,h,pts)

if __name__ == "__main__":
    test(sys.argv[1],float(sys.argv[2]))