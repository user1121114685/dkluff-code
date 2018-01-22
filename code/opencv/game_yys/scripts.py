from exlib.botv import *

import time
import random
import os

from pymouse import PyMouse


BIMGDIR = '1080p'

BLIST = ["btz","bts","bwin1","bwin2","bxz","bfail1","bzb"]

BIMAGE_DICT = [os.path.join(BIMGDIR,b+".png") for b in BLIST ]





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



        


