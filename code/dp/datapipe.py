#   datapipe.py
#   Copyright (C) 2007 Filia Tao
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import sys
import socket
import SocketServer
from select import select
import traceback
sample_config = {
    "server_addr":("",2323),
    "remote_addr":("58.192.114.8",23)
}

class datapipeServer(SocketServer.TCPServer):
    def __init__(self,config):
        SocketServer.TCPServer.__init__(self,config["server_addr"],None)
        self.config = config
        self.in_sockets = []
        self.out_sockets = []
        self.pair = {}

    def serve_forever(self):
        print self.config
        while True:
            try:
                tri = select([self.socket] + self.in_sockets + self.out_sockets,[],[])
                for s in tri[0]:
                    if s is self.socket:
                        ins,client_addr = self.get_request()
                        print "handle client " + str(client_addr)
                        outs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        outs.bind((self.config["server_addr"][0],0))
                        outs.connect(self.config["remote_addr"])
                        self.pair[ins] = outs
                        self.pair[outs] = ins
                        self.in_sockets.append(ins)
                        self.out_sockets.append(outs)
                    elif s in self.in_sockets:
                        data = s.recv(4096)
                        if(self.pair[s].send(data)>=0):
                            print "client " + str(s.getpeername()) + " disconnected";
                            self.pair[s].close()
                            s.close()
                            self.in_sockets.remove(s)
                            self.out_sockets.remove(self.pair[s])

                    elif s in self.out_sockets:
                        data = s.recv(4096)
                        if(self.pair[s].send(data)>=0):
                            print "client " + str(self.pair[s].getpeername()) + " disconnected";
                            self.pair[s].close()
                            s.close()
                            self.out_sockets.remove(s)
                            self.in_sockets.remove(self.pair[s])

            except Exception,e:
                print "Error Occous"
                #traceback.print_stack()
                print e

def run(server_class=datapipeServer,
        config=sample_config):
    print "start server on " + str(config["server_addr"])
    datapiped = server_class(config)
    datapiped.serve_forever()

def print_help():
    print '''datapipe.py  A datapipe program (by python@bbs.seu.edu.cn)
usage: python datapipe.py [localhost] localport remotehost remoteport
examples:  python datapipe.py 23 bbs.seu.edu.cn 23
           python datapipe.py 10.22.0.2 2323 58.192.114.8 23
'''
if __name__ == "__main__":
    if len(sys.argv) > 4:
        print_help()
        sys.exit(0)
    elif len(sys.argv) == 4:
        argv = [""] + sys.argv[1:]
    else:
        argv = sys.argv[1:]
    #print argv
    myconfig = {
        "server_addr":(argv[0],int(argv[1])),
        "remote_addr":(argv[2],int(argv[3])),
    }
    run(config = myconfig)
