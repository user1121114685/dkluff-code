#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import random

MAXNUM=33

def fmtdata(rr):
  k=re.sub("[^0-9]"," ",rr)
  return [ int(i) for i in k.split() ]

def readdata(fdir):
    f = open(fdir)
    return [ fmtdata(l) for l in f.readlines() ]

def prc_omit_hit(data):
    """
    input: data=[n1,n2,...]
    output: [0,0,...1,1..]
    """
    o = [ 1 for i in range(MAXNUM+1) ]
    for n in data:
        if n >MAXNUM: continue
        o[n] = 0
    return o

def sub_arr(src,dst):
    r=[]
    i=0
    for s in src:
        r.append((s+1)*dst[i])
        i+=1
    return r


def prc_omit_tt(data,omit_tt=None):
    omit_all = []
    if omit_tt is None:
        omit_tt = [ 0 for i in range(MAXNUM+1) ]
    for l in data:
        omit_tt = sub_arr(omit_tt,prc_omit_hit(l))
        omit_all.append(omit_tt[1:])

    return omit_all

def select_cols(data,start=7,end=7):
    r=[]
    for l in data:
        r.append(l[start:][:end-start+1])
    return r

def select_rows(data,count=1,israndom=False):
    r=[]
    rowcount=len(data)

    if  israndom:
        while count >0:
            r.append(data[random.randint(1,rowcount-1)])
            count-=1
    else:
        r=data[rowcount-count:]
    return r

def cal_row_sum(row):
    s=0
    for i in row:
        s+=i
    return s

def cal_row_avg(row):
    return cal_row_sum(row)/len(row)

def data_to_row(data,col):
    r=[]
    for d in data:
        r.append(data[col])
    return r

def cal_col_avg(data,col):
    return cal_row_avg(data_to_row(data,col))


#slice: row[start:lenght+start]
#last: d[-1:]

def join_rows(a,b,end=2*MAXNUM):
    i=0
    r=[]
    for d in a:
        r.append((d+b[i])[:end])
        i+=1
    return r

def prtrows(data):
    for r in data:
        s=""
        for i in r:
            s+=str(i)+" "
        print s

def run():
    data=readdata("/root/tmp/ssq.txt")

    #data=select_rows(data,50)
    #data=select_rows(data,25,True)

    blue_omit=prc_omit_tt(select_cols(data))
    red_omit=prc_omit_tt(select_cols(data,1,6))

    prtrows(join_rows(red_omit,blue_omit,49))



if __name__ == "__main__":
    run()




