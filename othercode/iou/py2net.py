#!/usr/bin/python

import os,sys,socket,select,struct,pcap,traceback

"""
WARNING: This script was written by a network engineer, and reading it may induce vomiting in 
        software engineers and computer scientists.

        Used to connect network interfaces with UNIX sockets that have a certain header format. If you
happen to find this functionality useful for something, well, all the better. Can also do serial 
interfaces now! See other scripts for doing remote captures on interfaces.

Many thanks to the person who wrote a certain perl script for figuring out this header format.

This script uses two files, should be in the same directory as the script, but you can change the
path in the options below:
        NETMAP - Same as always, except use the pseudo-instance as one of the instances.
                the interface maps to something in the IFMAP file...
        IFMAP - Looks like this:
                        0>lo
                        1|eth0
                        2>vboxnet0
                The first value is the interface number on the pseudo-instance. The middle symbol 
                is the forwarding direction. | means bidirectional (forward to and from the real interface)
                whereas the > means unidirectional (forward to, but not back from the real interface). 
                        ***WARNING: If you are forwarding from a SERIAL interface, make it UNIDIRECTIONAL, otherwise
                        it will get in a forwarding loop.
                For example, by default, if you have
                        100:0 101:0/1 1023:1 
                in the NETMAP file, it will forward traffic from instance 100 int 0 and
                instance 101 int 0/1 to eth0, and vice-versa. 
                 

        HINT: Virtualbox host-only adapters are awesome here. You can connect ... things
        to virtualbox, and you can easily capture on these interfaces to packet capture
        what the two other instances are talking about.

Warning: This script needs python-libpcap installed, and thus needs to be run as root (it 
        also opens raw sockets.) It will also try to delete whatever file is specified for
        the pseudo-instance socket if it exists (ie: /tmp/netio0/1023 in by default). I am not
        responsible if this script causes your computer, cat, or neighbourhood to explode into 
        shards of glass and metal.

This script doesn't really do any validation on the NETMAP or IFMAP files. You can have as many
instances as you want per line, but don't put your pseudo-instance on a line twice. 

If you want to see alot of text scroll by, and verify its working, turn on verbose debug.
"""

"""
And yes, I know I don't tear down the sockets, but this is a single thread, and its always
released the resources for me after a ctrl-c.
"""

#OPTIONS
PSEUDO_INSTANCE = '1023'
UNIX_SOCKET_DIR = '/tmp/netio0/'
VERBOSE_DEBUG = 0


UNIX_SOCKET_PATH = UNIX_SOCKET_DIR + PSEUDO_INSTANCE
NETMAP_FILE = './NETMAP'
IFMAP_FILE = './IFMAP'


INSTANCE_ID = 0
IFINDEX = 1


def parseNetmap(filename):
        netmapList, lineBuffer = [], []
        #Looking at each line
        if VERBOSE_DEBUG: print "NETMAP FILE RESULTS:"
        for line in open(filename, 'r'):
                #Skip over it if its a blank line or there is a comment at the start
                if not line.strip() or line.find('#') == 0: continue
                #If there is a comment in the middle of a string
                if line.find('#') != -1: line = line[0:line.find('#')]
                        
                #Looking at each instance:ifIndex pair
                #Has form [ instanceID, ifIndex, remoteHost ]
                for pair in line.split():
                        #Get the instanceID
                        instanceID, pair = pair.split(':')

                        #Get the remoteHost
                        if pair.find('@') != -1:
                                pair, remoteHost = pair.split('@')
                        else:
                                remoteHost = ""
                        
                        #Get the ifIndex and convert it to a single number if its in x/y form
                        if pair.find('/') != -1:
                                pair = pair.split('/')
                                ifIndex = int(pair[0]) + ( int(pair[1]) * 16 )
                        else:
                                ifIndex = int(pair)

                        lineBuffer.append([instanceID, ifIndex, remoteHost])
                if VERBOSE_DEBUG: print lineBuffer
                #Check to make sure our pseudo-instance ID is in the line, otherwise
                #we don't care about it, and it can be discarded.
                for pair in lineBuffer:
                        if pair[0] == PSEUDO_INSTANCE: 
                                netmapList.append(lineBuffer)
                                break;
                #Empty out the lineBuffer for the next run
                lineBuffer = []                 

        return netmapList

def parseIfmap(filename):
        ifmapList = []
        try:
                for line in open(filename, 'r'):
                        #Skip over it if its a blank line.
                        if not line.strip() or line.find('#') == 0: continue
                        if line.find('#') != -1: line = line[0:line.find('#')]
                        if line.find('>') != -1:
                                lineBuffer = line.strip().split('>')
                                ifmapList.append( [lineBuffer[0], lineBuffer[1], 0] )
                        elif line.find('|') != -1:
                                lineBuffer = line.strip().split('|')
                                ifmapList.append( [lineBuffer[0], lineBuffer[1], 1] )
        except:
                print "Error parsing the IFMAP file."
                sys.exit(0)
        if VERBOSE_DEBUG: print "\n\nIFMAP LIST RESULTS:\n", ifmapList
        return ifmapList                        

def createPseudoInstanceSocket():
        #Bind the UNIX Domain socket
        try:    
                if os.path.exists(UNIX_SOCKET_PATH):
                        os.unlink(UNIX_SOCKET_PATH)
        except:
                print "Failed to create the pseudo-instance UNIX socket: ", UNIX_SOCKET_PATH, " already exists."
                sys.exit(1)

        try:
                unixSock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                unixSock.bind(UNIX_SOCKET_PATH)
        except:
                print "Failed to bind to the pseudo-instance UNIX socket."
                sys.exit(1)

        return unixSock

def createUnixSockets(netmap):
        unixSocketMap = {}
        unixSocketList = []

        for line in netmap: 
                for pair in line:
                #If it isn't our pseudo-instance number, and it isn't already in the map...
                        if pair[INSTANCE_ID] != PSEUDO_INSTANCE and pair[INSTANCE_ID] not in unixSocketMap:
                                try:
                                        unixSocketMap[ pair[INSTANCE_ID] ] = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                                        unixSocketMap[ pair[INSTANCE_ID] ].connect(UNIX_SOCKET_DIR + pair[INSTANCE_ID] )
                                        unixSocketList.append(unixSocketMap[pair[INSTANCE_ID]])
                                        print "Successfully connected to instance: ", pair[INSTANCE_ID]                         
                                except:
                                        print "Failed to connect to instance: ", pair[INSTANCE_ID]
                                        #If we couldn't connect, make sure its not in the map
                                        if pair[INSTANCE_ID] in unixSocketMap:
                                                del unixSocketMap[ pair[INSTANCE_ID] ]
                                
        return unixSocketMap, unixSocketList    


def createSockets(ifmap):
        socketMap, pcapMap = {}, {}
        pcapList = []

        for pair in ifmap:
                try:
                        socketMap[pair[0]] = socket.socket(socket.PF_PACKET, socket.SOCK_RAW)
                        socketMap[pair[0]].bind( (pair[1], 0) )
                        print "Successfully bound to interface: ", pair[1]
                except:
                        print "Failed to bind socket to interface: ", pair[1], ". Continuing execution..."
                try:
                        #Check to see if its bidirectional. 
                        pcapMap[pair[0]] = pcap.pcapObject()
                        #If its bidirectional, add the packet capture object to the select read list
                        #This is a bit of a hack, I know its not really proper, but it was a quick fix...
                        if pair[2]:
                                pcapMap[pair[0]].open_live( pair[1], 1600, 1, 0 )
                                pcapList.append(pcapMap[pair[0]])
                except:
                        print "Failed to create pcap object for interface: ", pair[1], ". Continuing execution..."
                                

                        
        return socketMap, pcapMap, pcapList


def createNetworkUnixFIB(netmap, socketMap, unixSocketMap):
        networkToUnixFIB = {}

        for line in netmap:
                #Find the one with the pseudo instance number
                for pseudoInstanceIndex, pair in enumerate(line):
                        if pair[INSTANCE_ID] == PSEUDO_INSTANCE:
                                break;
                #Lookup the socket object using the ifIndex, and put it in the dictionary.
                
                try:
                        srcIfIndex = line[pseudoInstanceIndex][IFINDEX]
                        pcapObject = pcapMap[ str(srcIfIndex) ]
                        networkToUnixFIB[ pcapObject ] = []
                except KeyError:
                        print "Couldn't find instance ", str(srcIfIndex), " in IFMAP."
                        traceback.print_exc(file=sys.stdout)
                
                for index, pair in enumerate(line):
                        if pair[INSTANCE_ID] == PSEUDO_INSTANCE: continue
                        networkToUnixFIB[ pcapObject ].append( [ pair[INSTANCE_ID], pair[IFINDEX], srcIfIndex, unixSocketMap[ pair[INSTANCE_ID] ] ] )
                        
                
        return networkToUnixFIB




"""
allSockets is a flat list of all the sockets we'll be waiting on, including 
the pseudo-instance UNIX socket, and the sockets
bound to actual interfaces.
"""
allSockets = []
pseudoSock = createPseudoInstanceSocket()
allSockets.append(pseudoSock)
"""
ifmap contains the information in the IFMAP file. Its a mapping between the ifIndex on the
pseudo-instance created by the script and a network interface. Has the following structure:
                [
        line1:          [ifIndex, interface],
        linen:          [ifIndex, interface]
                ]
"""
ifmap = parseIfmap(IFMAP_FILE)

"""
socketMap is a dictionary that has a map between the ifIndex on the pseudo-instance and
a socket object bound to the network interface. Has the following structure:
        { ifIndex1 : socketObject1, ifIndexn : socketObjectn }

This is used as the FIB for forwarding from UNIX sockets to network interfaces.
"""
"""
socketList is simply a list of all the network sockets created.
"""
socketMap, pcapMap, pcapList = createSockets(ifmap)
allSockets.extend(pcapList)
"""
netmap contains the information in the NETMAP file
Has the following structure: [ 
                line1:          [ [instanceID1, ifIndex1, hostname1], [instanceIDn, ifIndexn, hostnamen] ],
                linen:          [ [instanceID1, ifIndex1, hostname1], [instanceIDn, ifIndexn, hostnamen] ]
                             ]
"""
netmap = parseNetmap(NETMAP_FILE)

"""
unixSocketMap is essentially the same as socketMap but for the UNIX domain sockets.
In this case the key is the instance ID, and the value is the socket object:
        { instanceID1 : socketObject1, instanceIDn : socketObjectn }
"""
unixSocketMap, unixSocketList = createUnixSockets(netmap)


"""
networkToUnixFIB is a dictionary used to forward frames ingressing on an actual network socket and
egressing on a UNIX socket. it has the following structure:
        { 
                networkSocketObject1 : [ [dstInstanceID1, dstIfIndex1, srcIfIndex1, dstUnixSocket1], [dstInstanceIDn, dstIfIndexn ...
                networkSocketObjectn : [ [dstInstanceID1, dstIfIndex1, srcIfIndex1, dstUnixSocket1], [dstInstanceIDn, dstIfIndexn ...
        }
"""
networkToUnixFIB = createNetworkUnixFIB(netmap, socketMap, unixSocketMap)

while 1:
        readList, wl, xl = select.select(allSockets, [], [])
        
        for socket in readList:
                #If it came from the Pseudo-Instance Socket
                if socket == pseudoSock:
                        data = socket.recv(1600)
                        dstInstance, srcInstance, dstIfIndex, srcIfIndex, blank = struct.unpack("!HHBBH", data[:8])
                        if VERBOSE_DEBUG: print "\n***********GOT A FRAME ON PSEUDO-INSTANCE UNIX SOCKET************\nDest Instance: ", dstInstance, "Source Instance: ", srcInstance, "\nDest If: ", dstIfIndex, "Source If: ", srcIfIndex,"\nSource MAC: ",data[14:19].encode('hex')," Dest MAC: ",data[8:14].encode('hex') 
                        try:
                                socketMap[ str(dstIfIndex) ].send(data[8:])
                                if VERBOSE_DEBUG: print "\n^^^^^^^^^^^SENDING A FRAME TO NETWORK INTERFACE^^^^^^^^^\nSource MAC: ",data[14:19].encode('hex')," Dest MAC: ",data[8:14].encode('hex') 
                        except KeyError:
                                print "Unix to Network lookup failed for destination index: ", str(dstIfIndex)
                                traceback.print_exc(file=sys.stdout)
                        except:
                                print "Network error, couldn't send data to interface with index: ", dstIfIndex
                                traceback.print_exc(file=sys.stdout)
                else:
                        #Get the next packet in PCAP format
                        data = socket.next()
                        if VERBOSE_DEBUG: print "\n==============GOT A FRAME ON NETWORK INTERFACE===========\n Source MAC: ", data[1][6:12].encode('hex')," Dest MAC: ", data[1][0:6].encode('hex')

                        #Check to see if the frame came from an instance on this segment, if it did, set a flag so it gets dropped.
                        fromSameSegment = 0
                        #Extract the OUI from the MAC
                        OUI = (ord(data[1][6]) << 16) + (ord(data[1][7]) << 8) + ord(data[1][8])
                        #Did it come from an instance?
                        if OUI == 0xAABBCC:
                                srcInstance, srcIfIndex = struct.unpack("!HB", data[1][9:12])
                                if VERBOSE_DEBUG: print "OUI: ", hex(OUI), "    Instance: ", hex(srcInstance), "        IfIndex: ", hex(srcIfIndex)
                                try:
                                        for FIBentry in networkToUnixFIB[ socket ]:
                                                #Is it an instance on this segment?
                                                if int(FIBentry[0]) == srcInstance and FIBentry[1] == srcIfIndex:
                                                        fromSameSegment = 1
                                except KeyError:
                                        print "Network to Unix lookup failed for source pcap object: ", socket
                                        traceback.print_exc(file=sys.stdout)                    
                        #If it wasn't from the same segment, actually send the frame to the UNIX sockets
                        if not fromSameSegment:
                                        for FIBentry in networkToUnixFIB[ socket ]:
                                                ##Construct the header
                                                header = struct.pack('!HHBBH', int(FIBentry[0]), int(PSEUDO_INSTANCE), int(FIBentry[1]), FIBentry[2], 0x0100)
                                                try:
                                                        #Send it to the unix socket spec'd in the FIB
                                                        FIBentry[3].send(header+data[1])
                                                except:
                                                        print "Failed to send data to instance ", FIBentry[0], "interface ", FIBentry[1]
                                                        traceback.print_exc(file=sys.stdout)
                                                if VERBOSE_DEBUG: 
                                                        dstInstance, srcInstance, dstIfIndex, srcIfIndex, blank = struct.unpack("!HHBBH", header)
                                                        print "\n++++++++++++SENDING A FRAME TO UNIX SOCKET++++++++++\nDest Instance: ", dstInstance, "  Source Instance: ", srcInstance, "\nDest If: ", dstIfIndex, "Source If: ", srcIfIndex,"\nSource MAC: ",data[1][14:19].encode('hex')," Dest MAC: ",data[1][8:14].encode('hex')
                                
                
