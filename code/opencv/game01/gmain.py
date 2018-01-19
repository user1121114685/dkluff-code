
from scripts import *
import sys

def main():
	print "yhsolo 0"

	task=sys.argv[1]
	count=int(sys.argv[2])
	t=eval(task)
	t(count)


if __name__ == "__main__":
	"""
	ToDo:
		*what if win32 api blocked?
		*match button in random size
	"""
	print "Must run as admin!!!!"
	main()
	
