#!/usr/bin/python

import os,sys,struct

documentation = "\n\
This file takes a pcap stream from stdin, and echos it to stdout.\n\
\n\
The only thing it does, is change the data link field in the header.\n\
\n\
I use this to pipe the file to wireshark to live capture on serial interfaces.\n\
\n\
Usage: python -u changeL2.py <encapType>\n\
        encapType: The data link encapsulation type. Can be: eth, ppp, hdlc, fr or\n\
        a number representing the DLT value, check the libpcap documentation for other\n\
        values for this field.\n\
"

if len(sys.argv) != 2:
        print documentation
        sys.exit(0)
else:
        datalinkName = sys.argv[1]
        datalink = 0
        if datalinkName == 'eth': datalink = 1
        elif datalinkName == 'ppp': datalink = 9
        elif datalinkName == 'hdlc': datalink = 104
        elif datalinkName == 'fr': datalink = 107
        else: 
                try:
                        datalink = int(datalinkName)
                except:
                        print "Invalid data link type. Exiting..."
                        sys.exit(0)

        

header = struct.unpack("=LHHlLLL", sys.stdin.read(24))
sys.stdout.write(struct.pack("=LHHlLLL", header[0], header[1], header[2], header[3], header[4], header[5], datalink ))

while 1:
        header = sys.stdin.read(16)
        sys.stdout.write(header)
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack("=LLLL", header)
        sys.stdout.write(sys.stdin.read(incl_len))

