#!/usr/bin/env python
import random
import re
import sys
from time import sleep
#from collections import Counter

MAXNUM=36
SLEEP=0.5

def procfile(fdir):
  f = open(fdir)
  r = [ l.split() for l in f.readlines()]
  return r

def fmtdata(rr):
  k=re.sub("[^0-9]"," ",rr)
  return [ int(i) for i in k.split() ]

def countb(resultdic,item,s=1,e=6):
  while s<=e:
    resultdic[item[s-1]]+=1
    s+=1

def pickballs(b):
  l=len(b)
  c=random.randint(0,l-1)
  r=[]
  while c>=0:
    r.append(b[random.randint(0,c)])
    c-=1
  return r

def run(fdir,s=1,e=6,play=False):
  r = procfile(fdir)
  balls = [ fmtdata(i[3]) for i in r ]
  if play: return [ b[s-1:][:e-s+1] for b in balls ]
  balls = pickballs(balls)
  total_len =  len(balls)
  ballcount = { i:0 for i in range(1,MAXNUM) }
  for i in balls:
    countb(resultdic=ballcount,item=i,s=s,e=e)
  #
  #print ballcount
  #
  return getlucky(ballcount,total_len=total_len,outputlength=e-s+1)

def getlucky(ballcount,total_len,outputlength=6):
  q=sorted(ballcount.iteritems(),key=lambda x:x[1])
  k=1
  lucky=[]
  for i in q:
    print "[{:0>2d}] {:0>2d} :{:.2%} : {}\
          ".format(k,int(i[0]),i[1]*1.0/total_len,"="*(100*i[1]/total_len))
    if i[1] > 0 and len(lucky)<outputlength:
      lucky+=[i[0]]
    k+=1
  return lucky

def printrolls(lucky,m=MAXNUM,w=7):
  numfmt = "{:0>2d}".format
  fmt = '\033[0;32m{}\033[0m'.format
  r=[ fmt(numfmt(i)) if i in lucky else numfmt(i) for i in range(1,m)]

  c=len(r)/w
  k=0
  while k<=c:
    for i in r[w*k:][:w]:
      sys.stdout.write(i+' ')
    k+=1
    print

def cls():
    print chr(27) + "[2J"



if __name__ == "__main__":
  f=sys.argv[1]
  s1=1
  e1=6
  s2=7
  e2=7

  if 'd' in sys.argv[2] :
    e1,s2 = 5,6

  p1=run(f,s1,e1)
  p2=run(f,s2,e2)
  print p1,":",p2
  printrolls(p1)
  printrolls(p2)

  play = True if 'p' in sys.argv[2] else False
  r=int(re.sub("[^0-9]","",sys.argv[2])) if re.search("[0-9]",sys.argv[2]) else 0
  if play :
    b=(run(f,s1,e1,play),run(f,s2,e2,play))
    for i in b[r]:
      cls()
      printrolls(i)
      sleep(SLEEP)



