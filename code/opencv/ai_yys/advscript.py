from botv import *
from commscript import *

import time
import random
import os

from pymouse import PyMouse
from botcfg import *


###########################################################################
def preventstuck():
    m = PyMouse()

    blist=["bxz","bfail1"]

    bdict=readimgs(blist)

    while 1:
        for k in bdict:
            chkk(k,bdict,m)
            delay(15)
        
###########################################################################
def yhsolo(t):
    blist = ["btz","bwin2",]
    comlist= []
    r = Robot(blist,comlist)
    r.mainbot(t)
      
###########################################################################
def jwardb(t,pljj=False):
    jwarda(t,pljj)

def jwarda(t,pljj = True):
    blist =  ["bwin2"]
    comlist= ["jjt","jjk","bjjs","bjjf"]

    branchlist=["bsx"]
    brdict=readimgs(branchlist)

    class Jwd(Robot):
        def refresh(self):
            if pljj:
                chkk("bsx",brdict,self.m)
                waitchkk("bqd",self.st_all,self.m)
                print "---->Refresh as:"

        def checkwf(self):
            wincount=0
            failcount=0
            try:
                wf,ww,wh,wpts = findimg(self.st_all["bjjs"])
                wincount =len(wpts)

                ff,fw,fh,fpts = findimg(self.st_all["bjjf"],0.9)
                failcount =len(fpts)
            except:
                pass

            return wincount,failcount

        def beforefunc(self):
            wc,fc = self.checkwf()
            if wc>=3 or fc>5:
                self.refresh()
                print "---->wc,fc ",wc,fc
                return

            f,w,h,pts = findimg(self.st_all["jjk"],0.5)
            pcount = len(pts)

            if pcount<3:
                self.refresh()
                print "---->pcount",pcount
                return

            p=pts[random.randint(0,pcount-1)]
            print "---->Jward:pcount,wc,fc: ",pcount,wc,fc    
            mx,my = Getpoint(w,h,[p],0.5)
            self.m.click(mx,my,1,1)
            bflow=["bjg"]
            flowchkk(bflow,self.st_all,self.m,20,5)

        

    rb=Jwd(blist,comlist)
    rb.bstart="jjt"
    #pdb.set_trace()
    rb.mainbot(t)




        




