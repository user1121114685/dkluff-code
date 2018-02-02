from botv import *

import time
import random
import os

from pymouse import PyMouse
from botcfg import *



class init_script:
    bfuncs={}
    bdict={}
    commdict={}

    def __init__(self,blist,commlist,bfunc=chkk):
        bkeys={ k:bfunc for k in blist }
        ckeys={ k:None for k in commlist }
        self.bfuncs = dict(bkeys.items()+ckeys.items())

        self.bdict=readimgs(blist)
        self.commdict=readimgs(commlist)


###########################################################################
def preventstuck():
    m = PyMouse()

    blist=["bxz",]

    bdict=readimgs(blist)

    while 1:
        for k in bdict:
            chkk(k,bdict,m)
        
###########################################################################

def yhsolo(t,blist = ["btz","bwin2","bfail1"],comlist= ["ftb"]):
    if t == 0:
        t = 10000
    
    m = PyMouse()

    ist = init_script(blist,comlist)
    st_all = dict(ist.bdict.items()+ist.commdict.items())

    fighting = "ftb"
    win = "bwin2"
    #fightend = {k:ist.bdict[k] for k in ["bwin2","bfail1"]}


    unkowns=0
    unkownsTH=10
    while 1:

        print "------------------>Looping"
        delay(5)
        s=gstatus(st_all)

        #for slowpc
        if s is None:
            unkowns+=1
            if unkowns>unkownsTH:
                slowpc(m)
            continue

        unkowns=0

        if s == fighting:
            waitchkk(win,ist.bdict,m,20,5)
            t-=1
            if t <0:
                print "---->Quite script as MAX hit!"
                break

        gifstatus(s,ist.bdict,ist.bfuncs[s],m)


        




