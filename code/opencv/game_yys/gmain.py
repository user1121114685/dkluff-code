from scripts import *
import sys

from multiprocessing import Process

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

	if task.__name__ == "tssolo":
		pt = Process(target=yhsolo, args=(count,commlist,))
		pt.start()

		commlist=["bts","btsboss","btsbox","btscomm","bts_c8"]
		blist=["btsstandby","btscomm"]
		
	p0 = Process(target=yhsolo, args=(0,commlist,))
	p0.start()
 
	p1 = Process(target=task, args=(count,blist,))
	p1.start()
	
	
