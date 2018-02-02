from botv import *

import time
import random
import os

from pymouse import PyMouse
from botcfg import *



def yhsolo(t,bdict={},bmstring="bwin2"):
    if len(bdict)==0:
        return
    m = PyMouse()
    #bdict = ["btz","bwin2","bfail1","bxz","bwin1"]
    #bimgarr = [os.path.join(BIMGDIR,b+".png") for b in bdict ]

    print "Start YuHun Solo...",t

    startsec=time.time()

    MAXT=1000
    if t>0: MAXT=t

    monitor={}
    monitor[bmstring]=0

    count=0
    while count<MAXT:
        count+=1 
        print "---->",bmstring,monitor[bmstring]
        chkk_loop(bdict,m,monitor)
        delay(1)
        print "---->Total time:",time.time()-startsec
        print "---->Total Run Count: ",count

def yhslow(t,bdict={},bmstring="bwin2"):
    lb=len(bdict)
    if lb==0:
        return
    m = PyMouse()

    maxstun = 3
    c=0
    while 1:
        for k in bdict:
            delay(3)
            if not chkk(k,bdict,m):
                c+=1
        if c>maxstun*lb:
            slowpc(m)
            c=0


def tssolo(t,bdict={},bmstring="bwin2"):
    m = PyMouse()

    btsstandby = bdict["btsstandby"]
    btscomm = bdict["btscomm"]

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



def jward(t,bdict={},bmstring="bwin2"):
    
    while 1:
        try:
            waitchkk("jjt",bdict,None,20)
            jward_proc(t,bdict,bmstring)
            delay(5)
        except Exception as e:
            print e
            #pass

def story(*args,**kwargs):
    yhsolo(*args,**kwargs)




def jward_proc(t,bdict,bmstring="bwin2"):

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


    
    jjk  =bdict["jjk"]
    bjjs =bdict["bjjs"]
    bjjf =bdict["bjjf"]
    bsx  =bdict["bsx"]
    bjg  =bdict["bjg"]
    bqd  =bdict["bqd"]
    jjt  =bdict["jjt"]

    f,w,h,pts = findimg(jjk,0.5)
    pcount = len(pts)
    

    def refresh(s=""):
        chkk("bsx",bdict,m)
        waitchkk("bqd",bdict,m)
        print "---->Refresh as:",s,jtype

    def checkwf():
        wincount=0
        failcount=0
        try:
            wf,ww,wh,wpts = findimg(bjjs)
            wincount =len(wpts)

            ff,fw,fh,fpts = findimg(bjjf,0.9)
            failcount =len(fpts)
        except:
            pass

        return wincount,failcount      

    if not f:
        refresh("no jjk found")
        return

    
    if pcount<=3 and jtype == "PL":
        refresh("pcount<=6")
        return

    wc,fc = checkwf()
    if (wc>=3 or fc>3) and jtype == "PL":
        refresh("wc>=3 or fc>3")
        return


    p=pts[random.randint(0,pcount-1)]
    print "---->Jward:pcount,wc,fc: ",pcount,wc,fc    
    mx,my = Getpoint(w,h,[p],0.5)
    m.click(mx,my,1,1)
    waitchkk("bjg",bdict,m)
    waitchkk("jjt",bdict)
    
    


    

        
        




        


