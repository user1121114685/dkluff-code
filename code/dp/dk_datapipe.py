import sys
import socket
import threading
import SocketServer

ACL_CLIENT='/tmp/acl_client.txt'
LOG_ACL='/tmp/sec_acl.log'

SIZE_BUF = 1024
PAT_List = {
        "test":("",0,"localhost",22),#port 0 is an random port
        }

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    conf = "" #conf=(host,port)

    def handle(self):
        self.remote = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.remote.connect(self.conf)
        f = FetcherThread(self.remote, self.request)
        f.start()
        while 1:
            try:
                dataReceived = self.request.recv(SIZE_BUF)
                if not dataReceived: break
                self.remote.send(dataReceived)
            except socket.timeout:
                continue
    def finish(self):
        self.request.close()
        self.remote.close()

def setHandler(config,Handler):
    class _Handler(Handler):
        conf = config
    return _Handler

import time
def chkacl(req,ip):
    dst=req.getsockname()
    f = open(ACL_CLIENT)
    log = open(LOG_ACL,'a')
    for l in f:
        if ip[0] == l[:-1]:
            f.close()
            log.writelines(str(ip) + " Connect/"+str(dst)+"/ @" +time.strftime("%Y.%m.%d %H:%M:%S")+"\r\n")
            return True
    log.writelines(str(ip) + " Denied/"+str(dst)+"/ @" +time.strftime("%Y.%m.%d %H:%M:%S")+"\r\n")
    log.close()
    return False

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    def verify_request(self,request,client_address):
        return chkacl(request,client_address)

class FetcherThread(threading.Thread):
    def __init__(self,remote,local):
        threading.Thread.__init__(self)
        self.remote = remote
        self.local = local
    def run(self):
        while 1:
            try:
                dataReceived = self.remote.recv(SIZE_BUF);
                if not dataReceived: break
                self.local.send(dataReceived)
            except socket.timeout:
               continue
        self.remote.close()
        self.local.close()


def runPAT(PORT,conf,HOST=''):
    server = ThreadedTCPServer((HOST, PORT), setHandler(conf,ThreadedTCPRequestHandler))
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name,conf
    #server.shutdown()
if __name__ == "__main__":
    for h in PAT_List:
        runPAT(PAT_List[h][1],PAT_List[h][2:4])
    print "Start Threads done!Press Ctrl-C to quit!"
    while 1:
        time.sleep(3600)
    #sys.exit(0)

