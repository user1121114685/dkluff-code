#!/usr/bin/env py27
import cgi
import Cookie
import socket
import os

def getCookie(i):
    cookies=os.environ['HTTP_COOKIE']
    v = cookies.split(';')
    for k in v:
        if i in k:
            return k.split('=')[1]

def getPic(i):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(str(i),("127.0.0.1",10000))
    resp,data =  s.recvfrom(8092)
    s.close()
    return resp

cookie = Cookie.SimpleCookie()
form = cgi.FieldStorage()
#npic = form.getvalue('npic')
pic = 0
try:
    pic = form['pic'].value
except KeyError:
    try:
        pic = getCookie('pic')
    except Exception:
        pass

if pic > 0:
    cookie['pic'] = pic
    cookie['pic']['expires'] = 365 * 24 * 60 * 60
    print cookie

picdir=getPic(int(pic))

print "Content-Type: text/html \r"
print "\r"

print "**</br>"
print """
    <a href="/htcgi/showpic.py?pic={0}">
    <img src="/pics/{1}" width=100%/>
    </a>
      """.format(int(pic)+1,picdir)


