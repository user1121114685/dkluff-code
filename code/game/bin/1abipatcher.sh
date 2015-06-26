#!/bin/sh

bn=$3
srcf="/root/otg_game/units/datacook/cmd.txt"
i=1
while [ $i -lt 10 ];do
    cat $srcf| sed -e '/./{H;$!d;}' -e "x;/$bn/b" -e d   | sed "s/I0/I$i/g" | sed "s/A0/A$i/g"
    i=$((i+1))
done | awk -v a=$1 -v b=$2 '{ if($4=="VAL"){$4=a;a=a+b} print}'
