#!/bin/sh


cat $1 | grep "^#-" | while read l
do
    src=`echo $l | awk '{print $2}'`
    dst=`echo $l | awk '{print $3}'`
    grep "ItemFunc.txt \[$src" all.db | sed "s/$src/$dst/g" >>all.db

done
cat $1 | grep [12]kit | sed 's/[12]kit //g' >>all.db
