#!/bin/sh


cat $1 | grep "^kat" | while read l
do
    src=`echo $l | awk '{print $2}'`
    dst=`echo $l | awk '{print $3}'`
    sed  -i "/$src/p;s/$src/$dst/g" all.db

done
