from exlib.botv import *
from pymouse import PyMouse
from time import sleep
import random

def delay(s=1):
    t=random.random()*s+0.8
    sleep(t)


def faildeamon(t):
    m = PyMouse()
    bwin1="bwin1.png"
    bfail1="bfail1.png"
    bwin2 = 'bwin2.png'

    ftxt=["Win--!","Fail--!"]

    while 1:
        ft=-1
        f,w,h,pts = findimg(bwin1)
        if f:
            p=getpoint(w,h,pts)
            m.click(p[0],p[1],1,1)
            ft=0
        delay(10)
        f,w,h,pts = findimg(bfail1)
        if f:
            p=getpoint(w,h,pts)
            m.click(p[0],p[1],1,1)
            ft=1

        f,w,h,pts = findimg(bwin2)
        if f:
            p=getpoint(w,h,pts)
            m.click(p[0],p[1],1,1)
            ft=1
        
        if ft>=0:
            print ftxt[ft]
        delay(10)



def yhsolo(t):
    m = PyMouse()
    btz = 'btz.PNG'
    bwin2 = 'bwin2.png'
    bfail1="bfail1.png"

    print "Start YuHun Solo...",t

    MAXT=1000
    if t>0: MAXT=t

    count=0
    while count<MAXT:
        count+=1
        print "GO #",count

        f,w,h,pts = findimg(bwin2)
        if f:
            p=getpoint(w,h,pts)
            m.click(p[0],p[1],1,1)
            print "--->Win #",count
        
        f,w,h,pts = findimg(bfail1)
        if f:
            p=getpoint(w,h,pts)
            m.click(p[0],p[1],1,1)
            print "--->Fail #",count

        while 1:
            f,w,h,pts = findimg(btz)
            if f:
               p=getpoint(w,h,pts)
               m.click(p[0],p[1],1,1)
               print "Start #",count
               break
            delay()

        
        delay(20)

        while 1:
            f,w,h,pts = findimg(bwin2)
            if f:
                delay(3)
                f,w,h,pts = findimg(bwin2)
                p=getpoint(w,h,pts)
                m.click(p[0],p[1],1,1)
                print "--->Win #",count
                break
            delay()
        
        delay(5)

        


