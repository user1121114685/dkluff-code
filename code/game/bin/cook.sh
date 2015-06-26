#!/bin/sh


org=$1
cookdir=$2
dst="/root/otg_game/units/"

if [ "$1" == "cp" ];then
    cp output/* $dst/.
    exit
fi


for f in `ls $org | grep slk$`;do
    python bin/prslk.py $org/$f $cookdir/comm.slk.cook >output/$f
    if [ -f "$cookdir/$f.cook" ];then
        tmpf=`tempfile`
        python bin/prslk.py output/$f $cookdir/$f.cook > $tmpf
        mv $tmpf output/$f
    fi

done

for f in `ls $org | grep txt$`;do
    ./bin/prtxt.sh $org/$f $cookdir/comm.txt.cook>./output/$f
    if [ -f "$cookdir/$f.cook" ];then
        ./bin/prtxt.sh output/$f $cookdir/$f.cook >output/$f
    fi
done
