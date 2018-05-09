# -*- coding: UTF-8 -*-
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

#import win32clipboard
import win32gui as w32


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

def verifypts(pts,w,h,lt,rb):
    l,t = lt
    r,b = rb
    goodpts = []
    for x,y in pts:
        if (x>l and x<r) and (y>t and y<b):
            goodpts.append((x,y))
    return goodpts

def matchImgray(template,img_gray,
                ww,wh,wlt,wrb,
                threshold=0.8,cc=True):
    bflag,w,h,pts = False,0,0,[]
    if img_gray is None:
        return bflag,w,h,pts
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)	
    loc = np.where( res >= threshold)

    bflag = False
    pts=zip(*loc[::-1])

    if len(pts)>0:
        if cc:
            print "__ matchImgray : centering-----"
            pts=calCenter(w,h,pts)
            pts=verifypts(pts,ww,wh,wlt,wrb)
        if len(pts)>0:
            bflag = True
    return bflag,w,h,pts

def dyMatchIm(template,img_gray,
              ww,wh,wlt,wrb,
              threshold=0.8,cc=True,
              maxth=0.9,minth=0.5,step=0.1,):
    bflag,w,h,pts = False,0,0,[]
    while maxth>=minth:
        bflag,w,h,pts = matchImgray(template,ww,wh,wlt,wrb,img_gray,maxth,cc)
        if bflag:
            break
        maxth-=step
    return bflag,w,h,pts


def findimg(template,img_rgb,threshold=0.8,rflag=False):
    
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

