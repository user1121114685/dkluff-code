# -*- coding: UTF-8 -*-
import glob
import os
import pdb
import random
import re
import time
from ctypes import windll
from time import sleep
import ConfigParser

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab as ig
from pykeyboard import PyKeyboard

#import win32clipboard
import win32gui as w32
from basev import *


__version__="3.0"
DefaultTH=0.8

_CFG_FILENAME="bot.conf"
def cleancfg(fname):
    content = open(fname).read()  
    #Window下用记事本打开配置文件并修改保存后，编码为UNICODE或UTF-8的文件的文件头  
    #会被相应的加上\xff\xfe（\xff\xfe）或\xef\xbb\xbf，然后再传递给ConfigParser解析的时候会出错  
    #，因此解析之前，先替换掉  
    content = re.sub(r"\xfe\xff","", content)  
    content = re.sub(r"\xff\xfe","", content)  
    content = re.sub(r"\xef\xbb\xbf","", content)  
    open(fname, 'w').write(content)

class GameScreen:
    def __init__(self):
        print "Reading config of Screen..."
        cleancfg(_CFG_FILENAME)
        config = ConfigParser.RawConfigParser()
        config.read([_CFG_FILENAME])

        self.BIGSCREEN=bool(int(config.get('screen','BIGSCREEN'))>=1)

        self.MainScreenX=int(config.get('screen','MainScreenX'))
        self.MainScreenY=int(config.get('screen','MainScreenY'))

        self.LScreenX=int(config.get('screen','LScreenX'))
        self.LScreenY=int(config.get('screen','LScreenY'))

        self.MouseScreenX=int(config.get('screen','MouseScreenX'))
        self.MouseScreenY=int(config.get('screen','MouseScreenY'))

        #self.onSLOWPC=bool(int(config.get('screen','onSLOWPC'))>=1)
        self.GAMENAME=u"阴阳师-网易游戏" 
        
        print "Screen Initial Done!!!!"
        print "BIGSCREEN:",self.BIGSCREEN
        #print "onSlowPC:",self.onSLOWPC
        print "GameName(Hardcode):",self.GAMENAME.encode("GB18030")     
        

    def GetGameWindow(self):
        hwnd=w32.FindWindow(None,self.GAMENAME)
        l,t,r,b = (0,0,0,0)
        l,t,r,b = w32.GetWindowRect(hwnd)
        w=r-l
        h=b-t
        return w,h,(l,t),(r,b)

    def cropImg(self,im):
        im=np.array(im)
        im=im[:self.MainScreenY,self.LScreenX:]

        r=self.MouseScreenX*1.0/im.shape[1]
        dim=(self.MouseScreenX,int(im.shape[0]*r))

        im=cv.resize(im, dim, interpolation = cv.INTER_AREA)

        return im

    def GrabGameImage(self):
        im=None    
        if self.BIGSCREEN == True:
            im = grabscreen()
            try:
                im = self.cropImg(im)
            except Exception as e:
                print e
                im = np.array(ig.grab())
        else:
            im = np.array(ig.grab())
        return im
    
    def slowpc(self,mouse=None):
        hwnd=w32.FindWindow(None,self.GAMENAME)
        l,t,r,b = w32.GetWindowRect(hwnd)
        w=r-l
        h=b-t

        mx = int(l+100*random.random()+w/2.0)
        my = int(t+50*random.random()+h/2.0)

        mouse.click(mx,my,1,1)
        print "---->Slow PC!!!"

#######################comm block######################
def showimgs(imgs=[]):
    for i in imgs:
        plt.imshow(i)
        plt.show()
            
def paint(w,h,pts,screen):
    img_rgb=screen.GrabGameImage()
    
    for pt in pts:
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    showimgs([img_rgb])

def readimgs(blist,imgsdir):
    imdict={}
    for b in blist:
        imdir=os.path.join(imgsdir,b+".png")
        print "Reading image:",imdir
        im=cv.imread(imdir,0)
        imdict[b]=im
    return imdict


def Getpoint(w,h,pts,shift=0):
    mx=0
    mxy=0
    try:
        p=pts[0]
        #mx=int(p[0]+shift*w+0.5+random.random())
        mx=int(p[0]+w*random.random())
        my=int(p[1]+h*random.random())
    except:
        print "Get Point Failed!"
    return (mx,my)


def delay(s=1,mini=0):
    t=random.random()*s+mini
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
#######################comm block -- End ######################

def chkk(k,imgdict,mouse,screen,threshold=DefaultTH):
    #mouse.move(0,0)
    print "*Checking: ",k
    img_rgb=screen.GrabGameImage()
    f,w,h,pts = findimg(imgdict[k],img_rgb,threshold)
    if f:
        bclick(mouse,w,h,pts)
        print "*Found ---->",k
    return f


def waitchkk(k,imgdict,mouse,screen,threshold=DefaultTH,maxcount=5,t=5):
    f=False
    while maxcount>0 and not f:
        if mouse is None:
            img_rgb=screen.GrabGameImage()
            f,w,h,pts = findimg(imgdict[k],img_rgb,threshold)
        else:
            f=chkk(k,imgdict,mouse,screen,threshold)
        maxcount-=1
        print "---->Wait",k,maxcount
        delay(t)
    return f

def flowchkk(blist,imgdict,mouse,screen,threshold=DefaultTH,maxcount=5,t=5):
    for im in blist:
        waitchkk(im,imgdict,mouse,screen,threshold,maxcount=5,t=5)

def uwaitchkk(k,imgdict,mouse,screen,threshold=DefaultTH,maxcount=0):
    f=False
    
    while not f:
        f=chkk(k,imgdict,mouse,screen,threshold)
        print "---->Wait until:",k,maxcount


def gstatus(imgdict,screen,threshold=DefaultTH,cc=True):
    """
    cc: centering,multiplayer should not do center check
    so that cc = not multiplayer
    """
    ss=[]
    f,w,h,pts = (False,0,0,[])
    ww,wh,wlt,wrb = (0,0,0,0)
    if cc:
        ww,wh,wlt,wrb =  screen.GetGameWindow()
    img_rgb = screen.GrabGameImage()
    #showimgs(img_rgb)
    img_gray = cv.cvtColor(img_rgb,cv.COLOR_BGR2GRAY)
    for k in imgdict:
        try:
            print "*Checking status: ",k
            f,w,h,pts = matchImgray(imgdict[k],img_gray,ww,wh,wlt,wrb,threshold,cc)
            if f:
                print "*Found status: ",k
                ss+=[(k,w,h,pts)]
                if cc:
                    break
        except Exception as e:
            print "---->Get Game stuatus Error:\n",e
            continue
    
    return ss