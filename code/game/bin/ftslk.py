#!/usr/bin/env python
import sys
import re
import pdb
from copy import deepcopy as cp

def prcfield(r):
    r=r.strip()
    #pdb.set_trace()
    try:
        if re.search("[0-9\.]*"):
            return float(r)
        return int(r)
    except Exception:
        pass

    return r

def readslk(slk,h,c):
    f=open(slk)
    for l in f:
        if l.startswith('E'): break
        if re.match("C;[XY].*K",l):
            c.append(l)
        elif l.startswith("ID") or l.startswith("B"):
            h.append(l)
def newarr(x):
    a=[]
    x+=1
    while x>0:
        a.append(None)
        x-=1
    return a

def procRecord(s):
    r=s.split(';')
    y=0
    x=0
    k=""
    for j in r:
        if re.match('Y',j):
            y=int(j[1:])
        if re.match('X',j):
            x=int(j[1:])
        if re.match('K',j):
            k=prcfield(j[1:])
    return y,x,k

def svC(dc,c,X):
    #pdb.set_trace()
    y=0
    for s in c:
        tmpy,x,k = procRecord(s)
        if tmpy>0:
            y=tmpy
            dc[y]=newarr(X)
        dc[y][x]=k

def svB(h):
    j=0
    for i in h:
        if i.startswith('B'):
            y,x,k=procRecord(i)
            k=""
            for tmp in i.split(';')[3:]:
                k+=tmp
            return j,y,x,k
        j+=1
    return 0,0,0,0


def pr1data(pa,cmd,newp=None):
    if len(cmd)==3:
        pa[int(cmd[1])] = cmd[2]

    if len(cmd)==4 and cmd[3] in '+-*/' :
        pa[int(cmd[1])]=eval(pa[int(cmd[1])]+cmd[3]+cmd[2])

    if len(cmd)==4 and cmd[3] == 'cp' and newp != None:
        newp[cmd[2]] = cp(pa)
        newp[cmd[2]][int(cmd[1])] = cmd[2]

def modSLK(p,func,cmd,newp=None):
    for k in p:
        if k == 1: continue
        if p[k][1] == None: continue
        if cmd[0] in p[k][1]:
            func(p[k],cmd,newp)
        if cmd[0] == '*':
            func(p[k],cmd,newp)
    return newp

def joinSLK(*args):
    y=1
    p={}
    for dic in args:
        for k in dic:
            if len(dic[k]) > 0:
                p[y]=dic[k]
                y+=1
    return y-1,p

def getreflist(p):
    a=[]
    f=open(p)
    for l in f:
        if not l.startswith("#"):
            k = l.strip().split()
            if len(k)>0:
                a.append(k )

    return a


def rRecord(s,y,x,k):
    if y >0:
        return s+";Y{};X{};K{}".format(y,x,k)
    return s+";X{};K{}".format(x,k)

def prtSLK(h,slk):
    for j in h:
        print j.strip()

    for key in slk:
        i=1
        if slk[key] == [] or slk[key][i]==None: continue
        print rRecord('C',key,i,slk[key][i])
        i+=1
        for xr in slk[key][2:]:
            #pdb.set_trace()
            if xr == "" or xr == None:
                i+=1
                continue
            print rRecord('C',0,i,xr)
            i+=1

    print "E"


def prtCSV(slk,p=False):
    a=[]
    for k in slk:
        if p:
            print re.sub("[\[\]]","","{},{}".format(k,slk[k]))
        a.append(slk[k])
    return a

def parseSLK(srcf):
    h=[]
    c=[]
    slk={}
    readslk(srcf,h,c)
    bj,y,x,hk = svB(h)
    svC(slk,c,x)

    h[bj]=rRecord("B",y,x,"")[:-1]+hk
    return h,slk


def test(a,b):
    h,slk=parseSLK(a)

    ref=getreflist(b)

    slk1=newSLK(slk,u_addtech,ref,1)
    pdb.set_trace()
    prtSLK(h,slk)

if __name__ == "__main__":
    h,slk=parseSLK(sys.argv[1])
    prtCSV(slk,True)

