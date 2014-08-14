#!/usr/env python
import os
from os.path import join
import shutil
import subprocess
import sys


'''
find $topdir -type f , then move && rename
'''
def findfiles(topdir):
    allfiles=[]
    for root, dirs, files in os.walk(topdir):
        allfiles += [join(root, name) for name in files]
    return allfiles


if __name__ == "__main__":

    srcIMGDIR='/data/xarc/imgs/picnew/'
    dstIMGDIR='/data/xarc/imgs/stardir/'
    TEMPDIR='/tmp/imgtemp/'
    outputlist='/tmp/outlist.txt'

    if not os.path.exists(TEMPDIR):
                os.makedirs(TEMPDIR)
    if not os.path.exists(dstIMGDIR):
                os.makedirs(dstIMGDIR)

    orgfiles=findfiles(srcIMGDIR)

    '''
    find $topdir -type f , then move && rename
    '''
    i=0
    tempfiles=[]
    for f in orgfiles:
        newfilename=join(TEMPDIR,"temp.jpg"+str(i))
        tempfiles.append(newfilename)
        i+=1
        #os.rename(f,newfilename)
        try:
            shutil.move(f,newfilename)
        except Exception as e:
            print e
            print "Can't Move files to tempdir , Exit..."
            sys.exit()

    output=open(outputlist,'w')
    for t in tempfiles:
        md5_val=subprocess.check_output(["md5sum",t]).split()
        dstfile=join(dstIMGDIR,md5_val[0]+".jpg")
        try:
            if len(md5_val) > 0:
                shutil.move(t,dstfile)
        except Exception as e:
            print e
            print "Can't Move files to dstIMGDIR , Exit..."
            sys.exit()
        print >>output,dstfile
        print "#SUC:#"+dstfile
    output.close()
    print "list is here:",outputlist





