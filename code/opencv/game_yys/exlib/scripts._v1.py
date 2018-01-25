from botv2 import *

import time
import random
import os

from pymouse import PyMouse
from botcfg import *


BLIST = ["btz","bts","bwin1","bwin2","bxz","bfail1","bzb"]

BIMAGE_DICT = [os.path.join(BIMGDIR,b+".png") for b in BLIST ]





def slowpc(mx=0,my=0):
    m = PyMouse()
    while 1:
        x,y=Getpoint(20,20,[(mx,my)])
        m.click(x,y,1,2)
        delay(10)
        print "---->slowpc!"


def yhsolo(t,blist=[],bmstring="bwin2"):
    if len(blist)==0:
        return
    m = PyMouse()
    #blist = ["btz","bwin2","bfail1","bxz","bwin1"]
    bimgarr = [os.path.join(BIMGDIR,b+".png") for b in blist ]

    print "Start YuHun Solo...",t

    startsec=time.time()

    MAXT=1000
    if t>0: MAXT=t

    monitor={}
    monitor[bmstring]=0

    count=0
    while count<MAXT:
        count+=1
        print "-->Total Run Count# ",count
        print "--> #",bmstring,monitor[bmstring]
        looptime=time.time()
        bcall(bmstring,monitor,chkk_loop,bimgarr,m)
        delay(1)
        print "---->Total time:",time.time()-startsec




def tssolo(t,blist=[],bmstring="bwin2"):
    m = PyMouse()
    blist=[os.path.join(BIMGDIR,i+".png") for i in blist ]

    btsstandby = blist[0]
    btscomm = blist[1]

    dt=1
    dtmax=20
    dtcount=0
    while 1:
        delay(5)
        bflag,w,h,pts = findimg(btsstandby)
        if bflag:         
            x0=0
            y0=0
            try:
                x0,y0=pts[0]
                ib,iw,ih,ipts = findimg(btscomm)
                if dt>0 and not ib:
                    mx=int(x0-w*random.random())
                    my=int(y0-h*random.random())
                    m.click(mx,my,1,1)
                    print "-----> walking!"
                    dtcount+=1
                    if dtcount>dtmax:
                        dtcount=0
                        dt=-1*dt

                if dt<0 and not ib:
                    mx=int(x0-w*random.random()-1.5*w)
                    my=int(y0-h*random.random())
                    m.click(mx,my,1,1)
                    print "walking!<-----"
                    dtcount+=1
                    if dtcount>dtmax:
                        dtcount=0
                        dt=-1*dt
            except Exception as e:
                print e



def jward(t,blist=[],bmstring="bwin2"):
    while 1:
        try:
            jward_proc(t,blist,bmstring)
            delay(5)
        except Exception as e:
            #print e
            pass

def story(*args,**kwargs):
    yhsolo(*args,**kwargs)




def jward_proc(t,blist=[],bmstring="bwin2"):

    """
    jtype : PL, PUB
    """

    X=3
    Y=3
    jtypes = ["PL","PUB"]
    jtype = jtypes[t]

    if jtype == "PUB":
        X=2

    m = PyMouse()

    blist = ["jjk","bjjs","bjjf","bsx","bjg","bqd"]
    blist = [os.path.join(BIMGDIR,i+".png") for i in blist ]

    badgelist = [str(2-i)+"x" for i in range(3)]
    badgelist = [os.path.join(BIMGDIR,i+".png") for i in badgelist ]
    
    
    imjj=blist[0]
    bjjs=blist[1]
    bjjf=blist[2]
    bsx =blist[3]
    bjg =blist[4]
    bqd =blist[5]

    w,h,pts = find2grid(imjj,3,3)
    imgs = cropscreen(w,h,pts)

    imgsindex =[]
    for bg in badgelist:
        for i in range(len(imgs)):
            ib,iw,ih,ipts = findimg(bg,0.8,False,imgs[i])
            if ib:
                imgsindex.append(i)
                continue

    print "---->sorted by badge: ",imgsindex,len(imgs)

    winpt = []
    failpt = []
    for i in imgsindex:
        ib,iw,ih,ipts = findimg(bjjs,0.8,False,imgs[i])
        if ib:
            winpt.append(i)
            if len(winpt)>=3 and jtype == "PL":
                chkk(bsx,m)
                delay(2)
                chkk(bqd,m)
                winpt=[]
            continue

        ib,iw,ih,ipts = findimg(bjjf,0.8,False,imgs[i])
        if ib:
            failpt.append(i)
            if len(failpt)>=5 and jtype == "PL":
                chkk(bsx,m)
                delay(2)
                chkk(bqd,m)
                failpt=[]
            continue

        mx,my = Getpoint(w,h,[pts[i]])
        m.click(mx,my,1,1)
        delay(2)
        chkk(bjg,m)

        

    

        
        




        


