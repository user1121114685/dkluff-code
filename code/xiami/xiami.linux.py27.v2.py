#!/usr/bin/env py27
import sys
import binascii
import os
from os.path import join
import xml.dom.minidom
import urllib
import re
import subprocess
import urllib2

#proxies = {'http': ''}
Proxies = {}

XML_ILLEGAL='\'|&|,'
FILENAME_ILLEGAL=':|\)|\(|"| |/|\;'
#decode url in xml
def decodeurl(urlcry):
    col=int(urlcry[0])
    urlcry=urlcry[1:]
    urllen=len(urlcry)

    sq_len=urllen/col
    lastcol=urllen%col
    sqstrs=[]
    while lastcol >0:
        sqstrs.append(urlcry[0:sq_len+1])
        urlcry=urlcry[sq_len+1:]
        lastcol-=1
    while len(urlcry) > 0:
        sqstrs.append(urlcry[0:sq_len])
        urlcry=urlcry[sq_len:]
    urluncry=''
    k=0
    while k <= sq_len+1:
        for s in sqstrs:
            try:
                urluncry += s[k]
            except IndexError:
                pass
        k += 1



    urldecode=''
    c=0
    while c < len(urluncry):
        if urluncry[c] == '%': # same as urllib.unquote("%5e")
            if urluncry[c+1]+urluncry[c+2] == '5E': #replace "^" with "0"
                urldecode += '0'
            else:
                urldecode += binascii.a2b_hex(urluncry[c+1]+urluncry[c+2])
            c +=3
        else:
            urldecode += (urluncry[c])
            c+=1
#    print urldecode
    return urldecode

class Song:
    name=''
    album=''
    artist=''
    url=''

#mkdir by album_name or artist_name
def mksubdir(sub_dir_name,prefix=None,tgdir=os.path.curdir):
    if prefix is not None:
        tgdir=join(prefix,sub_dir_name)
    else:
        tgdir=join(os.path.curdir,sub_dir_name)
    if not os.path.exists(tgdir):
        os.makedirs(tgdir)
    return tgdir

def downloadSong(url,output_name,skip=False):
    if skip is True and os.path.exists(output_name) is False:
        urllib.urlretrieve(url,output_name)
    elif skip is True and os.path.exists(output_name) is True:
        pass
    elif skip is False:
        urllib.urlretrieve(url,output_name)


def wget(url,output_name,skip=False):
    opt=["/usr/bin/wget",'-t','3','-q']
    if skip is True:
        opt.append('-nc')
    else:
        opt.append('-c')
    opt+=['-O',output_name,url]
    subprocess.Popen(opt)
    print "#Go background..."


#get song info by songID
#http://www.xiami.com/song/playlist/id/<SONG ID:1768939776>/object_name/default/object_id/0
def curl(url):
    try:
#        opener = urllib.FancyURLopener(Proxies)
#        opener.version = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0"
#        opener.addheader('User-Agent',opener.version)
#        return opener.open(url)
#
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        return opener.open(url)
    except Exception as e:
	print "#Fetch error:"
        print e
        return False

def getSonginfo(song_id):
    url="http://www.xiami.com/song/playlist/id/"+song_id+"/object_name/default/object_id/0"
    xmlf=curl(url)
    xmlfstring=''
    for line in xmlf:
	xmlfstring+=re.sub(XML_ILLEGAL, "", line)
    song = Song()
    try:
        dom = xml.dom.minidom.parseString(xmlfstring)
        song.url=decodeurl(dom.getElementsByTagName("location")[0].firstChild.nodeValue.rstrip())
        song.name=re.sub(FILENAME_ILLEGAL,"_",dom.getElementsByTagName("title")[0].firstChild.nodeValue.rstrip())
        song.album=re.sub(FILENAME_ILLEGAL,"_",dom.getElementsByTagName("album_name")[0].firstChild.nodeValue.rstrip())
        song.artist=re.sub(FILENAME_ILLEGAL,"_",dom.getElementsByTagName("artist")[0].firstChild.nodeValue.rstrip())
        return song
    except Exception as e:
        err="#Fetch song detail failed!,skip this song id:<{0}>!"
        print err.format(song_id)
	print e
        return


#get song_id(s) from page url
#http://www.xiami.com/artist/47821
#http://www.xiami.com/album/272329
#http://www.xiami.com/song/showcollect/id/6132943
def getSongids(url):
    numreg = re.compile(r'\d+')
    #reg = re.compile(r'xm_download..[0-9]+\'\)\;') #only artist page, or album page can match
    reg = re.compile(r'collect\(\'[0-9]+\'\)\;')

    html=curl(url)
    songids=set()
    if html is not False:
        for line in html:
            for m in re.findall(reg,line):
                n=numreg.search(m)
                songids.add(n.string[n.start():n.end()])
    return list(songids)
#--Mainn--#
EXIT_AllSUC = 0
EXIT_SOMEFAIL = 1
EXIT_NONESUC = 2

def climain():
    import argparse
    #import getopt
    #pkg: argparse is New in python 2.7
    parser = argparse.ArgumentParser(description='Fetch songs from  url of (album,song,collection..) \
                and save into certain directory.')
    parser.add_argument('url',nargs=1,metavar='http://...',help='a url of (album,song,collection..)')
    parser.add_argument('-p','--prefix',default='/media/Store/Music/',help='target dir to save (default:/media/Store/Music/)')
    parser.add_argument('-s','--saveby',default=0,type=int,help='organize songs by \
                            <0:artist , 1:album ,2:date>,default: 0')
    parser.add_argument('-d','--download',action='store_const',
                                       const=True, default=False,
                                       help='Download songs or not(Defaut:False)')
    parser.add_argument('-S','--skip',action='store_const',
                                       const=True, default=False,
                                       help='Skip exist songs(Default:no)')
    parser.add_argument('--wget',dest='downloader',action='store_const',
                                       const=wget, default=downloadSong,
                                       help='Download songs by wget from shell (Defaut:urllib)')


    args = parser.parse_args()

    download=args.download
    downloader=args.downloader
    skipsw=args.skip

    #global url
    url=args.url[0]
    songfext=".mp3"
    prefix=args.prefix
    saveby=args.saveby

    songs_info=[]
    songs_id=getSongids(url)

    total_ids=len(songs_id)

    for sid in songs_id:
        k=getSonginfo(sid)
        if k is not None:
            songs_info.append(k)

    total_songs=len(songs_info)
    print "#Get ids:%d,Get Songs:%d,Failed:%d" % (total_ids,total_songs,total_ids-total_songs)
    for s in songs_info:
        print "Processing:",s.name,s.url

        subdir=None
        if saveby == 0:
            subdir=s.artist
        elif saveby == 1:
            subdir=s.album
        else:
            subdir=None

        if not download: continue
        tgdir=mksubdir(subdir,prefix)
        downloader(s.url,join(tgdir,s.name+songfext),skip=skipsw)




if __name__ == "__main__":
    #sys.excepthook = excepthook
    #sys.exit(main())
    climain()
