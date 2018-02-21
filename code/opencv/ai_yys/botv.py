# -*- coding: UTF-8 -*-
import glob
import os
import pdb
import random
import re
import time
from ctypes import windll
from time import sleep

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab as ig
from pykeyboard import PyKeyboard

#import win32clipboard
import win32gui as w32
from basev import *
from botcfg import *

__version__="3.0"

class init_script:
    
    bdict={}
    commdict={}

    def __init__(self,blist,commlist):
        self.bdict=readimgs(blist)
        self.commdict=readimgs(commlist)



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

def bclick(mouse,w,h,pts):
    #paint(w,h,pts)
    p=Getpoint(w,h,pts)
    mouse.click(p[0],p[1],1,1)
    print "*click: ",p
    #move mouse random
    rx,ry=mouse.screen_size()
    rx=int(random.random()*rx)
    ry=int(random.random()*ry)
    mouse.move(rx,ry)

def chkk(k,imgdict,mouse):
    #mouse.move(0,0)
    print "*Checking: ",k
    f,w,h,pts = findimg(imgdict[k],DefaultTH)
    if f:
        bclick(mouse,w,h,pts)
        print "*Found ---->",k
    return f

def _chkk_loop(bimgdic,mouse,monitor={}):
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
    return f


def waitchkk(k,imgdict,mouse=None,maxcount=5,t=5):
    f=False      
    while maxcount>0 and not f:
        if mouse is None:
            f,w,h,pts=findimg(imgdict[k])
        else:
            f=chkk(k,imgdict,mouse)
        maxcount-=1
        print "---->Wait",k,maxcount
        delay(t)
    return f

def flowchkk(blist,imgdict,mouse,maxcount=5,t=5):
    for im in blist:
        waitchkk(im,imgdict,mouse=None,maxcount=5,t=5)

def uwaitchkk(k,imgdict,mouse,maxcount=0):
    f=False
    
    while not f:
        f=chkk(k,imgdict,mouse)
        print "---->Wait until:",k,maxcount


def showimgs(imgs=[]):
    for i in imgs:
        plt.imshow(i)
        plt.show()
            
def paint(w,h,pts):
    img_rgb=GrabGameImage()
    
    for pt in pts:
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    showimgs([img_rgb])


def slowpc(mouse=None):
    hwnd=w32.FindWindow(None,GAMENAME)
    l,t,r,b = w32.GetWindowRect(hwnd)
    w=r-l
    h=b-t

    mx = int(l+w*random.random()+w/3.0)
    my = int(t+h*random.random()+h/3.0)

    mouse.click(mx,my,1,1)
    print "---->Slow PC!!!"

def readimgs(blist=[]):
    imdict={}
    for b in blist:
        imdir=os.path.join(BIMGDIR,b+".png")
        im=cv.imread(imdir,0)
        imdict[b]=im
    return imdict

def gstatus(imgdict):
    s=None
    f,w,h,pts = (False,0,0,[])
    img_rgb = GrabGameImage()
    img_gray = cv.cvtColor(img_rgb,cv.COLOR_BGR2GRAY)
    for k in imgdict:
        try:
            print "*Checking status: ",k
            f,w,h,pts = matchImgray(imgdict[k],img_gray)
            if f:
                s=k
                print "*Found status: ",s
                break
        except Exception as e:
            print "---->Get Game stuatus Error:\n",e
            continue
    return s,w,h,pts
