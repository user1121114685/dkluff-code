#!/usr/bin/env python
import cgi
import socket
import os


form = cgi.FieldStorage()

f = open('/tmp/hb.log','a')
print >>f ,form.value

print "Content-Type: text/html \r"
print "\r"

print "OK!"


