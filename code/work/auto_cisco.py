#!/usr/bin/env python
import select
import telnetlib
import socket
import sys
from time import sleep
import logging

try:
    from paramiko.client import SSHClient
    from paramiko.client import AutoAddPolicy
except Exception:
    print """
          Missing module \"paramiko\"
          run below cmd to install,otherwise,the ssh will not work:\n 
            sudo pip install paramiko 
          """
#--self def lib--START
ASA_MORE="--- More ---"
IOS_MORE="--More--"
SGS=[IOS_MORE,ASA_MORE]

def matchsg(m,sgs=SGS):
  for s in sgs:
     if s in m:
       logging.debug("_____,matched more")
       return True

  return

WTIME=1
RBYTES=1024

EOF="#"
TMP_EOF=">"

TEL_UNTIL_USER="ername: "
TEL_UNTIL_PASSWORD="sword: "


class AdvSSHClient():
      def __init__(self):
          self.channel = None #ssh channel
          self.client = None
          self.CR ="\r\n"

      def open(self, host, port=22,username=None,password=None):
          self.client = SSHClient()
          self.client.set_missing_host_key_policy(AutoAddPolicy())
          self.client.connect(hostname=host,port=port,username=username,password=password,look_for_keys=False)
          t=self.client.get_transport()
          self.channel=t.open_session()
          self.channel.get_pty()
          self.channel.invoke_shell()

      def enable(self,enpassword):
          print self.doexec("en")
          sleep(WTIME)
          print self.doexec(enpassword)


      def read_all(self,tn,rbytes=RBYTES,waittime=WTIME):
          t=""
          while select.select([tn],[], [],WTIME) == ([tn], [], []):
            t+=tn.recv(rbytes)

          return t

      def doexec(self,cmdstring,eof=EOF,rbytes=RBYTES,waittime=WTIME):
          m=""
          tn=self.channel
          tn.send(cmdstring+"\n")
          m=self.read_all(tn)

          if matchsg(m):
            tn.send(self.CR)
            logging.debug("____sending CR")
            while 1:
              t=self.read_all(tn)
              m+=t
              if not matchsg(t):
                logging.debug("_____get msg:"+t)
                break
              tn.send(self.CR)
          return m

class sockT:
      def __init__(self,sock):
          self.sock=sock

      def send(self,data):
          return self.sock.send(data)

      def recv(self,rbytes=RBYTES):
          return self.sock.recv(rbytes)

      def send_ready(self):
          s=self.sock
          return select.select([], [s], [], WTIME) == ([], [s], [])

      def recv_ready(self):
          s=self.sock
          return select.select([s], [], [],WTIME) == ([s], [], [])

      def fileno(self):
          return self.sock.fileno()

class AdvTELNETClient(AdvSSHClient):

      def login(self,user,password,tlu=TEL_UNTIL_USER,tlp=TEL_UNTIL_PASSWORD,eof=EOF):
          tn=self.client
          #tn.interact()
          #tn.set_debuglevel(5)
          #print tn.read_all()
          print tn.read_until(tlu)
          tn.write(user+"\n")
          print tn.read_until(tlp)
          tn.write(password+"\n")
          print tn.read_until(eof)

      def open(self,host,port=23,username="admin",password="cisco",
               tlu=TEL_UNTIL_USER,tlp=TEL_UNTIL_PASSWORD,eof=EOF):
          self.client=telnetlib.Telnet(host,port)
          sock=self.client.get_socket()
          self.channel=sockT(sock)
          self.login(user=username,password=password,tlu=TEL_UNTIL_USER,tlp=TEL_UNTIL_PASSWORD,eof=EOF)

      def qexec(self,cmdstring,eof=EOF,rbytes=RBYTES,waittime=WTIME):
          #quick exec for telnet
          m=""
          tn=self.client
          tn.write(cmdstring+"\n")
          m=tn.read_until(eof)
          return m


#--self def lib--END--
def runcmd(cmdfile,logfile,client):
    cf=open(cmdfile)
    lf=open(logfile,'a')

    for line in cf:
      m=client.doexec(line)
      client.doexec("!")
      print >>lf,m
      logging.info(m)


#-----cmd block start---

client,h=AdvSSHClient(),"1.1"
#client,h=AdvTELNETClient(),"1.1"
logging.basicConfig(level=logging.DEBUG)
client.open(host=h,username=u,password=p)
client.enable(p)
print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
runcmd("tst","tslog",client)
print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

#-----cmd block end-----

#----close----
