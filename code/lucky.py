#!/usr/bin/env python
import random
import re
import sys
#from collections import Counter

MAXNUM=36

def initbm(m=MAXNUM):
  bm = {}
  while m > 0:
    bm[m] = 0
    m-=1
  return bm

def procfile(fdir):
  f = open(fdir)
  r = [ l.split() for l in f.readlines()]
  return r

def fmtdata(rr):
  k=re.sub("[^0-9]"," ",rr)
  return [ int(i) for i in k.split() ]

def countb(bmdic,k,s=1,e=6):
  while s<=e:
    bmdic[k[s-1]]+=1
    s+=1

def pickballs(b):
  l=len(b)
  c=random.randint(0,l-1)
  r=[]
  while c>=0:
    r.append(b[random.randint(0,c)])
    c-=1
  return r

def run(fdir,s=1,e=5):
  r = procfile(fdir)
  balls = [ fmtdata(i[3]) for i in r ]
  balls = pickballs(balls)
  bm=initbm()
  l=len(balls)
  for i in balls:
    countb(bmdic=bm,k=i,s=s,e=e)
  printbm(bm,l)

def printbm(bm,l):
  q=sorted(bm.iteritems(),key=lambda x:x[1],reverse=True)
  k=1
  for i in q:
    print "[{:0>2d}] {:0>2d} :{:.2%} : {}".format(k,int(i[0]),i[1]*1.0/l,"="*(100*i[1]/l))
    k+=1


if __name__ == "__main__":
  run(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))


