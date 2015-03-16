#!/usr/bin/env python
import cgi
import socket
import os
import tempfile

form = cgi.FieldStorage()
tmplog = tempfile.mkstemp(dir='/logtmp/')[1]

with open(tmplog,'a') as f:
  print >>f ,form.value
  #f.writelines(form.value)

print "Content-Type: text/html \r"
print "\r"

print "OK!"


