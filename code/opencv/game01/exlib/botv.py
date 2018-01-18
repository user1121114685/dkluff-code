import ConfigParser
import re
import cv2 as cv
import numpy as np
from PIL import ImageGrab as ig

__version__="1.0"

methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

def cleancfg(fname):
    content = open(fname).read() 
    content = re.sub(r"\xfe\xff","", content)  
    content = re.sub(r"\xff\xfe","", content)  
    content = re.sub(r"\xef\xbb\xbf","", content)  
    open(fname, 'w').write(content)


def loadcfg(cfgfile,sec,cfgnames):
    cleancfg(cfgfile)
    config = ConfigParser.RawConfigParser()
    config.read([cfgfile])
    
    result={}

    for c in cfgnames:
		result[c]=config.get(sec,c)

    return result


def findimg(timg,threshold=0.8):
    """
    timg: template image dir
    """
    img_rgb = ig.grab()
    img_rgb = np.array(img_rgb)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(timg,0)
    w, h = template.shape[::-1]

    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)	
    loc = np.where( res >= threshold)

    bflag = False
    pts=zip(*loc[::-1])
    if len(pts)>0: bflag=True
    return bflag,w,h,pts

def getpoint(w,h,pts):
    #todo: random point, error process
    p=pts[0]
    mx=int(p[0]+w/2)
    my=int(p[1]+h/2)    
    return (mx,my)