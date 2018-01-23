from exlib.botv import *
import sys

img=sys.argv[1]

w,h,pts = find2grid(img,3,3)
cropscreen(w,h,pts)