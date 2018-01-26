from botv import *

import time
import random
import os

from pymouse import PyMouse
from botcfg import *



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
    #bimgarr = [os.path.join(BIMGDIR,b+".png") for b in blist ]

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
    jjt=os.path.join(BIMGDIR,"jjt.png")
    
    while 1:
        try:
            waitchkk(jjt,None,20)
            jward_proc(t,blist,bmstring)
            delay(5)
        except Exception as e:
            print e
            #pass

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

    blist = ["jjk","bjjs","bjjf","bsx","bjg","bqd","jjt"]
    blist = [os.path.join(BIMGDIR,i+".png") for i in blist ]

    #badgelist = [str(3-i)+"x" for i in range(3)]
    #badgelist = [os.path.join(BIMGDIR,i+".png") for i in badgelist ]
    
    
    jjk=blist[0]
    bjjs=blist[1]
    bjjf=blist[2]
    bsx =blist[3]
    bjg =blist[4]
    bqd =blist[5]
    jjt =blist[6]

    f,w,h,pts = findimg(jjk,0.5)
    pcount = len(pts)
    

    def refresh(s=""):
        chkk(bsx,m)
        waitchkk(bqd,m)
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

    
    if pcount<=6 and jtype == "PL":
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
    waitchkk(bjg,m)
    waitchkk(jjt)
    
    


    

        
        




        


