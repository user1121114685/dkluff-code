from scripts import *
import sys

from multiprocessing import Process

def parseArg():
	optblist = ["btz","bts","bzb"]
	
	print optblist
	print "yhsolo 0 btz"

	task=sys.argv[1]
	count=int(sys.argv[2])
	t=eval(task)

	try:
		optblist=sys.argv[3:]
	except:
		pass

	return t,count,optblist


if __name__ == "__main__":
	"""
	ToDo:
		*what if win32 api blocked? directx/winio
		*match button in random size
	"""
	print "Must run as admin!!!!"
	
	task,count,blist= parseArg()

	commlist = ["bwin2","bfail1","bxz","bwin1"]
	

	p0 = Process(target=yhsolo, args=(count,commlist,))
	p0.start()

	p1 = Process(target=yhsolo, args=(count,blist,))
	p1.start()
	
	
