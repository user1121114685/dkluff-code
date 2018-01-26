import re
import cv2 as cv
import numpy as np
import random
import glob
import os
from time import sleep
import time
import pdb
from PIL import ImageGrab as ig
from matplotlib import pyplot as plt
from pykeyboard import PyKeyboard
from ctypes import windll
from botcfg import *
#import win32clipboard

__version__="2.0"

methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

def readimgs(blist=[]):
    imdict={}
    for b in blist:
        imdir=os.path.join(BIMGDIR,b+".png")
        im=cv.imread(imdir,0)
        imdict[b]=im
    return imdict


def grabscreen(i=0):
    if i>10: return None
    img_rgb=ig.grabclipboard()
    if not img_rgb is None:
        """
        Must run as admin
        """
        windll.user32.OpenClipboard()
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()
        #print "---->Clipboard Cleaned!"

    kb=PyKeyboard()
    kb.press_key(kb.print_screen_key)
    sleep(1)
    img_rgb=ig.grabclipboard()
    if img_rgb == None:
        print "---->grab error!",i
        i+=1
        grabscreen(i)
    return img_rgb

def procImg_cv(im):
    im=np.array(im)
    im=im[:MainScreenY,LScreenX:]

    r=MouseScreenX*1.0/im.shape[1]
    dim=(MouseScreenX,int(im.shape[0]*r))

    im=cv.resize(im, dim, interpolation = cv.INTER_AREA)

    return im

def GrabGameImage():
    im=None    
    if BIGSCREEN == True:
        im = grabscreen()
        try:
            im = procImg_cv(im)
        except Exception as e:
            print e
            im = np.array(ig.grab())
        
    else:
        im = np.array(ig.grab())
    
    return im


def calCenter(w,h,pts):
    if len(pts)<0: return []

    centers=[pts[0]]
    r=min(w,h)**2/4

    upts=[]
    #pdb.set_trace()
    for x,y in pts:
        ix=x+w/2
        iy=y+h/2
        dis=[(cx-ix)**2+(cy-iy)**2 for cx,cy in centers ]
        
        if len(dis)>0:
            dis.sort()
            if dis[0]>r:
                centers.append((ix,iy))
                upts.append((x,y))

    return upts




def findimg(template,threshold=DefaultTH,rflag=False,img_rgb=None):
    """
    timg: template image dir
    """
    if type(img_rgb) == type(None):
        img_rgb=GrabGameImage()

    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    #template = cv.imread(timg,0)
    w, h = template.shape[::-1]

    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)	
    loc = np.where( res >= threshold)

    bflag = False
    pts=zip(*loc[::-1])


    if len(pts)>0:
        bflag=True
        pts=calCenter(w,h,pts)

    if rflag: return bflag,w,h,pts,img_rgb
    return bflag,w,h,pts

def Getpoint(w,h,pts,shift=0):
    mx=0
    mxy=0
    try:
        p=pts[0]
        mx=int(p[0]+shift*w+0.5+random.random())
        my=int(p[1]+h*random.random())
    except:
        print "Get Point Failed!"
    return (mx,my)


def delay(s=1):
    t=random.random()*s+0.8
    sleep(t)


def chkk(k,imgdict,mouse):
    #mouse.move(0,0)
    print "*Checking: ",k
    f,w,h,pts = findimg(imgdict[k],DefaultTH)
    if f:
        #paint(w,h,pts)
        p=Getpoint(w,h,pts)
        mouse.click(p[0],p[1],1,1)
        print "*Found -->",k

        #move mouse random
        rx,ry=mouse.screen_size()
        rx=int(random.random()*rx)
        ry=int(random.random()*ry)
        mouse.move(rx,ry)
    return f

def chkk_loop(bimgdic,mouse,monitor={}):
    f = False
    while not f:
        for k in bimgdic:
            f = chkk(k,bimgdic,mouse)
            if f:
                try:
                    monitor[k]+=1
                except:
                    monitor[k]=1
                break
            delay(3)

def waitchkk(k,imgdict,mouse=None,maxcount=5):
    f=False
    if mouse is None:
        while maxcount>0 and not f:
            f,w,h,pts = findimg(imgdict[k])
            print "---->Wait",k,maxcount
            maxcount-=1
            return
    while maxcount>0 and not f:
        f=chkk(k,imgdict,mouse)
        maxcount-=1
        print "---->Wait",k,maxcount
    

def showimgs(imgs=[]):
    for i in imgs:
        plt.imshow(i)
        plt.show()
            
def paint(w,h,pts):
    img_rgb=GrabGameImage()
    
    for pt in pts:
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    showimgs([img_rgb])



