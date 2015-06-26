#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from prslk import *
from copy import deepcopy as cp
import pdb

ABI='/root/otg_game/units/datacook/cook_item/'
ITEM='/root/otg_game/units/datacook/cook_ability/'
CMDOT='/root/otg_game/cook/cmd.txt'

def optxtdb(fdir):
    a=[]
    f=open(fdir)
    for l in f:
        a.append(l.strip().split())
    return a

def opslkdb(fdir):
    a=[]
    h,slk=parseSLK(fdir)
    a=prtCSV(slk)
    return h,slk,a

def a2d(a,d):
    for r in a:
        if r[1] == None: continue
        if r[0] == None: r[0]=""
        dkey=re.sub("[^A-Za-z0-9_\.]","",r[0]+"_"+r[1])
        if dkey in d:
            d[dkey]+=r[2:]
        d[dkey] = r[2:]


def readbyIDD(idd,arr,k=1):
    r=[]
    for a in arr:
        for i in a:
            if idd in i[k]:
                r.append(i)
                continue
    return r

def updatearr(arr,src,dst):
    for k in arr:
        if not k==None:
            re.sub(src,dst,k)

def prtarr(arr,f=None):
    s=""
    for k in arr:
        try:
            s+=k+" "
        except Exception:
            s+=str(k)+" "
    print s
    if f:
        print >>f,s

def duprecord(idd,newidd,dic):
    for k in dic:
        if newidd in k:
             print "Error: duplictename"
             return
    for k in dic:
        if idd in k:
            nk=re.sub("_[A-Za-z0-9]*","_"+newidd,k)
            narr=cp(dic[k])
            updatearr(narr,idd,newidd)
            prtarr([nk]+narr)


def getoptvalue(idd,dic,opt,k=1):
    for key in dic:
        if idd in key:
            for i in dic[key]:
                if i.startswith(opt):
                    return re.sub(opt+"=","",i)
    return "Not Found"

def a2s(a):
    s=""
    for i in a:
        if i==None: continue
        s+=i+" "
    return s

def linkidd2name(s,dictxt):
    k=set(re.findall("<[a-zA-z0-9]*",s))
    for r in k:
        s=re.sub(r,"__"+getoptvalue(r[1:],dictxt,"Name")+"__"+r,s)
    return s

def prt_txt(idd,dictxt,dicslk,abi_dictxt,abit_dicslk):
    #pdb.set_trace()
    if idd == None: return
    s="----\n"
    for k in dictxt:
        if idd in k:
            s+=k+" : "+a2s(dictxt[k])
            s+="\n"

    s+="\nSLK:\n"
    for k2 in dicslk:
        if idd in k2:
            s+=k2+" : "+a2s(dicslk[k2])

    print linkidd2name(s,abi_dictxt)

def findtxt(s,dictxt):
    r=[]
    for k in dictxt:
        if re.search(s,k):
            r.append(k)
            continue
        #dicstr=a2s(dictxt[k])
        #pdb.set_trace()
        if s in a2s(dictxt[k]):
            r.append(k)
            continue
    #pdb.set_trace()
    return r

def prcmd(s,txtdb,slkdb,abi_txtdb,abi_slkdb,cmd=None):
    if len(s) == 0: return
    incmd=s.split()
    incmd[0]=incmd[0].lower()

    if incmd[0] == 'cm':
        cmd.append(['\n'+'#']+incmd[1:])
        return

    if incmd[0] == 'u':
        print "cmd: ",cmd
        if len(cmd)>0 :
            cmd.pop()
            print "new cmd: ",cmd
        return

    if incmd[0] == 'pi':
        prt_txt(incmd[1],txtdb,slkdb,abi_txtdb,abi_slkdb)
        return

    if incmd[0] == 'pa':
        prt_txt(incmd[1],abi_txtdb,abi_slkdb,abi_txtdb,abi_slkdb)
        return

    if incmd[0] == 'si':
        for k in findtxt(incmd[1],txtdb):
            prt_txt(k,txtdb,slkdb,abi_txtdb,abi_slkdb)
        return

    if incmd[0] == 'sa':
        #pdb.set_trace()
        for k in findtxt(incmd[1],abi_txtdb):
            k=re.sub(".*_","",k)
            prt_txt(k,abi_txtdb,slkdb,abi_txtdb,abi_slkdb)
            for j in findtxt(k,txtdb):
                print "Item----"
                prt_txt(j,txtdb,slkdb,abi_txtdb,abi_slkdb)
        return

    if incmd[0] == 'ki' or incmd[0] =='ka':
        #kit - item txt
        #kis - item slk
        if incmd[0] =='ki':
            duprecord(incmd[1],incmd[2],txtdb)
            duprecord(incmd[1],incmd[2],slkdb)
        #kat - abi txt
        #kas - abi slk
        if incmd[0] =='ka':
            duprecord(incmd[1],incmd[2],abi_txtdb)
            duprecord(incmd[1],incmd[2],abi_slkdb)

        cmd.append([incmd[0]+'t']+incmd[1:]+["cp"])
        cmd.append([incmd[0]+'s',incmd[1],1,"\""+incmd[2]+"\"","cp"])

    if incmd[0].startswith('k') and len(incmd[0])==3:
        cmd.append(incmd)

def prtcmd(cmd):
    cmdf=open(CMDOT,'a')
    for k in cmd:
        prtarr(k,cmdf)
    print >>cmdf,"\n"

def run(txtdb,slkdb,abi_txtdb,abi_slkdb,cmd):
    while 1:
        incmd=raw_input("Input CMD:\n")
        prcmd(incmd,txtdb,slkdb,abi_txtdb,abi_slkdb,cmd)
        if incmd == 'x':
            break
        if incmd == 'px':
            prtarr(cmd)

def test(txtdb,slkdb,abi_txtdb,abi_slkdb):
    #pdb.set_trace()
    prcmd("si 智力",txtdb,slkdb,abi_txtdb,abi_slkdb)

if __name__ == "__main__":
    pdir='/root/otg_game/units/datacook/'
    txtdb={}
    slkdb={}
    abi_txtdb={}
    abi_slkdb={}

    a2d(optxtdb(pdir+'cook_item/all.db'),txtdb)
    a2d(optxtdb(pdir+'cook_ability/all.db'),abi_txtdb)

    h,slk,a = opslkdb(pdir+'cook_item/data/ItemData.slk')
    a2d(a,slkdb)

    ah,aslk,aa = opslkdb(pdir+'cook_ability/data/AbilityData.slk')
    a2d(aa,abi_slkdb)


    #test(txtdb,slkdb,abi_txtdb,abi_slkdb)
    cmd = []
    newtxtdb,newslkdb,newabi_txtdb,newabi_slkdb = {},{},{},{}
    run(txtdb,slkdb,abi_txtdb,abi_slkdb,cmd)
    prtcmd(cmd)














