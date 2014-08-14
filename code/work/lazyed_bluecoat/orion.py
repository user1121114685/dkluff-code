#!/usr/bin/env py27
import re
import sys

fwlog = '/tmp/fw-outside.csv'
laglog = '/tmp/globe-Response_Time_and_Packet_Loss.csv'
cpumemlog = '/tmp/globe-CPU_and_Memory_Load.csv'

REG_dropline = re.compile(r'^#|Node|TEMP|216.200.88.246',flags=re.IGNORECASE)
REG_dropline_nofw = re.compile(r'^#|Node|TEMP|216.200.88.246|FW0|Edge',flags=re.IGNORECASE)
REG_delstrings = re.compile(r'\..*.COM|"',flags=re.IGNORECASE)

#pattern:full name
DicLocation = {"CHN":"CTC(HangZhou)","POL":"Poland",
        "ADCA":"DC6-SocialAPPs","BJ":"BeiJingR&D",
        "ASH":"Ashburn"
                }
#return name, not pattern
def getalias(k):
    if k == "CHN" or k == "CTC":
         return "CTC"
    if k == "DC6" or k == "ADCA":
        return "DC6"
    return k




#----Latency----#
#lags={}#node:[ip,avg_res,pk_res,lost]
lag_format=(0,1,2,4,5)

#----Fw proc----#
#fws={} #node:[ip,avg_rx,pk_rx,avg_tx,pk_tx,avg_rxtx,total_rxtx]
fw_format=(0,1,2,3,4,5,9,10)

#cpumems={}Node ,ip,Average CPU Load,Peak CPU Load ,  Average Percent Memory Used, Peak Memory Used
cpumem_format=(0,1,2,3,4,5)


def read_csv(logfile,f_type,pattern,dropreg=REG_dropline):
    f = open(logfile)
    REG_matchp = re.compile(pattern.upper())
    dic = {}
    for line in f:
        vals = []
        if not dropreg.search(line):
            s = line[:-2].split(",")
            for x in f_type:
                vals.append(s[x])
            #chk vals is legal
            if '' in vals: continue

            vals[0] = vals[0].upper()
            if REG_matchp.search(vals[0]):
                for index,val in enumerate(vals):
                    vals[index] = REG_delstrings.sub("",val)
                dic[vals[0]] = vals[1:]
    f.close()
    return dic

from liblaz.dklib import drawTab,drawBar,drawTime
from liblaz.fwcss import CSS,HTML,lactabs
import time

def printTab(pat,navhead):
    fws = read_csv(fwlog,fw_format,pat)
    lags = read_csv(laglog,lag_format,pat,dropreg=REG_dropline_nofw)
    cpumems = read_csv(cpumemlog,cpumem_format,pat)

    if not cpumems:
        return ""

    titlelocation = DicLocation[pat]
    lacid = getalias(pat)

    avg_resp = "{0:.0f}ms".format(sum(int(lags[k][1].split()[0]) for k in lags)/len(lags))
    pk_resp = "{0:.0f}ms".format(sum(int(lags[k][2].split()[0]) for k in lags)/len(lags))
    packetlost = "{0:.2f}%".format(min(int(lags[k][3].split()[0]) for k in lags))
    lagtab = drawTab(5).format(\
            titlelocation,
            avg_resp,
            pk_resp,
            packetlost,
            len(lags)
            )

    fwtab=""
    for k in fws:
        avg_rc = fws[k][1]
        pk_rc = fws[k][2]
        avg_tx = fws[k][3]
        pk_tx = fws[k][4]
        avg_rctx = fws[k][5]
        tot_rctx = fws[k][6]
        fwtab += drawTab(7).format(\
                k,
                avg_rc,
                pk_rc,
                avg_tx,
                pk_tx,
                avg_rctx,
                tot_rctx
                )

    cputab = ""
    cpus={}
    memtab = ""
    mems={}
    for k in cpumems:
        cpuload = int(cpumems[k][1].split()[0])
        memload = int(cpumems[k][3].split()[0])
        if cpuload >= 50:
            cpus[k] = [cpumems[k][2],cpumems[k][1],drawBar(cpuload,100)]
        if memload >= 50:
            mems[k] = [cpumems[k][4],cpumems[k][3],drawBar(memload,100)]

    for k in cpus:
        v = [k] + list(x for x in cpus[k])
        cputab += drawTab(4).format(v[0],v[1],v[2],v[3])

    for k in mems:
        v = [k] + list(x for x in mems[k])
        memtab += drawTab(4).format(v[0],v[1],v[2],v[3])


    outtab = lactabs.format(_titlelocation=titlelocation,
            _navhead=navhead,
            _lacid=lacid,
            _cputab=cputab,
            _memtab=memtab,
            _fwtab=fwtab,
            _lagtab=lagtab,
            )

    return outtab


def run():
    tabs  = ""
    navhead=""
    for k in DicLocation:
        navhead += """<a href="#{_l}">{_l}</a> """.format(_l=getalias(k))
    for k in DicLocation:
        tabs += printTab(k,navhead)

    html = HTML.format(_titletime=drawTime(),
            _style=CSS,
            _tabs=tabs)

    return html




if __name__ == "__main__":
    #printTab(sys.argv[1].upper())
    print run()

