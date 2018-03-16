import os
import random
import time

from pymouse import PyMouse

from botv import *
CFG_FILENAME="bot.conf"

class Robot:

    def __init__(self,brachlist,commlist,stucklist):
        print "Reading Config of botsetting..."
        cleancfg(CFG_FILENAME)
        config = ConfigParser.RawConfigParser()
        config.read([CFG_FILENAME])
        self.BIMGDIR=config.get('botsetting','BIMGDIR')
        self.DefaultTH=config.get('botsetting','DefaultTH')

        self.bdict=readimgs(brachlist,self.BIMGDIR)
        self.commdict=readimgs(commlist,self.BIMGDIR)
        self.bstuckdict=readimgs(stucklist,self.BIMGDIR)

        self.bwin="bwin2"
        self.wcount = 20
        self.wtimeout = 5
        self.bstart="btz"
        self.botdelay=5
        self.starttime=time.time()
        #self.st_all = dict(self.bdict.items()+self.commdict.items())
        self.m = PyMouse()
        self.screen = GameScreen()
        print "Bot initial done!!!"
        

    def beforefunc(self):
        print "before-done!"
    
    def afterfunc(self):
        #put statics and others here
        print "after-done!"

    def mainbot(self,t):
        if t == 0:
            t = 1000

        onSLOWPC=self.screen.onSLOWPC

        while 1:
            if t <0:
                print "---->Quite script as MAX hit!"
                break

            print "\n*********** Looping Count Down: ",t," ***********\n"
            delay(5)
            s,w,h,pts=gstatus(self.commdict,self.screen)
            if s is None:
                print "---->No status Found!"
                print "---->Checking stuck!"
                s,w,h,pts=gstatus(self.bstuckdict,self.screen)
                if s is None:
                    print "---->No status Found! Loop Continue!---->"
                    if onSLOWPC and random.random()>0.5:
                        self.screen.slowpc(self.m)
                        delay(self.botdelay)
                    continue

            if s.startswith("b"):
                bclick(self.m,w,h,pts)
            
            try:
                if s == self.bstart:
                    self.beforefunc()
                    print "before-done!"
                    t-=1
                    self.afterfunc()
                    print "after-done!"
            except Exception as e:
                print e
                t-=1
            
            delay(self.botdelay)
