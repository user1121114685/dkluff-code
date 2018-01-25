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

class rgt:
    BIGSCREEN=True

    """
    Big Screen, only work with primary
    """
    
    MainScreenX=3840
    MainScreenY=2160
    
    LScreenX=1600
    LScreenY=900
    
    MouseScreenX=2560
    MouseScreenY=1440



def test01():
    im=grabscreen()
    im=procImg_cv(im)

    plt.imshow(im)
    plt.show()

def test02(imdir,threshold = 0.4):
    
    img_rgb=GrabGameImage()

    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(imdir,0)
    w, h = template.shape[::-1]


    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    #res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)

    

    res = cv.matchTemplate(img_gray,template,eval(methods[1]))	
    loc = np.where( res >= threshold)


    #pdb.set_trace()
    zpoints = zip(*loc[::-1])
    mx,my=zpoints[0]
    #print "org",mx,my

    #mx=int(msx*(mx-1600)/3840.0)
    #my=int(msy*my/2160.0)
    mx=int(mx)
    my=int(my)

    #print mx,my
    #m.click(mx,my,1)
    #cv.circle(img_rgb,(mx,my),w/4,(0,0,255), 2)
    

    #pdb.set_trace()
    for pt in zpoints:
    	cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    	#cv.circle(img_rgb,(pt[0]+w/2,pt[1]+h/2),w/4,(0,0,255),-1)
    #cv.imwrite(methods[1]+'.png',img_rgb)
    plt.imshow(img_rgb)
    plt.show()





if __name__ == "__main__":
    #test02("..\\4k\\btz.png",0.6)
    test01()