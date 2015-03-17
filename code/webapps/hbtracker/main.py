#!/usr/bin/env python
import CGIHTTPServer
import BaseHTTPServer
import threading
import socket
from time import sleep


class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ["/htcgi",]

PORT = 80

httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)

print "Starting httpd at port:", PORT
http_th = threading.Thread(target=httpd.serve_forever)
http_th.daemon = True
http_th.start()


while 1:
    sleep(3600)
