import re

REG_MATCH_PUBLIC_DNS=re.compile('\.[A-Za-z]{1,9}$|^[1-9]')
REG_REMOVESPACE=re.compile(r'".*?"') #remove space in Double quotes

PROTO_NAME_LIST=(
        ("HTTP","80","8080"),
        ("HTTPS","443"),
        ("SSH","22"),
        ("FTP","21"),
        ("RDP","3389"),
        ("VNC","5800",5900),
        ("OTHER","-"),
        #("CIFS","139","445"),
        )

def checkProtocol(s):
    p = s.upper()
    for k in PROTO_NAME_LIST:
        if p in k:
            return k[0]
    return "OTHER"

def humanRead(n):
    if n < 1000000:
        return "<1MB"
    if n < 1000000000 and n >1000000:
        return "{0:.2f}MB".format(n/1000000.00)
    else:
        return "{0:.2f}GB".format(n/1000000000.00)

def dic_topten(dic,f,p=False):
    """
    return a list[("hostname",[0,0,0]),]
        dic.iteritems().next()=("hostname",[r,sc+cs,sc+cs])
    """
    top=sorted(dic.iteritems(),key=lambda x:x[1][f],reverse=True)
    if len(top)>=10 and p == False:
        return top[0:10]
    else:
        return top

def drawBar(i,t):
    if t == 0: t=1
    percent=i*100.00/t
    bar="["
    for b in range(int(percent/5)):
         bar+=">>"
    bar+="]{0:.2f}%"
    return bar.format(percent)

def drawTab(c):
    i=0
    td="<tr>{0}</tr>\n"
    temp=""
    while i <c:
        temp +="<td>{"+str(i)+"}</td>"
        i +=1
    return td.format(temp)

def drawList(s):
    k="<ul>{0}</ul>"
    items=list(s)
    temp=""
    i=0
    while i < 5:
        try:
            temp += "<li>"+str(items.pop())+"</li>\n"
            i +=1
        except IndexError:
            break
    _k=""
    if len(items)>0:
        _temp="<option>--More--</option>"
        _k="<li><select>{0}</select></li>"
        while True:
            try:
                _temp += "<option>"+str(items.pop())+"</option>"
            except IndexError:
                break
        _k=_k.format(_temp)
    temp+=_k
    return k.format(temp)
import time
def drawTime():
    e_curtime=time.time()
    s_curtime=e_curtime-7*24*3600
    _e=time.strftime("%Y.%m.%d",time.localtime(e_curtime))
    _s=time.strftime("%Y.%m.%d",time.localtime(s_curtime))
    titletime=_s + " - " + _e
