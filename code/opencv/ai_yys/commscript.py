import os
import random
import time

from pymouse import PyMouse

from botv import *
CFG_FILENAME="bot.conf"
_version="""
Vsersion=1.0
Update=2018.3.22
"""
class Robot:

    def __init__(self,brachlist,commlist,stucklist):
        print "Init Bot..."
        print _version
        print "Reading Config of botsetting..."
        
        cleancfg(CFG_FILENAME)
        config = ConfigParser.RawConfigParser()
        config.read([CFG_FILENAME])
        self.BIMGDIR=config.get('botsetting','BIMGDIR')
        self.DefaultTH=float(config.get('botsetting','DefaultTH'))

        self.bdict=readimgs(brachlist,self.BIMGDIR)
        self.commdict=readimgs(commlist,self.BIMGDIR)
        self.bstuckdict=readimgs(stucklist,self.BIMGDIR)

        self.bwin="bwin2"
        self.wcount = 20
        self.wtimeout = 5
        self.bstart="btz"
        self.botdelay=1
        self.starttime=time.time()
        #self.st_all = dict(self.bdict.items()+self.commdict.items())
        self.m = PyMouse()
        self.screen = GameScreen()

        self.cc = True #multiplayer should not do center check
                    
        print "Bot initial done!!!"
        

    def beforefunc(self):
        print "before-done!"
    
    def afterfunc(self):
        #put statics and others here
        print "after-done!"

    def mainbot(self,t):
        if t == 0:
            t = 1000
        #onSLOWPC=self.screen.onSLOWPC
        
        while 1:
            if t <0:
                print "---->Quite script as MAX hit!"
                break

            print "\n*********** Looping Count Down: ",t," ***********\n"
            delay(self.botdelay)
            ss=gstatus(self.commdict,self.screen,threshold=self.DefaultTH,cc=self.cc)
            
            if len(ss)==0:
                print "---->No status Found!"
                print "---->Checking stuck!"
                ss=gstatus(self.bstuckdict,self.screen,threshold=self.DefaultTH,cc=self.cc)
                if len(ss)==0:
                    print "---->No status Found! Loop Continue!---->"
                    #if onSLOWPC and random.random()>0.5:
                    #   self.screen.slowpc(self.m)
                    #   delay(self.botdelay)
                    continue

            for s,w,h,pts in ss:
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

