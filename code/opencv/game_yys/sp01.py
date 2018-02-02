from botv import *

import time
import random
import os

from pymouse import PyMouse
from botcfg import *

import sys

from multiprocessing import Process
from pynput import keyboard
from botcfg import *
from botv import readimgs

import pdb

p_list=[]
def killer():
    print "Kill All..."
    for p in p_list:
		p.terminate()

def press_f12(key):
    if key == keyboard.Key["f12"]:
		killer()
		return False

def parseArg():
	print "yhsolo 0"
	task=sys.argv[1]
	count=int(sys.argv[2])
	t=eval(task)
	return t,count

def sfloop(t,bdict={},bmstring="bwin2"):
    while 1:
        sfeng(t,bdict)
        print "|--------------------|"


def sfeng(t,bdict={},bmstring="bwin2"):
    lb=len(bdict)
    if lb==0:
        return
    m = PyMouse()

    print "----------->Go"
    uwaitchkk("sfm",bdict,m)
    time.sleep(10)
    if chkk("sf0",bdict,m):
        chkk("sf1",bdict,m)
        uwaitchkk("sf3",bdict,m)
        chkk("sf4",bdict,m)
    
    chkk("sfx",bdict,m)

    print "----------->"

    uwaitchkk("jx",bdict,m)
    uwaitchkk("jx1",bdict,m,10)
    uwaitchkk("btz",bdict,m)
    uwaitchkk("bwin2",bdict,m,20)
    uwaitchkk("jxx",bdict,m,20)
    uwaitchkk("back",bdict,m,20)
    waitchkk("sfm",bdict,m)

    print "----------->End"


if __name__ == "__main__":
    jx=["jx","jx1","jxx","btz","bwin2","back"]
    blist=["sfx","sfm","sf0","sf1","sf3","sf4"]
    blist+=jx
    bdict=readimgs(blist)

    p0 = Process(target=sfloop, args=(0,bdict,))
    p0.start()
    p_list.append(p0)

    with keyboard.Listener(on_press=press_f12) as listener:
		listener.run()