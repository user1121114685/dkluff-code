# -*- coding: UTF-8 -*-
from basev import *
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
import win32gui as w32

__version__="3.0"


methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']



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

def GetGameWindow(gn=GAMENAME):
    hwnd=w32.FindWindow(None,gn)
    l,t,r,b = (0,0,0,0)
    l,t,r,b = w32.GetWindowRect(hwnd)
    w=r-l
    h=b-t

    return w,h,(l,t),(r,b)