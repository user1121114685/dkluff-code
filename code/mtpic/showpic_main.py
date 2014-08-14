import CGIHTTPServer
import BaseHTTPServer
import threading
import socket
from time import sleep

def picdb():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(("127.0.0.1",10000))
    db='/tmp/a.txt'
    f=open(db)
    plist=[]
    for k in f:
        plist.append(k[:-1])

    plen=len(plist)

    while True:
        data,address = s.recvfrom(8092)
        if int(data)< plen:
            s.sendto(plist[int(data)],address)
        else:
            s.sendto(plist[0],address)

class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ["/htcgi",]

PORT = 80

httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)

print "Starting httpd at port:", PORT
http_th = threading.Thread(target=httpd.serve_forever)
http_th.daemon = True
http_th.start()

print "Starting DB"
db_th = threading.Thread(target=picdb)
db_th.daemon = True
db_th.start()

while 1:
    sleep(3600)
