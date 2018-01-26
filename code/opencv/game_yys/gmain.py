from scripts import *
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


if __name__ == "__main__":
	"""
	ToDo:
		*what if win32 api blocked? directx/winio
		*match button in random size
	"""
	print "Must run as admin!!!!"

	task,count = parseArg()
	blist = ["btz"]	
	commlist = ["bwin2","bfail1","bxz"]	
	if task.__name__ == "jward":
		commlist+=["bzb"]
	
	if task.__name__ == "story":
		blist=["st1","st2","st3","st4","st5","bzb","btscomm"]

	if task.__name__ == "tssolo":
		commlist=["bts","btsboss","btsbox","btscomm","bts_c8"]
		blist=["btsstandby","btscomm"]

	if task.__name__ == "jward":
		blist=["jjk","bjjs","bjjf","bsx","bjg","bqd","jjt"]

	commdict=readimgs(commlist)
	bdict=readimgs(blist)

	if task.__name__ == "tssolo":
		pt = Process(target=yhsolo, args=(count,commdict,))
		pt.start()
		p_list.append(pt)

	p0 = Process(target=yhsolo, args=(0,commdict,))
	p0.start()
	p_list.append(p0)

	p1 = Process(target=task, args=(count,bdict,))
	p1.start()
	p_list.append(p1)

	if onSLOWPC:
		ptslow=Process(target=slowpc, args=(584,190,))
		ptslow.start()
		p_list.append(ptslow)
	
	#not a good way, pyhook is better
	with keyboard.Listener(on_press=press_f12) as listener:
		listener.run()
