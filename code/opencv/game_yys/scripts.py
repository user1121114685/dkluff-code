from exlib.botv import *

import time
import random
import os

from pymouse import PyMouse


BIMGDIR = '1080p'

BLIST = ["btz","bts","bwin1","bwin2","bxz","bfail1","bzb"]

BIMAGE_DICT = [os.path.join(BIMGDIR,b+".png") for b in BLIST ]


def yhsolo(t):
    m = PyMouse()
    blist = ["btz","bwin1","bwin2","bxz","bfail1"]
    bimgarr = [os.path.join(BIMGDIR,b+".png") for b in blist ]

    print "Start YuHun Solo...",t

    startsec=time.time()

    MAXT=1000
    if t>0: MAXT=t

    monitor={}
    monitor["btz"]=0

    count=0
    while count<MAXT:
        count+=1
        print "-->Total Run Count# ",count
        print "--> #","btz",monitor["btz"]
        looptime=time.time()
        bcall("btz",monitor,chkk_loop,bimgarr,m)
        delay(3)
        print "---->Total time:",time.time()-startsec

def yhpt(t):
    m = PyMouse()
    blist = ["bwin1","bwin2","bxz","bfail1"]
    bimgarr = [os.path.join(BIMGDIR,b+".png") for b in blist ]

    print "Start YuHun Solo...",t

    MAXT=1000
    if t>0: MAXT=t

    startsec=time.time()

    count=0
    while count<MAXT:
        count+=1
        print "-->GO #",count
        looptime=time.time()
        chkk_loop(bimgarr,m)
        delay(3)
        print "---->Time:",time.time()-looptime
        print "---->Total time:",time.time()-startsec



        


