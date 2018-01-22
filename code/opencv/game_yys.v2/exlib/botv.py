import ConfigParser
import re
import cv2 as cv
import numpy as np
import random
import glob
import os
from time import sleep
import time
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

def Getpoint(w,h,pts):
    mx=0
    mxy=0
    try:
        p=pts[0]
        mx=int(p[0]+w*random.random())
        my=int(p[1]+h*random.random())
    except:
        print "Get Point Failed!"
    return (mx,my)


def delay(s=1):
    t=random.random()*s+0.8
    sleep(t)


def chkk(img,mouse):
    mouse.move(0,0)
    print "Checking: ",img
    f,w,h,pts = findimg(img)
    if f:
        p=Getpoint(w,h,pts)
        mouse.click(p[0],p[1],1,1)
        print "Found -->",img
        rx,ry=mouse.screen_size()
        rx=int(random.random()*rx)
        ry=int(random.random()*ry)
        mouse.move(rx,ry)
    return f,re.sub(".*\\\|.png","",img)

def chkk_loop(bimgarr,mouse,monitor={}):
    f = False
    while not f:
        for k in bimgarr:
            f,bname = chkk(k,mouse)
            if f:
                try:
                    monitor[bname]+=1
                except:
                    monitor[bname]=1
                break
            delay(3)

def bcall(bname,tmonitor,func,*argv):
    st=time.time()
    start_count=0
    try:
        start_count=tmonitor[bname]
    except:
        tmonitor[bname]=1

    func(*argv.__add__((tmonitor,)))
    try:
        if tmonitor[bname]>start_count:
            tmonitor[bname+"_time"]+=(time.time()-st)
            print "---->",bname," Cost Time: ",func.func_name,time.time()-st
            print "---->",bname," Total Time: ",func.func_name,tmonitor[bname+"_time"]
            print "---->",bname," Avg. Time: ",func.func_name,tmonitor[bname+"_time"]/tmonitor[bname]
    except:
        tmonitor[bname+"_time"]=time.time()-st
    
    
    
    