from advscript import *
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
	

	#if task.__name__ == "jward":

	blist = ["btz","bwin2","bfail1"]
	comlist= ["ftb"]

	p0 = Process(target=task, args=(count,))
	p0.start()
	p_list.append(p0)

	p1 = Process(target=preventstuck)
	p1.start()
	p_list.append(p1)

	
	#not a good way, pyhook is better
	with keyboard.Listener(on_press=press_f12) as listener:
		listener.run()
