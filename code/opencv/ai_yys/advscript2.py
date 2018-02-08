from botv import *
from basev import findimg
import time
import random
import os

from pymouse import PyMouse
from botcfg import *



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


def jwarda(t):
    blist =  ["bsx","bjg","bqd","bwin2","bfail1"]
    comlist= ["jjt","jjk","bjjs","bjjf"]   
    jward_proc(t,blist,comlist,wcount=20,wsecends=5,pljj=True)

def jwardb(t):
    blist =  ["bsx","bjg","bqd","bwin2","bfail1"]
    comlist= ["jjt","jjk","bjjs","bjjf"]   
    jward_proc(t,blist,comlist,wcount=20,wsecends=5)

def jward_proc(t,blist,comlist,wcount=20,wsecends=5,pljj=False):

    if t == 0:
        t = 1000
    
    m = PyMouse()

    ist = init_script(blist,comlist)
    st_all = dict(ist.bdict.items()+ist.commdict.items())
    
    bstart = "jjt"
    #fighting = "ftb"
    win = "bwin2"
    fail = "bfail1"

    def refresh():
        if pljj:
            chkk("bsx",st_all,m)
            waitchkk("bqd",st_all,m)
            print "---->Refresh as:"

    def checkwf():
        wincount=0
        failcount=0
        try:
            wf,ww,wh,wpts = findimg(st_all["bjjs"])
            wincount =len(wpts)

            ff,fw,fh,fpts = findimg(st_all["bjjf"],0.9)
            failcount =len(fpts)
        except:
            pass

        return wincount,failcount      


    unkowns=0
    unkownsTH=10
    while 1:
        if t <0:
            print "---->Quite script as MAX hit!"
            break
        print "!-----------Looping ",t," -----------!"
        delay(5)
        s,w,h,pts=gstatus(st_all)

        #for slowpc and exceptions
        if s is None:
            unkowns+=1
            if unkowns>unkownsTH:
                slowpc(m)
            continue

        unkowns=0
        if s in ist.bdict:
            bclick(m,w,h,pts)

        if s == bstart:
            #################
            wc,fc = checkwf()

            if wc>=3 or fc>5:
                refresh()
                print "---->wc,fc ",wc,fc
                continue
            
            f,w,h,pts = findimg(st_all["jjk"],0.5)
            pcount = len(pts)

            if pcount<3:
                refresh()
                print "---->pcount",pcount
                continue

            p=pts[random.randint(0,pcount-1)]
            print "---->Jward:pcount,wc,fc: ",pcount,wc,fc    
            mx,my = Getpoint(w,h,[p],0.5)
            m.click(mx,my,1,1)
            bflow = ["bjg","bwin2"]
            flowchkk(bflow,st_all,m,wcount,wsecends)
            #################
            t-=1





    
    
    


    

        
        




        


