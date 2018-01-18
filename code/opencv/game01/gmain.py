
from scripts import *
import sys

def main():
	print "yhsolo 0"
	print "faildeamon 0"
	
	task=sys.argv[1]
	count=int(sys.argv[2])
	t=eval(task)
	t(count)

	
if __name__ == "__main__":
	main()
	
