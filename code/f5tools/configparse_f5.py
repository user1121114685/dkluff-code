#!/usr/bin/env python
#parser {} mode f5config to csv
import sys
import re

REG_IP=re.compile(r'[1-9][0-9]*(\.[0-9]+){3}')
REG_INDENT=re.compile('^[ ]*')
EOF='{'
FOE='}'

""" config for read argv of subcmd"""
BLOCK_SUBCMD = (
        "members",
        "origins",
        "rules",
        )

NONBLOCK_SUBCMD = (
        "pool",
        "destination",
        "originating-address",
        "translation-address",
        "translation",
        )
ALL_SUBCMD = NONBLOCK_SUBCMD + BLOCK_SUBCMD
PREFIX_POOL = "ltm pool "
PREFIX_VSERVER = "ltm virtual "

def ldepth(l,r):
    d=r.search(l).group(0)
    return (len(d),d)

def readconf(fdir):
    f=open(fdir)
    b=[]
    for l in f:
        b.append(l)
    f.close()
    return b

"""Pop a block by indent"""
def pop_block(f):
    b=[ ]
    b.append(f[0])

    md=ldepth(f[0],r=REG_INDENT)
    flag=(' '*md[0]) + FOE

    i=1
    l=len(f)
    while i<l:
        b.append(f[i])
        i+=1
        if f[i-1].startswith(flag):
            break

    return b,i

def block_to_dict(block):
    r_eof = '[^' + EOF + ']*'
    rdict={}
    k=re.search(r_eof,block[0]).group(0)
    rdict[k]=block[1:-1]
    return rdict

def nonblock_to_dict(x):
    r=x.split()
    lenth_r=len(r)
    if lenth_r == 2:
        return { strip_key(r[0]):r[1] }
    return { strip_key(x):x }

strip_key=lambda x: x.strip().strip(EOF).strip()

def readblock(block):
    if block[0].strip().endswith(EOF):
        return pop_block(block)
    return block[0],1

"""
convert a block of :
    "string"
 or   [sub1,sub2,]
to dict
"""
def parseblock(block):

    """return if a string """
    if isinstance(block,str):
        return nonblock_to_dict(block)

    bdict={}

    lenth_block= len(block)
    if lenth_block == 0:
        return bdict

    b,i = readblock(block)
    if isinstance(b,list):
        bdict.update({ strip_key(b[0]):parseblock(b[1:-1]) })
    else:
        bdict.update(nonblock_to_dict(b))
    bdict.update(parseblock(block[i:]))

    return bdict

"""read argv"""

keyformat = lambda k : k.split().pop()

def read_dict_byprefix(dic,n):
    vdict={}
    for k in dic:
        if k.startswith(n):
            subdict={}
            for kk in dic[k]:
                if kk in ALL_SUBCMD:
                    subdict.update({ kk: dic[k][kk] })
            vdict.update( { keyformat(k): subdict } )
    return vdict

HEADLINE="VserverName,PublicIP,InternalIP,PoolName"
REG_DEL_PREFIX=re.compile("/Common/")
def printcsv_byvserver(lv,lp):
    """
    ltmvserver,destination,member,pool
    """
    print HEADLINE
    output="%s,%s,%s,%s"

    for k in lv:
        destination=lv[k]["destination"]
        pool=lv[k]["pool"]
        members=lp[pool]["members"].keys()
        for m in members:
            r = (output) % (\
                    k,destination,m,pool
                    )
            print REG_DEL_PREFIX.sub("",r)

if __name__ == "__main__":
    conf = readconf(sys.argv[1])
    conf_dict = {}

    """read conf to dict"""
    while len(conf) > 0:
        b,i = readblock(conf)
        conf_dict.update(parseblock(b))
        conf=conf[i:]

    ltm_pool = read_dict_byprefix(conf_dict,PREFIX_POOL)
    ltm_vserver = read_dict_byprefix(conf_dict,PREFIX_VSERVER)

    #printcsv_byvserver(ltm_vserver,ltm_pool)
    for k in ltm_vserver:
      try:
        if not "/Common/slowloris_dos_mitigate" in [ i for i in ltm_vserver[k]['rules']]:
          print k
          continue
      except Exception as e:
          print k
          continue



