#!/bin/sh
db=all.db
dst=./data

cat $db | grep -v ^# | grep -v ^$ | awk '{print $1}' | sort -u | while read nf;do
    echo >$dst/$nf
done

for f in `ls $dst | grep "txt$"`;do
    cat $db |grep $f| sed "s/$f //g;s/ /\n/g;G" >>$dst/$f
done
