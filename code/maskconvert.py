#!/usr/bin/env python
import sys
import math

"""
--config---
"""
SP="/" #INPUT separator
OSP=" " #OUTPUT  separator

def n2m(n):
    p=int(n)
    if p > 32:
      sys.exit("Error: Wrong input...")
    r=[]
    f=[255,255,255,255]
    z=[0,0,0,0]
    r=f[:p/8]+[(255>>(p%8))^255]
    r+=z[len(r):]
    return "%d.%d.%d.%d" % (r[0],r[1],r[2],r[3])

def m2n(m):
    r=0
    rs=m.split(".")
    for i in rs:
      if i == "0":
        continue
      p=8-math.log(256-int(i),2)
      if p <> math.floor(p):
        sys.exit("Error: Wrong input...")
      r+=int(p)

    return "%d" % r


def coroute(func):
    def _coroute(*args,**kw):
        gen = func(*args, **kw)
        gen.next()
        return gen
    _coroute.__name__ = func.__name__
    _coroute.__dict__ = func.__dict__
    _coroute.__doc__  = func.__doc__
    return _coroute


def parse(arg):
    if "." in arg:
      return m2n(arg)
    else:
      return n2m(arg)

@coroute
def run():
    while True:
      l=yield
      net,mask = ( i for i in l.split(SP))
      print net+OSP+parse(mask)


if __name__ == "__main__":
    if len(sys.argv) < 2:
       r=run()
       for l in sys.stdin:
         r.send(l)
    if len(sys.argv) == 2:
       print parse(sys.argv[1])

