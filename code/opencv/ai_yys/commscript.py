import os
import random
import time

from pymouse import PyMouse

from botcfg import *
from botv import *


class Robot:

    def __init__(self,blist,commlist):
        self.bdict=readimgs(blist)
        self.commdict=readimgs(commlist)
        self.bwin="bwin2"
        self.wcount = 20
        self.wtimeout = 5
        self.bstart="btz"
        #self.st_all = dict(self.bdict.items()+self.commdict.items())
        self.m = PyMouse()

    def beforefunc(self):
        f=waitchkk(self.bwin,self.commdict,self.m,15,5)
        if not f and onSLOWPC:
            slowpc()
        print "before-done!"
    
    def afterfunc(self):
        #put statics and others here
        print "after-done!"

    def mainbot(self,t):
        if t == 0:
            t = 1000

        unkowns=0
        unkownsTH=10
        while 1:
            if t <0:
                print "---->Quite script as MAX hit!"
                break

            print "\n!-----------Looping ",t," -----------!\n"
            delay(5)
            s,w,h,pts=gstatus(self.commdict)

            #for slowpc and exceptions
            if s is None:
                unkowns+=1
                if unkowns>unkownsTH:
                    slowpc(self.m)
                continue
            else:
                unkowns=0

            if s.startswith("b"):
                bclick(self.m,w,h,pts)

            if s == self.bstart:
                self.beforefunc()
                t-=1
            self.afterfunc()
