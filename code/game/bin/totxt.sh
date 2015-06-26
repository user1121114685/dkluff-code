#!/bin/sh
filelist=$1/csvfilelist.txt
db=$1/all.db
dst=$1/data

for f in `cat $filelist | grep -v ^# |grep -v ^$ `;do
     cat $db | sed "/$f/!d;s/$f//g;s/ /\n/g;G" >$dst/$f
done
