#!/usr/bin/env python
#Usage: python lazed.py /opt/logfile/chn

import os,sys,re
from os.path import join
import fnmatch
import time

#date,cip,hip,temp_sc,temp_cs,cache_status,protocol
LOGTYPE_MAIN=(0,3,15,22,23,11,16)
LOGTYPE_SSL=(0,3,14,19,20,10,15)
CACHE_STATUS = 'TCP_HIT'

#date,cip,hip,c_read,s_read,c_written
LOGTYPE_CIFS=(0,2,4,23,24,25)
REG_MATCH_UNDROP_CIFS=re.compile('CLOSE')

REG_MATCHDROP=re.compile('^#|tcp_error')
REG_MATCHDENIED=re.compile('policy_denied')
REG_MATCHVPN=re.compile('^10.*[0-9]$|prod-|microstrategy')

#[readlines,droplines]
COUNTER_LINES=[0,0]
#"hostname/date":[req,unhit_sc+unhit_cs,hit_sc+hit_cs]
interHost={}
vpnHost={}
allDaily={}
#{"hostname":[deniedreq,set()]}
interDeniedHost={}

from liblaz.dklib import *
PROTOCOL={}
for k in PROTO_NAME_LIST:
    PROTOCOL[k[0]]=[0,0,0]
    PROTOCOL['VPN'+k[0]]=[0,0,0]
PROTOCOL['VPNCIFS']=[0,0,0]

def coroute(func):
    def _coroute(*args,**kw):
        gen = func(*args, **kw)
        gen.next()
        return gen
    _coroute.__name__ = func.__name__
    _coroute.__dict__ = func.__dict__
    _coroute.__doc__  = func.__doc__
    return _coroute

@coroute
def find_files(tg):
    readfiles = 0
    while True:
        topdir,pattern = (yield readfiles)
        for path,dirname,filelist in os.walk(topdir):
            for name in filelist:
                if fnmatch.fnmatch(name,pattern):
                    print "<!-- #Reading file:",os.path.join(path,name),"-->"
                    readfiles += 1
                    tg.send(os.path.join(path,name))
                    #commite to db?

import gzip

@coroute
def gzopener(tg):
    while True:
        name = yield
        try:
            if name.endswith(".gz") or name.endswith(".done"):
                f = gzip.open(name)
            else:
                f = open(name)
        except IOError as e:
            print e
            name = yield
        tg.send(f)

@coroute
def sendlines(tg):
    while True:
        f = (yield)
        for line in f:
            tg.send(line)

@coroute
def procNonCIFS(logtype):
    while True:
        line  = yield
        COUNTER_LINES[0]+=1

        if REG_MATCHDROP.search(line) is not None:#bad line drop matched
            COUNTER_LINES[1]+=1
            continue

        f = REG_REMOVESPACE.sub("X",line).split()
        date,cip,hip,unhit_sc,unhit_cs,hit_sc,hit_cs = ("-","-","-",0,0,0,0)

        """
        Get values from f
        """
        date,cip,hip,temp_sc,temp_cs,cache_status,protocol = (f[x] for x in logtype)

        """
        check values
        """
        if "-" in(date,cip,hip,temp_sc,temp_cs,cache_status,protocol):
            COUNTER_LINES[1]+=1
            continue

        isVPN = False
        if REG_MATCHVPN.search(hip) or not REG_MATCH_PUBLIC_DNS.search(hip):
            isVPN = True

        if cache_status == CACHE_STATUS:
            hit_sc = int(temp_sc)
            hit_cs = int(temp_cs)
        else:
            unhit_sc = int(temp_sc)
            unhit_cs = int(temp_cs)

        isDenied = False
        if REG_MATCHDENIED.search(line):
            isDenied = True

        """
        Update values
        """

        if isDenied: #and not isVPN: #a policy denied record
            if hip in interDeniedHost:
                interDeniedHost[hip][0] += 1
                interDeniedHost[hip][1].add(cip)
            else:
                interDeniedHost[hip]   = [1,set()]
                interDeniedHost[hip][1].add(cip)
            continue
        else: #not isDenied:
            p = checkProtocol(protocol)
            if isVPN:
                aHost = vpnHost
                p = 'VPN' + p
            else:
                aHost = interHost
            for i,v in enumerate([1,unhit_sc+unhit_cs,hit_sc+hit_cs]):
                if hip in aHost:
                    aHost[hip][i] += v
                else:
                    aHost[hip] = [1]
                    aHost[hip] += [unhit_sc+unhit_cs,hit_sc+hit_cs]

                """
                Update Protocol
                """
                PROTOCOL[p][i] += v

                """
                Update Daily
                """
                if date in allDaily:
                    allDaily[date][i] += v
                else:
                    allDaily[date] = [1]
                    allDaily[date]+= [unhit_sc+unhit_cs,hit_sc+hit_cs]




@coroute
def procCIFS(logtype=LOGTYPE_CIFS):
    while True:
        COUNTER_LINES[0]+=1
        line = yield
        if REG_MATCH_UNDROP_CIFS.search(line) is None:
            COUNTER_LINES[1]+=1
            continue
        f = line.split()
        date,cip,hip,c_read,s_read,c_written = (f[x] for x in logtype)
        if "-" in (cip,hip,c_read,s_read,c_written):
            COUNTER_LINES[1]+=1
            continue
        cr=int(c_read)
        sr=int(s_read)
        cw=int(c_written)
        for i,v in enumerate([1,sr+cw,cr-sr+0]):
            if hip in vpnHost:
                vpnHost[hip][i] +=v
            else:
                vpnHost[hip]=[1]
                vpnHost[hip] += [sr+cw,cr-sr]

            PROTOCOL["VPNCIFS"][i] += v
            """
            Update Daily
            """
            if date in allDaily:
                allDaily[date][i] += v
            else:
                allDaily[date] = [1]
                allDaily[date]+= [sr+cw,cr-sr]


from liblaz.css import *
def run():
    #expect rootdir is like /opt/log/arg
    rootdir=sys.argv[1]
    maindir=join(rootdir,"main")
    ssldir=join(rootdir,"ssl")
    cifsdir=join(rootdir,"cifs")

    mainf = find_files(gzopener(sendlines(procNonCIFS(LOGTYPE_MAIN))))
    cmain=mainf.send((maindir,"*gz*"))

    sslf = find_files(gzopener(sendlines(procNonCIFS(LOGTYPE_SSL))))
    cssl=sslf.send((ssldir,"*gz*"))

    cifsf = find_files(gzopener(sendlines(procCIFS())))
    ccifs=cifsf.send((cifsdir,"*gz*"))

    if cmain+ccifs+cssl == 0:
        print "Error:No log files found!!!"
        sys.exit(1)

    #do calculate
    totalRequests = COUNTER_LINES[0]
    totalDrequests = 0
    for dk in interDeniedHost:
        totalDrequests += interDeniedHost[dk][0]

    NonVPNBytes = 0
    NonVPNBytes_cache = 0
    #NonVPNBytes_uncache = 0

    VPNBytes = 0
    VPNBytes_cache = 0
    #VPNBytes_uncache = 0

    for k in PROTOCOL:
        if "VPN" not in k:
            NonVPNBytes += sum(PROTOCOL[k][1:])
            NonVPNBytes_cache += PROTOCOL[k][2]
        else:
            VPNBytes += sum(PROTOCOL[k][1:])
            VPNBytes_cache += PROTOCOL[k][2]
    totalBytes = NonVPNBytes + VPNBytes
    #NonVPNBytes_uncache = NonVPNBytes - NonVPNBytes_cache
    #VPNBytes_uncache = VPNBytes - VPNBytes_cache
    totalBytes_cache = NonVPNBytes_cache + VPNBytes_cache
    totalBytes_uncache = totalBytes - totalBytes_cache

    totalBytes_cache_bar = drawBar(totalBytes_cache,totalBytes)
    totalBytes_uncache_bar = drawBar(totalBytes_uncache,totalBytes)
    VPNBytes_bar = drawBar(VPNBytes,totalBytes)
    NonVPNBytes_bar = drawBar(NonVPNBytes,totalBytes)

    """Daily Usage"""
    daytab=""
    key_date=sorted(allDaily)
    for k in key_date:
        daytab += drawTab(4).format(\
                k,
                allDaily[k][0],\
                humanRead(allDaily[k][1]+allDaily[k][2]),
                drawBar(allDaily[k][1]+allDaily[k][2],totalBytes)
                )
    """VPN - Top 10 Hosts By BytesUnCached"""
    vpn_toptab=""
    topvpn=dic_topten(vpnHost,1)
    for k in (x[0] for x in topvpn):
        vpn_toptab += drawTab(5).format(\
                k,
                vpnHost[k][0],
                humanRead(vpnHost[k][2]),
                humanRead(vpnHost[k][1]),
                drawBar(vpnHost[k][1],totalBytes)
                )

        _PROTOCOL =list(x[0] for x in PROTO_NAME_LIST)
        _vpnPROTOCOL = _PROTOCOL+["CIFS"]
        """VPN - Protocol Details"""
        vpn_protab=""
        for k in _vpnPROTOCOL:
            p = 'VPN'+k
            vpn_protab += drawTab(6).format(\
                k,
                PROTOCOL[p][0],
                humanRead(PROTOCOL[p][2]),
                humanRead(PROTOCOL[p][1]),
                humanRead(PROTOCOL[p][1]+PROTOCOL[p][2]),
                drawBar(PROTOCOL[p][1]+PROTOCOL[p][2],totalBytes)
                )
        """NonVPN - Protocol Details"""
        nonvpn_protab=""
        for p in _PROTOCOL:
            nonvpn_protab += drawTab(6).format(\
                p,
                PROTOCOL[p][0],
                humanRead(PROTOCOL[p][2]),
                humanRead(PROTOCOL[p][1]),
                humanRead(PROTOCOL[p][1]+PROTOCOL[p][2]),
                drawBar(PROTOCOL[p][1]+PROTOCOL[p][2],totalBytes)
                )
        """NonVPN - Top 10 Hosts By BytesUnCached"""
        nonvpn_toptab=""
        nonvpntop=dic_topten(interHost,1)
        for k in (x[0] for x in nonvpntop):
            nonvpn_toptab += drawTab(5).format(\
                    k,
                    interHost[k][0],
                    humanRead(interHost[k][2]),
                    humanRead(interHost[k][1]),
                    drawBar(interHost[k][1],totalBytes)
                    )
        """NonVPN - Top 10 Hosts By Requests"""
        nonvpn_reqtab=""
        nonvpn_reqtop=dic_topten(interHost,0)
        for k in (x[0] for x in nonvpn_reqtop):
            nonvpn_reqtab += drawTab(5).format(\
                    k,
                    humanRead(interHost[k][2]),
                    humanRead(interHost[k][1]),
                    interHost[k][0],
                    drawBar(interHost[k][0],totalRequests)
                    )
        """NonVPN - Top 10 Hosts By Denied Requests """
        nonvpn_dreqtab=""
        nonvpn_dreqtop=dic_topten(interDeniedHost,0)
        for k in (x[0] for x in nonvpn_dreqtop):
            nonvpn_dreqtab += drawTab(4).format(\
                    k,
                    interDeniedHost[k][0],
                    len(interDeniedHost[k][1]),
                    drawList(interDeniedHost[k][1])
                    )


    q=os.path.split(rootdir)
    while q[1] == '':
        q=os.path.split(q[0])
    titlelocation=q[1].upper()

    e_curtime=time.time()
    s_curtime=e_curtime-7*24*3600
    _e=time.strftime("%Y.%m.%d",time.localtime(e_curtime))
    _s=time.strftime("%Y.%m.%d",time.localtime(s_curtime))
    titletime=_s + " - " + _e

    style = CSS
    html = HTML

    outputdir="/tmp/html_output/"
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    outputfile = open(join(outputdir,titlelocation+".html"),'w')
    outputhtml = html.format(\
            _style=style,
            _titlelocation=titlelocation,
            _titletime=titletime,
            _totalBytes=humanRead(totalBytes),
            _VPNBytes=humanRead(VPNBytes),
            _VPNBytes_bar=VPNBytes_bar,
            _NonVPNBytes=humanRead(NonVPNBytes),
            _NonVPNBytes_bar=NonVPNBytes_bar,
            _totalBytes_cache=humanRead(totalBytes_cache),
            _totalBytes_cache_bar=totalBytes_cache_bar,
            _totalBytes_uncache=humanRead(totalBytes_uncache),
            _totalBytes_uncache_bar=totalBytes_uncache_bar,
            _totalRequests=totalRequests,
            _totalDrequests=totalDrequests,
            _daytab=daytab,
            _vpn_toptab=vpn_toptab,
            _vpn_protab=vpn_protab,
            _nonvpn_toptab=nonvpn_toptab,
            _nonvpn_protab=nonvpn_protab,
            _nonvpn_reqtab=nonvpn_reqtab,
            _nonvpn_dreqtab=nonvpn_dreqtab
            )
    print >>outputfile,outputhtml








if __name__ == "__main__":
    run()
    #print COUNTER_LINES,interHost,interDeniedHost,vpnHost,PROTOCOL
    for h in vpnHost:
        print h
