#!/usr/bin/env python
# coding=utf-8
import re
import json
import sys


fmt = '\033[0;3{}m{}\033[0m'.format

def cls():
  print chr(27) + "[2J"

def fmtAnswer(s,sp=None):
  r=re.sub("Answer:| |\r|\n","",s)
  if sp is None:
    a=[]
    for i in r.upper():
      a+=[i]
    return a
  return r.upper().split(sp)

def fmtItem(item):
  q=""
  l=len(item)
  i=0
  while i < l:
    q+=item[i]
    i+=1
    if re.search("^[A-Z]\.",item[i]):
      break

  return [q,item[i:]]

def readf(f):
  exam=[]
  for l in f:
    r=re.search("^[0-9]*\.",l)
    item=[]
    if r:
      while not l.startswith("Answer:"):
        item+=[l]
        l=f.next()
      exam+=[fmtItem(item)+[fmtAnswer(l,sp=",")]]
      #exam[i] = [ q,[opts],[ans] ]

  return exam

def examTodict(exam):
  j={}
  iid=1
  for i in exam:
    j[str(iid)]={"question":i[0],"opts":i[1],"ans":i[2]}
    iid+=1

  return j

def prtq(item):
  print "----->"
  print fmt(4,item[0])
  for i in item[1]:
    print i


def prtRes(answer,myanswer,item):
  print "Answer is :",answer
  c=1
  if answer == myanswer:
    c=2
  for i in item:
    if i[0] in answer:
      print fmt(c,i)
    else:
      print i

  return answer == myanswer

def recordmis(fdir,iid):
  with open(fdir,'a') as r:
    print >> r,iid



def play(p):  
  iid=0
  lenth=len(p)
  while iid <lenth:
    cls()
    i=p[iid]
    prtq(i)
    with open(bookmark,'a') as bk:
      print >>bk,iid+1
    myanswer=fmtAnswer(raw_input("Enter Answers: "))
    cls()
    print fmt(4,i[0])
    tf=prtRes(i[2],myanswer,i[1])
    if not tf:
      recordmis(logfile,iid+1)
  
    iid+=1
  
    c=raw_input("<----Continue...?")
    try:
      iid=int(c)-1
    except Exception:
      pass

  
if __name__ == "__main__":

  f=open(sys.argv[1])
  logfile="wrlog.log"
  bookmark="bookmark.txt"
  p=readf(f)
  wrgs=[]
  if len(sys.argv) == 3:
    wrgfile=sys.argv[2]
    print "Review...."
    with open(wrgfile) as r:
      for l in r:
        wrgs+=[p[int(l[:-1])-1]]
  if len(wrgs) > 0:
    play(wrgs)
  else:
    play(p)

