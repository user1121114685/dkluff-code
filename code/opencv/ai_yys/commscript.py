import os
import random
import time

from pymouse import PyMouse

from botcfg import *
from botv import *


class Robot:

    def __init__(self,brachlist,commlist):
        self.bdict=readimgs(brachlist)
        self.commdict=readimgs(commlist)
        self.bwin="bwin2"
        self.wcount = 20
        self.wtimeout = 5
        self.bstart="btz"
        self.botdelay=5
        self.starttime=time.time()
        #self.st_all = dict(self.bdict.items()+self.commdict.items())
        self.m = PyMouse()

    def beforefunc(self):
        print "before-done!"
    
    def afterfunc(self):
        #put statics and others here
        print "after-done!"

    def mainbot(self,t):
        if t == 0:
            t = 1000

        while 1:
            if t <0:
                print "---->Quite script as MAX hit!"
                break

            print "\n!-----------Looping ",t," -----------!\n"
            delay(5)
            s,w,h,pts=gstatus(self.commdict)
            if s is None:
                continue

            if s.startswith("b"):
                bclick(self.m,w,h,pts)
            
            try:
                if s == self.bstart:
                    self.beforefunc()
                    t-=1
                    self.afterfunc()
            except Exception as e:
                print e
                t-=1
            
            delay(self.botdelay)
